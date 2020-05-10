"""RIOT application generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import prompt_common_information, check_common_params
from .utils import read_config, parse_list_option


def _read_application_config(filename):
    """Read the application specific configuration file."""
    params = read_config(filename, section='application')
    if 'name' not in params or not params['name']:
        raise MissingParameter(param_type='application name')
    if 'brief' not in params:
        params['brief'] = ''
    if 'board' not in params:
        params['board'] = 'native'
    else:
        params['board'] = params['board']
    for param in ['modules', 'packages', 'features']:
        if param not in params:
            params[param] = ''
        else:
            params[param] = parse_list_option(params[param])
    return params


def _prompt_application_params():
    """Request application specific variables."""
    params = {}
    params['name'] = click.prompt(
        text='Application name (no space)')
    params['brief'] = click.prompt(
        text='Application brief description', default='')
    params['board'] = click.prompt(text='Target board', default='native')
    params['modules'] = click.prompt(
        text='Required modules (comma separated)', default='',
        value_proc=parse_list_option)
    params['packages'] = click.prompt(
        text='Required packages (comma separated)', default='',
        value_proc=parse_list_option)
    params['features'] = click.prompt(
        text='Required board features (comma separated)', default='',
        value_proc=parse_list_option)

    params.update(prompt_common_information())
    return params


def _check_application_params(params):
    application_name = params['name'].replace(' ', '_')
    params['name'] = application_name


def generate_application(output_dir, config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_application_params()
    else:
        params = _read_application_config(config)
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
