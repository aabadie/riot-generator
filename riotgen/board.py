"""RIOT application generator module."""

import os.path
import datetime

import click
from click import MissingParameter

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR, generate_file
from .helpers import _read_config, _parse_list_option
from .helpers import _prompt_common_information, _check_common_params


def _read_board_config(filename):
    """Read the board specific configuration file."""
    params = _read_config(filename, section='board')
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
        params['features'] = _parse_list_option(params['features'])
    return params


def _prompt_board_params():
    """Request application specific variables."""
    params = {}
    params['name'] = click.prompt(
        text='Board name (no space)')
    params['displayed_name'] = click.prompt(
        text='Board displayed name (for doxygen documentation)')
    params['cpu'] = click.prompt(
        text='CPU name')
    params['cpu_model'] = click.prompt(
        text='CPU model name')
    params['description'] = click.prompt(
        text='Application detailed description', default='')
    params['features'] = click.prompt(
        text='Features provided by this board (comma separated)', default='',
        value_proc=_parse_list_option)

    params.update(_prompt_common_information())
    return params


def _check_board_params(params):
    board_name = params['name'].replace(' ', '_')
    params['name'] = board_name
    params['features_provided'] = ''
    for feature in sorted(params['features']):
        params['features_provided'] += \
            'FEATURES_PROVIDED += periph_{}\n'.format(feature)


def generate_board(config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_board_params()
    else:
        params = _read_board_config(config)
    _check_board_params(params)
    _check_common_params(params)

    tpl_dir = os.path.join(TEMPLATES_DIR, 'board')
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

    files = {os.path.join(tpl_dir, f_name): os.path.join(board_dir, f_name)
             for f_name in ['board.c', 'doc.txt', 'Makefile', 'Makefile.dep',
                            'Makefile.features', 'Makefile.include']}
    files.update({os.path.join(tpl_dir, f_name):
                               os.path.join(board_include_dir, f_name)
                  for f_name in ['board.h', 'periph_conf.h']})

    for file_in, file_out in files.items():
        generate_file(params, file_in, file_out)

    click.echo(click.style('Board support generated!', bold=True))
