"""RIOT pkg generator module."""

import os
import os.path
import datetime

import click
from click import MissingParameter

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR
from .helpers import _read_config, _parse_list_option
from .helpers import _prompt_common_information, _check_common_params
from .helpers import generate_source, generate_file


def _read_pkg_config(filename):
    """Read the pkg specific configuration file."""
    params = _read_config(filename, section='pkg')
    if 'name' not in params or not params['name']:
        raise MissingParameter(param_type='package name')
    if 'displayed_name' not in params or not params['displayed_name']:
        raise MissingParameter(param_type='board displayed name')
    if 'url' not in params or not params['url']:
        raise MissingParameter(param_type='package source url')
    if 'hash' not in params or not params['hash']:
        raise MissingParameter(param_type='package version hash')
    if 'license' not in params or not params['license']:
        raise MissingParameter(param_type='package license')
    if 'description' not in params:
        params['description'] = ''
    return params


def _prompt_pkg_params():
    """Request pkg specific variables."""
    params = {}
    params['name'] = click.prompt(text='Package name (no space)')
    params['displayed_name'] = click.prompt(
        text='Package displayed name (for doxygen documentation)')
    params['url'] = click.prompt(text='Package source url')
    params['hash'] = click.prompt(text='Package version hash')
    params['license'] = click.prompt(text='Package license')
    params['description'] = click.prompt(text='Package short description')

    params.update(_prompt_common_information())
    return params


def _check_pkg_params(params):
    test_name = params['name'].replace(' ', '_')
    params['name'] = test_name


def generate_pkg(config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_pkg_params()
    else:
        params = _read_pkg_config(config)
    _check_pkg_params(params)
    _check_common_params(params)

    pkgs_dir = os.path.join(os.path.expanduser(params['riotbase']), 'pkg')
    pkg_dir = os.path.join(pkgs_dir, params['name'])

    riotbase = os.path.abspath(os.path.expanduser(params['riotbase']))
    if os.path.abspath(os.path.curdir) == riotbase:
        params['output_dir'] = os.path.join('pkg', params['name'])
    else:
        params['output_dir'] = os.path.expanduser(pkg_dir)

    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    elif not click.prompt('\'{name}\' pkg directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    generate_source(params, 'pkg', ['doc.txt',
                                    'Makefile',
                                    'Makefile.dep',
                                    'Makefile.include'])

    makefile_pkg_in = os.path.join(TEMPLATES_DIR, 'pkg', 'Makefile.pkg')
    makefile_pkg_out = os.path.join(params['output_dir'],
                                    'Makefile.{}'.format(params['name']))
    generate_file(params, makefile_pkg_in, makefile_pkg_out)

    click.echo(click.style('Package \'{name}\' generated in '
                           '{output_dir} with success!'
                           .format(**params), bold=True))
