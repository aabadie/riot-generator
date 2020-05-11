"""RIOT application generator module."""

import os

import click

from .common import render_source
from .common import check_common_params, check_param, check_riotbase
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def read_application_config(filename):
    """Read the application specific configuration file."""
    params = read_config(filename)
    _params = params['application']
    for param in ['modules', 'packages', 'features']:
        if param not in _params:
            _params[param] = []
        else:
            _params[param] = parse_list_option(_params[param])
    return params


def prompt_application_params(params):
    """Request application specific variables."""
    _params = params['application']
    prompt_param(_params, 'name', 'Application name')
    prompt_param(_params, 'brief', 'Application brief description')
    prompt_param(_params, 'board', 'Target board', default='native')
    prompt_param_list(
        _params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        _params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        _params, 'features', 'Required features (comma separated)')


def check_application_params(params):
    _params = params['application']
    for param in ['name', 'board', 'brief']:
        check_param(_params, param)
    _params['name'] = _params['name'].replace(' ', '_')


def generate_application(output_dir, interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    check_riotbase(riotbase)

    params = {
        'common': {},
        'application': {
            'riotbase': os.path.abspath(os.path.expanduser(riotbase))
        }
    }

    if config is not None:
        params = read_application_config(config)

    if interactive:
        prompt_application_params(params)
        prompt_common_params(params)

    check_application_params(params)
    check_common_params(params)

    output_dir = os.path.expanduser(output_dir)
    render_source(
        params,
        'application',
        ['main.c', 'Makefile', 'README.md'],
        output_dir
    )

    click.echo(click.style(
        'Application \'{name}\' generated in {output_dir} with success!'
        .format(name=params['application']['name'], output_dir=output_dir),
        bold=True
    ))
    click.echo('\nTo build the application, use')
    click.echo('\n     make -C {output_dir}\n'.format(output_dir=output_dir))
