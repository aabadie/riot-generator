"""RIOT application generator module."""

import os

import click

from .common import read_config_file, render_source
from .common import check_common_params, check_params, check_riotbase
from .common import prompt_common_params, prompt_params, prompt_params_list


APPLICATION_PARAMS = {
    "name": {"args": ["Application name"], "kwargs": {}},
    "brief": {"args": ["Application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features"]


def generate_application(output_dir, interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)

    params = {
        "common": {},
        "application": {"riotbase": os.path.abspath(os.path.expanduser(riotbase))},
    }

    if config is not None:
        params = read_config_file(config, "application")

    if interactive:
        prompt_params(params, APPLICATION_PARAMS, "application")
        prompt_params_list(params, "application", *APPLICATION_PARAMS_LIST)
        prompt_common_params(params)

    check_params(params, APPLICATION_PARAMS.keys() ,"application")
    check_common_params(params)

    output_dir = os.path.expanduser(output_dir)
    render_source(
        params, "application", ["main.c", "Makefile", "README.md"], output_dir
    )

    click.echo(
        click.style(
            "Application '{name}' generated in {output_dir} with success!".format(
                name=params["application"]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
    click.echo("\nTo build the application, use")
    click.echo("\n     make -C {output_dir}\n".format(output_dir=output_dir))
