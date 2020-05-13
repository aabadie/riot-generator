"""RIOT test generator module."""

import os

import click

from .common import render_source, read_config_file
from .common import check_common_params, check_params, check_riotbase
from .common import prompt_common_params, prompt_params, prompt_params_list


APPLICATION_PARAMS = {
    "name": {"args": ["Test name"], "kwargs": {}},
    "brief": {"args": ["Test brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
    "use_testrunner": {
        "args": ["Add testrunner script (y/N)"],
        "kwargs": {"default": False, "show_default": False},
    },
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features"]


def generate_test(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)

    params = {"common": {}, "test": {}}

    if config is not None:
        params = read_config_file(config, "board")

    if interactive:
        prompt_params(params, APPLICATION_PARAMS, "test")
        prompt_params_list(params, "test", *APPLICATION_PARAMS_LIST)
        prompt_common_params(params)

    check_params(params, APPLICATION_PARAMS.keys() ,"test")
    check_common_params(params)

    test_params = params["test"]

    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    tests_dir = os.path.join(riotbase, "tests")
    test_dir = os.path.join(tests_dir, test_params["name"])

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join("tests", test_params["name"])
    else:
        output_dir = os.path.expanduser(test_dir)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    elif not click.prompt(
        "'{name}' test directory already exists, "
        "overwrite (y/N)?".format(name=test_params["name"]),
        default=False,
        show_default=False,
    ):
        click.echo("Abort")
        return

    if "use_testrunner" in test_params and test_params["use_testrunner"] == "True":
        testrunner_dir = os.path.join(test_dir, "tests")
        render_source(params, "test", ["01-run.py"], testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, "01-run.py"), 0o755)

    files = ["main.c", "Makefile", "README.md"]
    render_source(params, "test", files, output_dir)

    click.echo(
        click.style(
            "Test application '{name}' generated in {output_dir} with success!".format(
                name=test_params, output_dir=output_dir
            ),
            bold=True,
        )
    )
