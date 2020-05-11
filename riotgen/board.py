"""RIOT application generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import check_common_params, check_param
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def _read_board_config(filename):
    """Read the board specific configuration file."""
    params = read_config(filename, section='board')
    params['features'] = parse_list_option(params['features'])
    return params


def _prompt_board_params(params):
    """Request board specific variables."""
    prompt_param(params, 'name', 'Board name')
    prompt_param(
        params, 'displayed_name',
        'Board displayed name (for doxygen documentation)')
    prompt_param(params, 'cpu', 'CPU name')
    prompt_param(params, 'cpu_model', 'CPU model name')
    prompt_param_list(
        params,
        'features',
        'Features provided by this board (comma separated)'
    )

    prompt_common_params(params)
    return params


def _check_board_params(params):
    for param in ['name', 'cpu', 'cpu_model', 'displayed_name']:
        check_param(params, param)
    params['name'] = params['name'].replace(' ', '_')


def generate_board(interactive, config):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    params = {}
    # Start wizard if config is not set
    if config is not None:
        params = _read_board_config(config)

    if interactive:
        _prompt_board_params(params)

    _check_board_params(params)
    check_common_params(params)

    boards_dir = os.path.join(os.path.expanduser(params['riotbase']), 'boards')
    board_dir = os.path.join(boards_dir, params['name'])
    board_include_dir = os.path.join(board_dir, 'include')
    if not os.path.exists(board_dir):
        os.makedirs(board_dir)
        os.makedirs(board_include_dir)
    elif not click.prompt('\'{name}\' board directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    context = {'board': params}
    render_source(
        context, 'board',
        [
            'board.c', 'doc.txt', 'Makefile', 'Makefile.dep',
            'Makefile.features', 'Makefile.include'
        ],
        board_dir
    )

    render_source(
        context, 'board',
        ['board.h', 'periph_conf.h'],
        board_dir, output_subdir='include'
    )

    click.echo(click.style(
        'Support for board \'{board}\' generated!'.format(
            board=params['displayed_name']
        ),
        bold=True))
