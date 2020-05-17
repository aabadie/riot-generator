"""RIOT application generator module."""

import os
import click

from .common import render_source, generate


MODULE_PARAMS = {
    "name": {"args": ["Module name"], "kwargs": {}},
    "displayed_name": {"args": ["Module Doxygen name"], "kwargs": {},},
    "brief": {"args": ["Brief doxygen description"], "kwargs": {}},
}

MODULE_FILES = {
    "module.c": "{name}.c",
    "Makefile": None,
}

MODULE_INCLUDE_FILES = {"module.h": "{name}.h"}


def generate_module(interactive, config, riotbase):
    """Generate the code of a module."""
    group = "module"
    params, output_dir = generate(
        group,
        MODULE_PARAMS,
        [],
        MODULE_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="sys",
    )

    render_source(
        params, group, MODULE_INCLUDE_FILES, os.path.join(riotbase, "sys", "include"),
    )

    click.echo(
        click.style(
            "Module '{board}' generated in {output_dir} with success!".format(
                board=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
