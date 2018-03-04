"""RIOT test generator module."""

import os
import os.path
import datetime

import click
from click import MissingParameter

from .helpers import _get_usermail, _get_username
from .helpers import TEMPLATES_DIR
from .helpers import _read_config, _parse_list_option
from .helpers import _prompt_common_information, _check_common_params
from .helpers import generate_application_source, generate_file


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
    params['use_testrunner'] = click.prompt(
        text='Use testrunner script (y/N)?', default=False, show_default=False)

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

    riotbase = os.path.abspath(os.path.expanduser(params['riotbase']))
    if os.path.abspath(os.path.curdir) == riotbase:
        params['output_dir'] = os.path.join('tests', params['name'])
    else:
        params['output_dir'] = os.path.expanduser(test_dir)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    elif not click.prompt('\'{name}\' test directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    params['testrunner'] = ''
    if 'use_testrunner' in params and params['use_testrunner']:
        testrunner_dir = os.path.join(test_dir, 'tests')
        tpl_dir = os.path.join(TEMPLATES_DIR, 'test')
        if not os.path.exists(testrunner_dir):
            os.makedirs(testrunner_dir)
        script_in = os.path.join(tpl_dir, '01-run.py')
        script_out = os.path.join(testrunner_dir, '01-run.py')
        generate_file(params, script_in, script_out)
        os.chmod(script_out, 0o755)
        params['testrunner'] = "\ntest:\n\ttests/01-run.py\n"

    generate_application_source(params, template_dir='test')

    click.echo(click.style('Test application \'{name}\' generated in '
                           '{output_dir} with success!'
                           .format(**params), bold=True))
