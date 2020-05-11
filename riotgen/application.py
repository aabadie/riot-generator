"""RIOT application generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import check_common_params, check_param
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def _read_application_config(filename):
    """Read the application specific configuration file."""
    params = read_config(filename, section='application')
    for param in ['modules', 'packages', 'features']:
        params[param] = parse_list_option(params[param])
    return params


def _prompt_application_params(params):
    """Request application specific variables."""
    prompt_param(params, 'name', 'Application name')
    prompt_param(params, 'brief', 'Application brief description')
    prompt_param(params, 'board', 'Target board', default='native')
    prompt_param_list(
        params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        params, 'features', 'Required features (comma separated)')

    prompt_common_params(params)
    return params


def _check_application_params(params):
    for param in ['name', 'board', 'brief']:
        check_param(params, param)
    params['name'] = params['name'].replace(' ', '_')


def generate_application(output_dir, interactive, config):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    params = {}
    # Start wizard if config is not set
    if config is not None:
        params = _read_application_config(config)

    if interactive:
        _prompt_application_params(params)

    _check_application_params(params)
    check_common_params(params)

    output_dir = os.path.expanduser(output_dir)
    render_source(
        {'application': params}, 'application',
        ['main.c', 'Makefile', 'README.md'],
        output_dir
    )

    click.echo(click.style(
        'Application \'{name}\' generated in {output_dir} with success!'
        .format(name=params['name'], output_dir=output_dir),
        bold=True
    ))
    click.echo('\nTo build the application, use')
    click.echo('\n     make -C {output_dir}\n'.format(output_dir=output_dir))
