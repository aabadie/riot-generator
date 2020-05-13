"""RIOT example application generator module."""

import os

import click

from .common import render_source, read_config_file
from .common import check_common_params, check_params, check_riotbase
from .common import prompt_common_params, prompt_params, prompt_params_list


APPLICATION_PARAMS = {
    "name": {"args": ["Example application name"], "kwargs": {}},
    "brief": {"args": ["Example application brief description"], "kwargs": {}},
    "board": {"args": ["Target board"], "kwargs": {"default": "native"}},
}

APPLICATION_PARAMS_LIST = ["modules", "packages", "features"]


def generate_example(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)

    params = {"common": {}, "example": {}}

    if config is not None:
        params = read_config_file(config, "example")

    if interactive:
        prompt_params(params, APPLICATION_PARAMS, "example")
        prompt_params_list(params, "example", *APPLICATION_PARAMS_LIST)
        prompt_common_params(params)

    check_params(params, APPLICATION_PARAMS.keys() ,"example")
    check_common_params(params)

    example_params = params["example"]
    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    examples_dir = os.path.join(riotbase, "examples")
    example_dir = os.path.join(examples_dir, example_params["name"])

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join("examples", example_params["name"])
    else:
        output_dir = os.path.expanduser(example_dir)

    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
    elif not click.prompt(
        "'{name}' example directory already exists, "
        "overwrite (y/N)?".format(name=example_params["name"]),
        default=False,
        show_default=False,
    ):
        click.echo("Abort")
        return

    render_source(params, "example", ["main.c", "Makefile", "README.md"], output_dir)

    click.echo(
        click.style(
            "Example '{name}' generated in {output_dir} with success!".format(
                name=example_params["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
