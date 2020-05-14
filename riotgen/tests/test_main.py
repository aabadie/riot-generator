"""Main generator tests."""

import os

import pytest
from mock import patch

from click.testing import CliRunner

from riotgen import riotgen, __version__
from riotgen.board import BOARD_INCLUDE_FILES
from riotgen.common import TEMPLATE_BASE_DIR


HELP_OUTPUT = """Usage: riotgen [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  application  Bootstrap a RIOT application
  board        Bootstrap a RIOT board support
  example      Bootstrap a RIOT example application
  pkg          Bootstrap a RIOT external package
  test         Bootstrap a RIOT test application
"""


MISSING_PARAMETER_MSG = "Missing --interactive and/or --config options."

COMMANDS = ["application", "board", "example", "pkg", "test"]
COMMAND_FUNCS = [
    "riotgen.main.generate_application",
    "riotgen.main.generate_board",
    "riotgen.main.generate_example",
    "riotgen.main.generate_pkg",
    "riotgen.main.generate_test",
]


def test_help():
    runner = CliRunner()
    result = runner.invoke(riotgen, ["--help"])
    assert result.exit_code == 0
    assert result.output == HELP_OUTPUT


def test_version():
    runner = CliRunner()
    result = runner.invoke(riotgen, ["--version"])
    assert result.exit_code == 0
    assert result.output == f"riotgen, version {__version__}\n"


@pytest.mark.parametrize("command", COMMANDS)
def test_missing_param(command):
    runner = CliRunner()
    result = runner.invoke(riotgen, [command])
    assert result.exit_code != 0
    assert "Missing --interactive and/or --config options." in result.output


@pytest.mark.parametrize("command,func", list(zip(COMMANDS, COMMAND_FUNCS)))
@pytest.mark.parametrize(
    "options,expected_args", [([], [False, None, None]), (["-i"], [True, None, None]),]
)
def test_command_interactive(command, func, options, expected_args):
    runner = CliRunner()
    with patch(func) as m_command:
        runner.invoke(riotgen, [command] + options)
        m_command.assert_called_once()
        if command == "application":
            m_command.assert_called_with(os.getcwd(), *expected_args)
        else:
            m_command.assert_called_with(*expected_args)


@pytest.mark.parametrize("command,func", list(zip(COMMANDS, COMMAND_FUNCS)))
def test_command_config(command, func, tmpdir):
    config_file = tmpdir.join("file.cfg")
    config_file.write("test")

    runner = CliRunner()
    with patch(func) as m_command:
        runner.invoke(riotgen, [command, "-c", config_file.strpath])
        m_command.assert_called_once()
        if command == "application":
            assert m_command.call_args.args[2].name == config_file.strpath
        else:
            assert m_command.call_args.args[1].name == config_file.strpath


@pytest.mark.parametrize("command,func", list(zip(COMMANDS, COMMAND_FUNCS)))
def test_command_riotbase(command, func, tmpdir):
    runner = CliRunner()
    with patch(func) as m_command:
        runner.invoke(riotgen, [command, "-r", tmpdir.strpath])
        m_command.assert_called_once()
        if command == "application":
            assert m_command.call_args.args[3] == tmpdir.strpath
        else:
            assert m_command.call_args.args[2] == tmpdir.strpath


def test_command_application_output_dir(tmpdir):
    runner = CliRunner()
    with patch("riotgen.main.generate_application") as m_command:
        runner.invoke(riotgen, ["application", "-d", tmpdir.strpath])
        m_command.assert_called_with(tmpdir.strpath, False, None, None)


@patch("riotgen.application.generate")
def test_command_generate_application(m_generate, tmpdir):
    runner = CliRunner()
    name = "test"
    output_dir = tmpdir.strpath
    m_generate.return_value = ({"application": {"name": name}}, None)
    result = runner.invoke(riotgen, ["application", "-d", output_dir])

    msg = f"Application '{name}' generated in {output_dir} with success!"
    assert msg in result.output


@patch("riotgen.board.render_source")
@patch("riotgen.board.generate")
def test_command_generate_board(m_generate, m_render, tmpdir):
    runner = CliRunner()
    name = "test"
    riotbase = tmpdir.strpath
    m_generate.return_value = ({"board": {"name": name}}, riotbase)
    result = runner.invoke(riotgen, ["board"])
    m_render.assert_called_with(
        {"board": {"name": name}},
        "board",
        BOARD_INCLUDE_FILES,
        riotbase,
        output_subdir="include",
    )

    msg = f"Support for board '{name}' generated in {riotbase} with success!"
    assert msg in result.output


@patch("riotgen.example.generate")
def test_command_generate_example(m_generate, tmpdir):
    runner = CliRunner()
    name = "test"
    riotbase = tmpdir.strpath
    m_generate.return_value = ({"example": {"name": name}}, riotbase)
    result = runner.invoke(riotgen, ["example"])

    msg = f"Example '{name}' generated in {riotbase} with success!"
    assert msg in result.output


@patch("riotgen.test.render_source")
@patch("riotgen.test.generate")
def test_command_generate_test(m_generate, m_render, tmpdir):
    runner = CliRunner()
    name = "test"
    riotbase = tmpdir.strpath
    m_generate.return_value = ({"test": {"name": name}}, riotbase)
    result = runner.invoke(riotgen, ["test"])

    msg = f"Test application '{name}' generated in {riotbase} with success!"
    assert msg in result.output
    assert m_render.call_count == 0

    params = {"test": {"name": name, "use_testrunner": "True"}}
    m_generate.return_value = (params, riotbase)
    with patch("os.chmod"):
        result = runner.invoke(riotgen, ["test"])
        testrunner_dir = os.path.join(riotbase, "test")
        m_render.assert_called_with(params, "test", ["01-run.py"], testrunner_dir)

    msg = f"Test application '{name}' generated in {riotbase} with success!"
    assert msg in result.output


@patch("riotgen.pkg.render_file")
@patch("riotgen.pkg.generate")
def test_command_generate_pkg(m_generate, m_render, tmpdir):
    runner = CliRunner()
    name = "test"
    riotbase = tmpdir.strpath
    m_generate.return_value = ({"pkg": {"name": name}}, riotbase)
    result = runner.invoke(riotgen, ["pkg"])

    template_dir = os.path.join(TEMPLATE_BASE_DIR, "pkg")
    file_out = os.path.join(riotbase, "{}.mk".format(name))
    m_render.assert_called_with(
        {"pkg": {"name": name}}, template_dir, "pkg.mk.j2", file_out
    )

    msg = f"Package '{name}' generated in {riotbase} with success!"
    assert msg in result.output
