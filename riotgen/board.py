"""RIOT application generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import prompt_common_information, check_common_params
from .utils import read_config, parse_list_option


def _read_board_config(filename):
    """Read the board specific configuration file."""
    params = read_config(filename, section='board')
    if 'name' not in params or not params['name']:
        raise MissingParameter(param_type='board name')
    if 'displayed_name' not in params or not params['displayed_name']:
        raise MissingParameter(param_type='board displayed name')
    if 'cpu' not in params:
        raise MissingParameter(param_type='cpu name')
    if 'cpu_model' not in params:
        raise MissingParameter(param_type='cpu model name')
    if 'description' not in params:
        params['description'] = ''
    if 'features' not in params:
        params['features'] = ''
    else:
        params['features'] = parse_list_option(params['features'])
    return params


def _prompt_board_params():
    """Request board specific variables."""
    params = {}
    params['name'] = click.prompt(
        text='Board name (no space)')
    params['displayed_name'] = click.prompt(
        text='Board displayed name (for doxygen documentation)')
    params['cpu'] = click.prompt(
        text='CPU name')
    params['cpu_model'] = click.prompt(
        text='CPU model name')
    params['features'] = click.prompt(
        text='Features provided by this board (comma separated)', default='',
        value_proc=parse_list_option)

    params.update(prompt_common_information())
    return params


def _check_board_params(params):
    board_name = params['name'].replace(' ', '_')
    params['name'] = board_name


def generate_board(config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_board_params()
    else:
        params = _read_board_config(config)
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
