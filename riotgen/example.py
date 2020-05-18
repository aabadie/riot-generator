"""RIOT example application generator module."""

import os
import click

from .common import check_overwrite
from .application import load_and_check_application_params, render_application_source


APPLICATION_PARAMS = {
    "name": {"args": ["Example application name"], "kwargs": {}},
    "brief": {"args": ["Example application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}


def _get_output_dir(params, group, riotbase):
    """Helper function for tests.

    >>> params = {"test": {"name": "test"}}
    >>> _get_output_dir(params, "test", "/tmp")
    '/tmp/examples/test'
    """
    return os.path.join(riotbase, "examples", params[group]["name"])


def generate_example(interactive, config, riotbase):
    """Generate the code of an example application."""
    group = "example"
    params = load_and_check_application_params(group, interactive, config, riotbase,)

    output_dir = _get_output_dir(params, group, riotbase)
    check_overwrite(output_dir)

    render_application_source(params, group, output_dir)

    click.echo(
        click.style(
            f"Example '{params[group]['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
