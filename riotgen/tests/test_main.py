"""Main generator tests."""

import os
import sys

import pytest
from click.testing import CliRunner
from mock import patch

from riotgen import __version__
from riotgen.application import APPLICATION_FILES, get_output_dir
from riotgen.board import BOARD_FILES, BOARD_INCLUDE_FILES
from riotgen.driver import (
    DRIVER_FILES,
    DRIVER_INCLUDE_FILES,
    DRIVER_INTERNAL_INCLUDE_FILES,
    DRIVER_NETDEV_FILES,
    DRIVER_NETDEV_INCLUDE_FILES,
)
from riotgen.main import riotgen
from riotgen.module import MODULE_FILES, MODULE_INCLUDE_FILES
from riotgen.pkg import PKG_FILES

HELP_OUTPUT = """Usage: riotgen [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  application  Bootstrap a RIOT application
  board        Bootstrap a RIOT board support
  driver       Bootstrap a RIOT driver module
  example      Bootstrap a RIOT example application
  module       Bootstrap a RIOT system module
  pkg          Bootstrap a RIOT external package
  test         Bootstrap a RIOT test application
"""


MISSING_PARAMETER_MSG = "Missing --interactive and/or --config options."

COMMANDS = [
    "application",
    "board",
    "driver",
    "example",
    "module",
    "pkg",
    "test",
]
COMMAND_FUNCS = [
    "riotgen.main.generate_application",
    "riotgen.main.generate_board",
    "riotgen.main.generate_driver",
    "riotgen.main.generate_example",
    "riotgen.main.generate_module",
    "riotgen.main.generate_pkg",
    "riotgen.main.generate_test",
]


def _check_generated_files(files, expected_dir, generated_dir, name):
    for input_name, output_name in files.items():
        if output_name is None:
            output_name = input_name
        else:
            output_name = output_name.format(name=name)
        assert os.path.exists(generated_dir.join(output_name))
        with open(os.path.join(expected_dir, input_name)) as f_expected:
            expected_content = f_expected.read()
        with open(
            generated_dir.join(output_name.format(name=name))
        ) as f_result:
            result_content = f_result.read()
        assert result_content == expected_content


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="doesn't work on windows"
)
def test_get_output_dir_test():
    params = {"test": {"name": "test"}}
    output_dir = get_output_dir(params, "test", "/tmp", "test_dir")
    assert output_dir == "/tmp/test_dir/test"


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
    "options,expected_args",
    [
        ([], [False, None, None]),
        (["-i"], [True, None, None]),
    ],
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


def test_command_generate_application_from_config(tmpdir):
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_data_dir = os.path.join(test_data_dir, "application")
    config_file = os.path.join(test_data_dir, "application.cfg")

    tmpdir.mkdir("application")
    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase").strpath
    output_dir = tmpdir.join("application")
    result = runner.invoke(
        riotgen,
        [
            "application",
            "-c",
            config_file,
            "-d",
            output_dir.strpath,
            "-r",
            riotbase,
        ],
    )

    assert result.exit_code == 0

    for filename in APPLICATION_FILES:
        assert os.path.exists(output_dir.join(filename))
        with open(os.path.join(expected_data_dir, filename)) as f_expected:
            expected_content = f_expected.readlines()
        with open(output_dir.join(filename)) as f_result:
            result_content = f_result.readlines()
        for idx, line in enumerate(expected_content):
            if line.startswith("RIOTBASE"):
                # riotbase line depends on the local computer so needs a
                # special handling
                assert result_content[idx] == f"RIOTBASE ?= {riotbase}\n"
            else:
                assert result_content[idx] == line

    msg = f"Application 'test' generated in {output_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_application_from_prompt(tmpdir):
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_data_dir = os.path.join(test_data_dir, "application")

    tmpdir.mkdir("application")
    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase").strpath
    output_dir = tmpdir.join("application")
    result = runner.invoke(
        riotgen,
        ["application", "-i", "-d", output_dir.strpath, "-r", riotbase],
        input=(
            "test\nTest application\nboard_test\nxtimer,fmt\nyxml\n"
            "periph_gpio\nLGPL21\ntest_name\ntest_email\ntest_orga\n"
        ),
    )

    assert result.exit_code == 0

    for filename in APPLICATION_FILES:
        assert os.path.exists(output_dir.join(filename))
        with open(os.path.join(expected_data_dir, filename)) as f_expected:
            expected_content = f_expected.readlines()
        with open(output_dir.join(filename)) as f_result:
            result_content = f_result.readlines()
        for idx, line in enumerate(expected_content):
            if line.startswith("RIOTBASE"):
                # riotbase line depends on the local computer so needs a
                # special handling
                assert result_content[idx] == f"RIOTBASE ?= {riotbase}\n"
            else:
                assert result_content[idx] == line

    msg = f"Application 'test' generated in {output_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_board_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_dir = os.path.join(test_data_dir, "board")
    config_file = os.path.join(test_data_dir, "board.cfg")

    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase")
    board_dir = riotbase.join("boards", "test")
    board_include_dir = board_dir.join("include")
    result = runner.invoke(
        riotgen,
        ["board", "-c", config_file, "-r", riotbase],
    )

    assert result.exit_code == 0

    _check_generated_files(BOARD_FILES, expected_dir, board_dir, name)
    _check_generated_files(
        BOARD_INCLUDE_FILES, expected_dir, board_include_dir, name
    )
    _check_generated_files({"Kconfig": None}, expected_dir, board_dir, name)

    msg = f"Support for board '{name}' generated in {board_dir.strpath} with success!"
    assert msg in result.output

    # Call the runner a second time to trigger overwrite prompt
    result = runner.invoke(
        riotgen, ["board", "-c", config_file, "-r", riotbase], input="y\n"
    )

    assert result.exit_code == 0

    msg = f"Support for board '{name}' generated in {board_dir.strpath} with success!"
    assert msg in result.output

    # Verify Abort is correctly triggered
    result = runner.invoke(
        riotgen, ["board", "-c", config_file, "-r", riotbase], input="\n"
    )

    assert result.exit_code > 0
    assert "Aborted!" in result.output


def test_command_generate_driver_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_dir = os.path.join(test_data_dir, "driver")
    config_file = os.path.join(test_data_dir, "driver.yml")

    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase")
    driver_dir = riotbase.join("drivers", "test")
    driver_include_dir = riotbase.join("drivers", "include")
    driver_internal_include_dir = driver_dir.join("include")
    result = runner.invoke(
        riotgen,
        ["driver", "-c", config_file, "-r", riotbase],
    )

    assert result.exit_code == 0

    _check_generated_files(DRIVER_FILES, expected_dir, driver_dir, name)
    _check_generated_files(
        DRIVER_INCLUDE_FILES, expected_dir, driver_include_dir, name
    )
    _check_generated_files(
        DRIVER_INTERNAL_INCLUDE_FILES,
        expected_dir,
        driver_internal_include_dir,
        name=name,
    )
    _check_generated_files({"Kconfig": None}, expected_dir, driver_dir, name)

    msg = f"Driver '{name}' generated in {driver_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_driver_netdev_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_dir = os.path.join(test_data_dir, "driver_netdev")
    config_file = os.path.join(test_data_dir, "driver_netdev.yml")

    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase")
    driver_dir = riotbase.join("drivers", "test")
    driver_include_dir = riotbase.join("drivers", "include")
    driver_internal_include_dir = driver_dir.join("include")
    result = runner.invoke(
        riotgen,
        ["driver", "-c", config_file, "-r", riotbase],
    )

    assert result.exit_code == 0

    _check_generated_files(DRIVER_FILES, expected_dir, driver_dir, name)
    _check_generated_files(
        DRIVER_INCLUDE_FILES, expected_dir, driver_include_dir, name
    )
    _check_generated_files(
        DRIVER_INTERNAL_INCLUDE_FILES,
        expected_dir,
        driver_internal_include_dir,
        name=name,
    )
    _check_generated_files(DRIVER_NETDEV_FILES, expected_dir, driver_dir, name)
    _check_generated_files(
        DRIVER_NETDEV_INCLUDE_FILES,
        expected_dir,
        driver_internal_include_dir,
        name,
    )

    msg = f"Driver '{name}' generated in {driver_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_example(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_data_dir = os.path.join(test_data_dir, "example")
    config_file = os.path.join(test_data_dir, "example.yml")
    output_dir = tmpdir.join("examples", name)

    result = runner.invoke(
        riotgen,
        ["example", "-c", config_file, "-r", tmpdir.strpath],
    )

    assert result.exit_code == 0

    _check_generated_files(
        APPLICATION_FILES, expected_data_dir, output_dir, name
    )

    msg = f"Example '{name}' generated in {output_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_module_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_dir = os.path.join(test_data_dir, "module")
    config_file = os.path.join(test_data_dir, "module.yml")

    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase")
    module_dir = riotbase.join("sys", "test")
    module_include_dir = riotbase.join("sys", "include")
    result = runner.invoke(
        riotgen,
        ["module", "-c", config_file, "-r", riotbase],
    )

    assert result.exit_code == 0

    _check_generated_files(MODULE_FILES, expected_dir, module_dir, name)
    _check_generated_files(
        MODULE_INCLUDE_FILES, expected_dir, module_include_dir, name
    )

    msg = f"Module '{name}' generated in {module_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_pkg_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_dir = os.path.join(test_data_dir, "pkg")
    config_file = os.path.join(test_data_dir, "pkg.cfg")

    tmpdir.mkdir("riotbase")
    riotbase = tmpdir.join("riotbase")
    pkg_dir = riotbase.join("pkg", "test")
    result = runner.invoke(
        riotgen,
        ["pkg", "-c", config_file, "-r", riotbase],
    )

    assert result.exit_code == 0

    _check_generated_files(PKG_FILES, expected_dir, pkg_dir, name)
    _check_generated_files({"Kconfig": None}, expected_dir, pkg_dir, name)

    msg = f"Package '{name}' generated in {pkg_dir.strpath} with success!"
    assert msg in result.output


def test_command_generate_test_from_config(tmpdir):
    name = "test"
    runner = CliRunner()
    test_data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    expected_data_dir = os.path.join(test_data_dir, "test")
    config_file = os.path.join(test_data_dir, "test.yml")
    output_dir = tmpdir.join("tests", name)

    result = runner.invoke(
        riotgen,
        ["test", "-c", config_file, "-r", tmpdir.strpath],
    )

    assert result.exit_code == 0

    _check_generated_files(
        APPLICATION_FILES, expected_data_dir, output_dir, name
    )
    _check_generated_files(
        {"01-run.py": None}, expected_data_dir, output_dir.join("tests"), name
    )

    msg = f"Test '{name}' generated in {output_dir.strpath} with success!"
    assert msg in result.output
