"""RIOT test generator module."""

import os

import click

from .common import render_source
from .common import check_common_params, check_param, check_riotbase
from .common import prompt_common_params, prompt_param, prompt_param_list
from .utils import read_config, parse_list_option


def read_test_config(filename):
    """Read the test specific configuration file."""
    params = read_config(filename)
    _params = params['test']
    for param in ['modules', 'packages', 'features']:
        _params[param] = parse_list_option(_params[param])
    return params


def prompt_test_params(params):
    """Request test specific variables."""
    _params = params['test']
    prompt_param(_params, 'name', 'Test name')
    prompt_param(_params, 'brief', 'Test brief description')
    prompt_param(_params, 'board', 'Target board', default='native')
    prompt_param_list(
        _params, 'modules', 'Required modules (comma separated)')
    prompt_param_list(
        _params, 'packages', 'Required packages (comma separated)')
    prompt_param_list(
        _params, 'features', 'Required features (comma separated)')
    prompt_param(
        _params, 'use_testrunner', 'Add testrunner script (y/N)?',
        default=False, show_default=False)


def check_test_params(params):
    _params = params['test']
    for param in ['name', 'board', 'brief', 'use_testrunner']:
        check_param(_params, param)
    _params['name'] = _params['name'].replace(' ', '_')


def generate_test(interactive, config, riotbase):
    if not interactive and config is None:
        raise click.MissingParameter(
            param_type='--interactive and/or --config options'
        )

    check_riotbase(riotbase)

    params = {
        'common': {},
        'test': {}
    }

    if config is not None:
        params = read_test_config(config)

    if interactive:
        prompt_test_params(params)
        prompt_common_params(params)

    check_test_params(params)
    check_common_params(params)
    _params = params['test']

    riotbase = os.path.abspath(os.path.expanduser(riotbase))
    tests_dir = os.path.join(riotbase, 'tests')
    test_dir = os.path.join(tests_dir, _params['name'])

    if os.path.abspath(os.path.curdir) == riotbase:
        output_dir = os.path.join('tests', _params['name'])
    else:
        output_dir = os.path.expanduser(test_dir)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    elif not click.prompt('\'{name}\' test directory already exists, '
                          'overwrite (y/N)?'.format(name=_params['name']),
                          default=False, show_default=False):
        click.echo('Abort')
        return

    if 'use_testrunner' in _params and _params['use_testrunner'] == "True":
        testrunner_dir = os.path.join(test_dir, 'tests')
        if not os.path.exists(testrunner_dir):
            os.makedirs(testrunner_dir)
        render_source(params, 'test', ['01-run.py'], testrunner_dir)
        os.chmod(os.path.join(testrunner_dir, '01-run.py'), 0o755)

    files = ['main.c', 'Makefile', 'README.md']
    render_source(params, 'test', files, output_dir)

    click.echo(click.style(
        'Test application \'{name}\' generated in {output_dir} with success!'
        .format(name=_params['name'], output_dir=output_dir), bold=True))
