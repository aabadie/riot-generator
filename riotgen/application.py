"""RIOT application generator module."""

import os
import click

from .common import load_and_check_params, render_source


APPLICATION_PARAMS = {
    "name": {"args": ["Application name"], "kwargs": {}},
    "brief": {"args": ["Application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}

TESTRUNNER_PARAMS = {
    "use_testrunner": {
        "args": ["Add testrunner script (y/N)"],
        "kwargs": {"default": False, "show_default": False},
    },
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features_required"]

APPLICATION_FILES = {filename: None for filename in ["main.c", "Makefile", "README.md"]}


def get_output_dir(params, group, riotbase, in_riot_dir):
    """Helper function for tests."""
    return os.path.join(riotbase, in_riot_dir, params[group]["name"])


def load_and_check_application_params(
    group, interactive, config, riotbase, in_riot_dir=None, testrunner=False
):
    """Load, prompt and check application configuration parameters."""
    params = APPLICATION_PARAMS.copy()
    if testrunner is True:
        params.update(TESTRUNNER_PARAMS)

    return load_and_check_params(
        group,
        params,
        APPLICATION_PARAMS_LIST,
        interactive,
        config,
        riotbase,
        in_riot_dir,
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
