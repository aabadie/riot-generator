"""RIOT application generator module."""

import os

import click

from .common import render_source
from .common import check_common_params, check_param, check_riotbase
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def read_board_config(filename):
    """Read the board specific configuration file."""
    params = read_config(filename)
    _params = params['board']
    if 'features' not in _params:
        _params['features'] = []
    else:
        _params['features'] = parse_list_option(_params['features'])
    return params


def prompt_board_params(params):
    """Request board specific variables."""
    _params = params['board']
    prompt_param(_params, 'name', 'Board name')
    prompt_param(
        _params, 'displayed_name',
        'Board displayed name (for doxygen documentation)')
    prompt_param(_params, 'cpu', 'CPU name')
    prompt_param(_params, 'cpu_model', 'CPU model name')
    prompt_param_list(
        _params,
        'features',
        'Features provided by this board (comma separated)'
    )


def check_board_params(params):
    _params = params['board']
    for param in ['name', 'cpu', 'cpu_model', 'displayed_name']:
        check_param(_params, param)
    _params['name'] = _params['name'].replace(' ', '_')


def generate_board(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    check_riotbase(riotbase)

    params = {
        'common': {},
        'board': {}
    }

    if config is not None:
        params = read_board_config(config)

    if interactive:
        prompt_board_params(params)
        prompt_common_params(params)

    check_board_params(params)
    check_common_params(params)

    _params = params['board']
    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    boards_dir = os.path.join(riotbase, 'boards')
    board_dir = os.path.join(boards_dir, _params['name'])
    board_include_dir = os.path.join(board_dir, 'include')

    if not os.path.exists(board_dir):
        os.makedirs(board_dir)
        os.makedirs(board_include_dir)
    elif not click.prompt('\'{name}\' board directory already exists, '
                          'overwrite (y/N)?'.format(_params['name']),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    render_source(
        params, 'board',
        [
            'board.c', 'doc.txt', 'Makefile', 'Makefile.dep',
            'Makefile.features', 'Makefile.include'
        ],
        board_dir
    )

    render_source(
        params, 'board',
        ['board.h', 'periph_conf.h'],
        board_dir, output_subdir='include'
    )

    click.echo(click.style(
        'Support for board \'{board}\' generated!'.format(
            board=_params['displayed_name']
        ),
        bold=True))
