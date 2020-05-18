"""RIOT application generator module."""

import click

from .common import generate


APPLICATION_PARAMS = {
    "name": {"args": ["Application name"], "kwargs": {}},
    "brief": {"args": ["Application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features_required"]

APPLICATION_FILES = {filename: None for filename in ["main.c", "Makefile", "README.md"]}


def generate_application(output_dir, interactive, config, riotbase):
    """Generate the code of an application."""
    params, _ = generate(
        "application",
        APPLICATION_PARAMS,
        APPLICATION_PARAMS_LIST,
        APPLICATION_FILES,
        interactive,
        config,
        riotbase,
        output_dir=output_dir,
    )

    name = params["application"]["name"]

    click.echo(
        click.style(
            f"Application '{params['application']['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
    click.echo("\nTo build the application, use")
    click.echo(f"\n     make -C {output_dir}\n")
