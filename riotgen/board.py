"""RIOT application generator module."""

import os
import click

from .common import load_and_check_params, check_overwrite, render_source, load_license


BOARD_PARAMS = {
    "name": {"args": ["Board name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Board displayed name (for doxygen documentation)"],
        "kwargs": {},
    },
    "cpu": {"args": ["CPU name"], "kwargs": {}},
    "cpu_model": {"args": ["CPU model name"], "kwargs": {}},
}

BOARD_PARAMS_LIST = ["features_provided"]

BOARD_FILES = {
    filename: None
    for filename in [
        "board.c",
        "doc.txt",
        "Makefile",
        "Makefile.dep",
        "Makefile.features",
        "Makefile.include",
    ]
}

BOARD_INCLUDE_FILES = {filename: None for filename in ["board.h", "periph_conf.h"]}


def generate_board(interactive, config, riotbase):
    """Generate the code for a board support."""
    group = "board"
    params = load_and_check_params(
        group,
        BOARD_PARAMS,
        BOARD_PARAMS_LIST,
        interactive,
        config,
        riotbase,
        "boards",
    )

    output_dir = os.path.join(riotbase, "boards", params[group]["name"])
    check_overwrite(output_dir)

    render_source(params, group, BOARD_FILES, output_dir)
    render_source(
        params,
        group,
        BOARD_INCLUDE_FILES,
        os.path.join(output_dir, "include"),
    )

    # Generate the Kconfig file separately because of the different license
    # format
    load_license(params, "# ")
    render_source(params, group, {"Kconfig": None}, output_dir)

    click.echo(
        click.style(
            f"Support for {group} '{params[group]['name']}' generated in {output_dir} with success!",
            bold=True,
        )
    )
