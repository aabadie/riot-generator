"""RIOT pkg generator module."""

import os

import click
from click import MissingParameter

from .common import render_source, render_file
from .common import check_common_params, check_param
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def _read_pkg_config(filename):
    """Read the pkg specific configuration file."""
    params = read_config(filename, section='pkg')
    for param in ['modules', 'packages', 'features']:
        params[param] = parse_list_option(params[param])
    return params


def _prompt_pkg_params(params):
    """Request pkg specific variables."""
    prompt_param(params, 'name', 'Package name')
    prompt_param(
        params, 'displayed_name',
        'Package displayed name (for doxygen documentation)')
    prompt_param(params, 'url', 'Package source url')
    prompt_param(params, 'hash', 'Package version hash')
    prompt_param(params, 'license', 'Package license')
    prompt_param(params, 'description', 'Package short description')
    prompt_param_list(
        params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        params, 'features', 'Required features (comma separated)')

    prompt_common_params(params)
    return params


def _check_pkg_params(params):
    for param in ['name', 'displayed_name', 'url', 'hash', 'license']:
        check_param(params, param)
    params['name'] = params['name'].replace(' ', '_')


def generate_pkg(interactive, config):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    params = {}
    # Start wizard if config is not set
    if config is not None:
        params = _read_pkg_config(config)

    if interactive:
        _prompt_pkg_params(params)

    _check_pkg_params(params)
    check_common_params(params)

    pkgs_dir = os.path.join(os.path.expanduser(params['riotbase']), 'pkg')
    pkg_dir = os.path.join(pkgs_dir, params['name'])

    riotbase = os.path.abspath(os.path.expanduser(params['riotbase']))
    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('pkg', params['name'])
    else:
        output_dir = os.path.expanduser(pkg_dir)

    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    elif not click.prompt('\'{name}\' pkg directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    context = {'pkg': params}
    render_source(
        context, 'pkg',
        ['doc.txt', 'Makefile', 'Makefile.dep', 'Makefile.include'],
        output_dir
    )

    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates', 'pkg'
    )
    makefile_pkg_out = os.path.join(output_dir,
                                    '{}.mk'.format(params['name']))
    render_file(context, template_dir, 'pkg.mk.j2', makefile_pkg_out)

    click.echo(click.style('Package \'{name}\' generated in '
                           '{output_dir} with success!'
                           .format(name=params['name'], output_dir=output_dir),
                           bold=True))
