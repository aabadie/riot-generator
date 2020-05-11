"""RIOT example application generator module."""

import os

import click

from .common import render_source
from .common import check_common_params, check_param, check_riotbase
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def read_example_config(filename):
    """Read the application specific configuration file."""
    params = read_config(filename)
    _params = params['example']
    for param in ['modules', 'packages', 'features']:
        _params[param] = parse_list_option(_params[param])
    return params


def prompt_example_params(params):
    """Request application specific variables."""
    _params = params['example']
    prompt_param(_params, 'name', 'Example application name')
    prompt_param(_params, 'brief', 'Example application brief description')
    prompt_param(_params, 'board', 'Target board', default='native')
    prompt_param_list(
        _params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        _params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        _params, 'features', 'Required features (comma separated)')


def check_example_params(params):
    _params = params['example']
    for param in ['name', 'board', 'brief']:
        check_param(_params, param)
    _params['name'] = _params['name'].replace(' ', '_')


def generate_example(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    check_riotbase(riotbase)

    params = {
        'common': {},
        'example': {}
    }

    if config is not None:
        params = read_example_config(config)

    if interactive:
        prompt_example_params(params)
        prompt_common_params(params)

    check_example_params(params)
    check_common_params(params)

    _params = params['example']
    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    examples_dir = os.path.join(riotbase, 'examples')
    example_dir = os.path.join(examples_dir, _params['name'])

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('examples', _params['name'])
    else:
        output_dir = os.path.expanduser(example_dir)

    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
    elif not click.prompt('\'{name}\' example directory already exists, '
                          'overwrite (y/N)?'.format(name=_params['name']),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    render_source(
        params, 'example',
        ['main.c', 'Makefile', 'README.md'],
        output_dir
    )

    click.echo(click.style(
        'Example \'{name}\' generated in {output_dir} with success!'
        .format(name=_params['name'], output_dir=output_dir),
        bold=True
    ))
