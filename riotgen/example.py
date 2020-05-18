"""RIOT example application generator module."""

import click

from .common import generate
from .application import APPLICATION_FILES, APPLICATION_PARAMS_LIST


APPLICATION_PARAMS = {
    "name": {"args": ["Example application name"], "kwargs": {}},
    "brief": {"args": ["Example application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}


def generate_example(interactive, config, riotbase):
    """Generate the code of an example application."""
    group = "example"
    params, output_dir = generate(
        group,
        APPLICATION_PARAMS,
        APPLICATION_PARAMS_LIST,
        APPLICATION_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="examples",
    )

    click.echo(
        click.style(
            f"Example '{params[group]['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
