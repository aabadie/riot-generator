"""RIOT test generator module."""

import os

import click

from .common import render_source, generate
from .application import APPLICATION_FILES, APPLICATION_PARAMS_LIST


APPLICATION_PARAMS = {
    "name": {"args": ["Test name"], "kwargs": {}},
    "brief": {"args": ["Test brief description"], "kwargs": {}},
    "use_testrunner": {
        "args": ["Add testrunner script (y/N)"],
        "kwargs": {"default": False, "show_default": False},
    },
}


def generate_test(interactive, config, riotbase):
    """Generate the code of a test application."""
    group = "test"
    params, output_dir = generate(
        group,
        APPLICATION_PARAMS,
        APPLICATION_PARAMS_LIST,
        APPLICATION_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="tests",
    )

    test_params = params[group]
    if "use_testrunner" in test_params and test_params["use_testrunner"] == "True":
        testrunner_dir = os.path.join(output_dir, "test")
        render_source(params, group, ["01-run.py"], testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, "01-run.py"), 0o755)

    click.echo(
        click.style(
            "Test application '{name}' generated in {output_dir} with success!".format(
                name=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
