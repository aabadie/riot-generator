"""RIOT test generator module."""

import os

import click

from .common import check_overwrite, render_source
from .application import load_and_check_application_params, render_application_source


APPLICATION_PARAMS = {
    "name": {"args": ["Test name"], "kwargs": {}},
    "brief": {"args": ["Test brief description"], "kwargs": {}},
    "use_testrunner": {
        "args": ["Add testrunner script (y/N)"],
        "kwargs": {"default": False, "show_default": False},
    },
}


def _get_output_dir(params, group, riotbase):
    """Helper function for tests.

    >>> params = {"test": {"name": "test"}}
    >>> _get_output_dir(params, "test", "/tmp")
    '/tmp/tests/test'
    """
    return os.path.join(riotbase, "tests", params[group]["name"])


def generate_test(interactive, config, riotbase):
    """Generate the code of a test application."""
    group = "test"
    params = load_and_check_application_params(group, interactive, config, riotbase,)

    output_dir = _get_output_dir(params, group, riotbase)
    check_overwrite(output_dir)

    render_application_source(params, group, output_dir)

    test_params = params[group]
    if "use_testrunner" in test_params and test_params["use_testrunner"] == "True":
        testrunner_dir = os.path.join(output_dir, "test")
        render_source(params, group, ["01-run.py"], testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, "01-run.py"), 0o755)

    click.echo(
        click.style(
            f"Test '{params[group]['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
