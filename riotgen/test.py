"""RIOT test generator module."""

import os

import click
from click import MissingParameter

from .common import render_source
from .common import check_common_params, check_param
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def _read_test_config(filename):
    """Read the test specific configuration file."""
    params = read_config(filename, section='test')
    for param in ['modules', 'packages', 'features']:
        params[param] = parse_list_option(params[param])
    return params


def _prompt_test_params(params):
    """Request test specific variables."""
    prompt_param(params, 'name', 'Test name')
    prompt_param(params, 'brief', 'Test brief description')
    prompt_param(params, 'board', 'Target board', default='native')
    prompt_param_list(
        params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        params, 'features', 'Required features (comma separated)')
    prompt_param(
        params, 'use_testrunner', 'Use testrunner script (y/N)?',
        default=False, show_default=False)

    prompt_common_params(params)
    return params


def _check_test_params(params):
    for param in ['name', 'board', 'brief', 'use_testrunner']:
        check_param(params, param)
    params['name'] = params['name'].replace(' ', '_')


def generate_test(interactive, config):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    params = {}
    # Start wizard if config is not set
    if config is not None:
        params = _read_test_config(config)

    if interactive:
        _prompt_test_params(params)

    _check_test_params(params)
    check_common_params(params)

    tests_dir = os.path.join(os.path.expanduser(params['riotbase']), 'tests')
    test_dir = os.path.join(tests_dir, params['name'])

    riotbase = os.path.abspath(os.path.expanduser(params['riotbase']))
    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('tests', params['name'])
    else:
        output_dir = os.path.expanduser(test_dir)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    elif not click.prompt('\'{name}\' test directory already exists, '
                          'overwrite (y/N)?'.format(**params),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    if 'use_testrunner' in params and params['use_testrunner']:
        testrunner_dir = os.path.join(test_dir, 'tests')
        if not os.path.exists(testrunner_dir):
            os.makedirs(testrunner_dir)
        render_source({'test': params}, 'test', ['01-run.py'], testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, '01-run.py'), 0o755)

    files = ['main.c', 'Makefile', 'README.md']
    render_source({'test': params}, 'test', files, output_dir)

    click.echo(click.style('Test application \'{name}\' generated in '
                           '{output_dir} with success!'
                           .format(name=params['name'], output_dir=output_dir),
                           bold=True))
