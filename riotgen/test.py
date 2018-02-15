"""RIOT test generator module."""

import os.path
import datetime

import click
from click import MissingParameter

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR
from .helpers import _read_config, _parse_list_option
from .helpers import _prompt_common_information, _check_common_params
from .helpers import write_application_source


def _read_test_config(filename):
    """Read the test specific configuration file."""
    params = _read_config(filename, section='test')
    if 'name' not in params or not params['name']:
        raise MissingParameter(param_type='test name')
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


def _prompt_test_params():
    """Request test specific variables."""
    params = {}
    params['name'] = click.prompt(
        text='Application name (no space)')
    params['brief'] = click.prompt(
        text='Test brief description', default='')
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


def _check_test_params(params):
    test_name = params['name'].replace(' ', '_')
    params['name'] = test_name
    params['includes'] = ''
    for module in params['modules']:
        params['includes'] += 'USEMODULE += {}\n'.format(module)
    for package in params['packages']:
        params['includes'] += 'USEPKG += {}\n'.format(package)
    for feature in params['features']:
        params['includes'] += 'FEATURES_REQUIRED += {}\n'.format(feature)


def generate_test(config=None):
    # Start wizard if config is not set
    if config is None:
        params = _prompt_test_params()
    else:
        params = _read_test_config(config)
    _check_test_params(params)
    _check_common_params(params)

    tests_dir = os.path.join(os.path.expanduser(params['riotbase']), 'tests')
    test_dir = os.path.join(tests_dir, params['name'])
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    elif not click.prompt('\'{name}\' test directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    output_dir = os.path.expanduser(test_dir)
    write_application_source(output_dir, params, template_dir='test')

    click.echo(click.style('Test application \'{name}\' generated!'
                           .format(**params), bold=True))
