"""RIOT application generator module."""

import os
import click

from .common import render_source, generate


DRIVER_PARAMS = {
    "name": {"args": ["Driver name"], "kwargs": {}},
    "displayed_name": {"args": ["Driver Doxygen group name"], "kwargs": {},},
    "brief": {"args": ["Brief doxygen description"], "kwargs": {}},
    "ingroup": {"args": ["Parent driver Doxygen group"], "kwargs": {}},
}

DRIVER_FILES = {
    "driver.c": "{name}.c",
    "Makefile": None,
}

DRIVER_INCLUDE_FILES = {"driver.h": "{name}.h"}

DRIVER_INTERNAL_INCLUDE_FILES = {
    "driver_constants.h": "{name}_constants.h",
    "driver_params.h": "{name}_params.h",
}


def generate_driver(interactive, config, riotbase):
    """Generate the code for a driver module."""
    group = "driver"
    params, output_dir = generate(
        group,
        DRIVER_PARAMS,
        [],
        DRIVER_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="drivers",
    )

    render_source(
        params,
        group,
        DRIVER_INCLUDE_FILES,
        os.path.join(riotbase, "drivers", "include"),
    )

    render_source(
        params,
        group,
        DRIVER_INTERNAL_INCLUDE_FILES,
        os.path.join(output_dir, "include"),
    )

    click.echo(
        click.style(
            "Driver '{board}' generated in {output_dir} with success!".format(
                board=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
