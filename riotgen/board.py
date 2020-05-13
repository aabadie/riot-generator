"""RIOT application generator module."""

import os

import click

from .common import render_source, read_config_file
from .common import check_common_params, check_params, check_riotbase
from .common import prompt_common_params, prompt_params, prompt_params_list


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


def generate_board(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)

    params = {"common": {}, "board": {}}

    if config is not None:
        params = read_config_file(config, "board")

    if interactive:
        prompt_params(params, BOARD_PARAMS, "board")
        prompt_params_list(params, "board", *BOARD_PARAMS_LIST)
        prompt_common_params(params)

    check_params(params, BOARD_PARAMS.keys() ,"board")
    check_common_params(params)

    board_params = params["board"]
    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    boards_dir = os.path.join(riotbase, "boards")
    board_dir = os.path.join(boards_dir, board_params["name"])

    if os.path.exists(board_dir) and not click.prompt(
        "'{name}' board directory already exists, "
        "overwrite (y/N)?".format(board_params["name"]),
        default=False,
        show_default=False,
    ):
        click.echo("Abort")
        return

    render_source(
        params,
        "board",
        [
            "board.c",
            "doc.txt",
            "Makefile",
            "Makefile.dep",
            "Makefile.features",
            "Makefile.include",
        ],
        board_dir,
    )

    render_source(
        params,
        "board",
        ["board.h", "periph_conf.h"],
        board_dir,
        output_subdir="include",
    )

    click.echo(
        click.style(
            "Support for board '{board}' generated!".format(
                board=board_params["displayed_name"]
            ),
            bold=True,
        )
    )
