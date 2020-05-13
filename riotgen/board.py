"""RIOT application generator module."""

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

BOARD_FILES = [
    "board.c",
    "doc.txt",
    "Makefile",
    "Makefile.dep",
    "Makefile.features",
    "Makefile.include",
]

BOARD_INCLUDE_FILES = ["board.h", "periph_conf.h"]


def generate_board(interactive, config, riotbase):
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
        params, group, BOARD_INCLUDE_FILES, output_dir, output_subdir="include",
    )

    click.echo(
        click.style(
            "Support for {group} '{board}' generated in {output_dir} with success!".format(
                group=group, board=params[group]["name"], output_dir=output_dir
            ),
            bold=True,
        )
    )
