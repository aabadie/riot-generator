"""RIOT application generator module."""

import os
import click

from .common import render_source, generate


BOARD_PARAMS = {
    "name": {"args": ["Board name"], "kwargs": {}},
    "displayed_name": {
        "args": ["Board displayed name (for doxygen documentation)"],
        "kwargs": {},
    },
    "cpu": {"args": ["CPU name"], "kwargs": {}},
    "cpu_model": {"args": ["CPU model name"], "kwargs": {}},
}

BOARD_PARAMS_LIST = ["features"]

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
    params, output_dir = generate(
        group,
        BOARD_PARAMS,
        BOARD_PARAMS_LIST,
        BOARD_FILES,
        interactive,
        config,
        riotbase,
        in_riot_dir="boards",
    )

    render_source(
        params, group, BOARD_INCLUDE_FILES, os.path.join(output_dir, "include"),
    )

    click.echo(
        click.style(
            "Support for {group} '{board}' generated in {output_dir} with success!".format(
                group=group, board=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
