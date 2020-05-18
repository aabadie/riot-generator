"""RIOT application generator module."""

import click

from .common import load_and_check_params, render_source


APPLICATION_PARAMS = {
    "name": {"args": ["Application name"], "kwargs": {}},
    "brief": {"args": ["Application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features_required"]

APPLICATION_FILES = {filename: None for filename in ["main.c", "Makefile", "README.md"]}


def load_and_check_application_params(group, interactive, config, riotbase):
    """Load, prompt and check application configuration parameters."""
    return load_and_check_params(
        group,
        APPLICATION_PARAMS,
        APPLICATION_PARAMS_LIST,
        interactive,
        config,
        riotbase,
    )


def render_application_source(params, group, output_dir):
    """Render an application source code."""
    render_source(params, group, APPLICATION_FILES, output_dir)


def generate_application(output_dir, interactive, config, riotbase):
    """Generate the code of an application."""
    group = "application"
    params = load_and_check_application_params(group, interactive, config, riotbase)
    render_application_source(params, group, output_dir)

    click.echo(
        click.style(
            f"Application '{params['application']['name']}' generated "
            f"in {output_dir} with success!",
            bold=True,
        )
    )
    click.echo("\nTo build the application, use")
    click.echo(f"\n     make -C {output_dir}\n")
