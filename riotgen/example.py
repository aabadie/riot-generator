"""RIOT example application generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import check_common_params, check_param
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def _read_example_config(filename):
    """Read the application specific configuration file."""
    params = read_config(filename, section='example')
    for param in ['modules', 'packages', 'features']:
        params[param] = parse_list_option(params[param])
    return params


def _prompt_example_params(params):
    """Request application specific variables."""
    prompt_param(params, 'name', 'Example application name')
    prompt_param(params, 'brief', 'Example application brief description')
    prompt_param(params, 'board', 'Target board', default='native')
    prompt_param_list(
        params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        params, 'features', 'Required features (comma separated)')

    prompt_common_params(params)
    return params


def _check_example_params(params):
    for param in ['name', 'board', 'brief']:
        check_param(params, param)
    params['name'] = params['name'].replace(' ', '_')


def generate_example(interactive, config):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    params = {}
    # Start wizard if config is not set
    if config is not None:
        params = _read_example_config(config)

    if interactive:
        _prompt_example_params(params)

    _check_example_params(params)
    check_common_params(params)

    examples_dir = os.path.join(
        os.path.expanduser(params['riotbase']), 'examples'
    )
    example_dir = os.path.join(examples_dir, params['name'])
    riotbase = os.path.abspath(os.path.expanduser(params['riotbase']))
    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('examples', params['name'])
    else:
        output_dir = os.path.expanduser(example_dir)

    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
    elif not click.prompt('\'{name}\' example directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    render_source(
        {'example': params}, 'example',
        ['main.c', 'Makefile', 'README.md'],
        output_dir
    )

    click.echo(click.style(
        'Example \'{name}\' generated in {output_dir} with success!'
        .format(name=params['name'], output_dir=output_dir),
        bold=True
    ))
