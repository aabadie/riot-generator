"""RIOT application generator module."""

import os.path
import datetime

import click
from click import MissingParameter

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR
from .helpers import _read_config, _parse_list_option
from .helpers import _prompt_common_information, _check_common_params
from .helpers import generate_application_source


def _read_application_config(filename):
    """Read the application specific configuration file."""
    params = _read_config(filename, section='application')
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
            params[param] = _parse_list_option(params[param])
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
        value_proc=_parse_list_option)
    params['packages'] = click.prompt(
        text='Required packages (comma separated)', default='',
        value_proc=_parse_list_option)
    params['features'] = click.prompt(
        text='Required board features (comma separated)', default='',
        value_proc=_parse_list_option)

    params.update(_prompt_common_information())
    return params


def _check_application_params(params):
    application_name = params['name'].replace(' ', '_')
    params['name'] = application_name
    params['name_underline'] = '=' * len(application_name)
    params['includes'] = ''
    for module in params['modules']:
        params['includes'] += 'USEMODULE += {}\n'.format(module)
    for package in params['packages']:
        params['includes'] += 'USEPKG += {}\n'.format(package)
    for feature in params['features']:
        params['includes'] += 'FEATURES_REQUIRED += {}\n'.format(feature)


def generate_application(output_dir, config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_application_params()
    else:
        params = _read_application_config(config)
    _check_application_params(params)
    _check_common_params(params)

    params['output_dir'] = os.path.expanduser(output_dir)
    generate_application_source(params)

    click.echo(click.style('Application \'{name}\' generated in {output_dir} '
                           'with success!'.format(**params), bold=True))
    click.echo('\nTo build the application, use')
    click.echo('\n     make -C {output_dir}\n'.format(**params))
