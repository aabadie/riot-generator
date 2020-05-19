"""RIOT example application generator module."""

import click

from .common import check_overwrite
from .application import load_and_check_application_params, render_application_source
from .application import get_output_dir


def generate_example(interactive, config, riotbase):
    """Generate the code of an example application."""
    group = "application"
    params = load_and_check_application_params(
        group, interactive, config, riotbase, in_riot_dir="examples"
    )

    params["application"]["type"] = "example"

    output_dir = get_output_dir(params, group, riotbase, "examples")
    check_overwrite(output_dir)

    render_application_source(params, group, output_dir)

    click.echo(
        click.style(
            f"Example '{params[group]['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
