"""RIOT pkg generator module."""

import os

import click

from .common import render_source, render_file
from .common import check_param, prompt_param, prompt_param_list
from .common import check_riotbase
from .utils import read_config, parse_list_option


def read_pkg_config(filename):
    """Read the pkg specific configuration file."""
    params = read_config(filename)
    _params = params['pkg']
    for param in ['modules', 'packages', 'features']:
        _params[param] = parse_list_option(_params[param])
    return params


def prompt_pkg_params(params):
    """Request pkg specific variables."""
    _params = params['pkg']
    prompt_param(_params, 'name', 'Package name')
    prompt_param(
        _params, 'displayed_name',
        'Package displayed name (for doxygen documentation)')
    prompt_param(_params, 'url', 'Package source url')
    prompt_param(_params, 'hash', 'Package version hash')
    prompt_param(_params, 'license', 'Package license')
    prompt_param(_params, 'description', 'Package short description')
    prompt_param_list(
        _params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        _params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        _params, 'features', 'Required features (comma separated)')


def check_pkg_params(params):
    _params = params['pkg']
    for param in ['name', 'displayed_name', 'url', 'hash', 'license']:
        check_param(_params, param)
    _params['name'] = _params['name'].replace(' ', '_')


def generate_pkg(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    check_riotbase(riotbase)

    params = {
        'pkg': {}
    }

    if config is not None:
        params = read_pkg_config(config)

    if interactive:
        prompt_pkg_params(params)

    check_pkg_params(params)

    _params = params['pkg']

    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    pkgs_dir = os.path.join(riotbase, 'pkg')
    pkg_dir = os.path.join(pkgs_dir, _params['name'])

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('pkg', _params['name'])
    else:
        output_dir = os.path.expanduser(pkg_dir)

    if not os.path.exists(pkg_dir):
        os.makedirs(pkg_dir)
    elif not click.prompt('\'{name}\' pkg directory already exists, '
                          'overwrite (y/N)?'.format(_params['name']),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    render_source(
        params, 'pkg',
        ['doc.txt', 'Makefile', 'Makefile.dep', 'Makefile.include'],
        output_dir
    )

    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates', 'pkg'
    )
    makefile_pkg_out = os.path.join(output_dir,
                                    '{}.mk'.format(_params['name']))
    render_file(params, template_dir, 'pkg.mk.j2', makefile_pkg_out)

    click.echo(click.style(
        'Package \'{name}\' generated in {output_dir} with success!'
        .format(name=_params['name'], output_dir=output_dir), bold=True))
