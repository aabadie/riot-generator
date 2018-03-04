"""Internal helper functions"""

import os
import os.path
import datetime
from configparser import ConfigParser
from subprocess import check_output

import click
from click import MissingParameter, BadParameter

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(PKG_DIR, 'templates')


def _parse_list_option(opt):
    """Split list element separated by a comma."""
    return opt.split(',')


def _get_username():
    try:
        name = check_output(
            ['git', 'config', '--get', 'user.name']).decode()[:-1]
    except:
        name = ''

    return name


def _get_usermail():
    try:
        email = check_output(
            ['git', 'config', '--get', 'user.email']).decode()[:-1]
    except:
        email = ''

    return email


def _check_riotbase(path, from_prompt=True):
    """Check the given path is a valid RIOTBASE directory."""
    missing = False
    if not path:
        missing = True

    coc = os.path.join(os.path.expanduser(path), 'CODE_OF_CONDUCT.md')
    if os.path.isfile(coc):
        first_line = open(coc, 'r').readline()[:-1]
        if first_line == 'RIOT-OS Code of Conduct':
            return os.path.expanduser(path)
    error_message = 'RIOT base directory'
    if not missing:
        raise BadParameter('{} (\'{}\')'.format(error_message,
                                                path.split(' ')[0]))
    elif from_prompt:
        raise MissingParameter(error_message)
    else:
        raise MissingParameter(param_type=error_message)


def _check_common_params(params):
    if 'year' not in params:
        params['year'] = datetime.datetime.now().year
    if 'author_name' not in params:
        params['author_name'] = _get_username()
    if 'author_email' not in params:
        params['author_email'] = _get_usermail()
    if 'organization' not in params:
        params['organization'] = _get_username()
    if 'riotbase' not in params:
        params['riotbase'] = ''
    params['riotbase'] = _check_riotbase(params['riotbase'], from_prompt=False)


def _prompt_common_information():
    params = {}
    params['year'] = datetime.datetime.now().year
    params['author_name'] = click.prompt(
        text='Author name', default=_get_username())
    params['author_email'] = click.prompt(
        text='Author email', default=_get_usermail())
    params['organization'] = click.prompt(
        text='Organization', default=_get_username())

    riotbase = os.getenv('RIOTBASE')
    if riotbase is None:
        params['riotbase'] = click.prompt(
            text='RIOT base directory', value_proc=_check_riotbase)
    else:
        params['riotbase'] = _check_riotbase(riotbase, from_prompt=False)
    return params


def _read_config(filename, section=None):
    parser = ConfigParser()
    parser.readfp(filename)
    config = dict(parser.items('common'))
    if section is not None:
        config.update(dict(parser.items(section)))
    return config


def generate_file(params, template, out):
    """Generate a file from an input template and a dict of parameters."""
    with open(template, 'r') as f_in:
        with open(out, 'w') as f_out:
            f_out.write(f_in.read().format(**params))


def generate_source(params, template_dir, input_files):
    """Generate a list of files given from an input template directory."""
    tpl_dir = os.path.join(TEMPLATES_DIR, template_dir)
    output_dir = params['output_dir']
    files = {os.path.join(tpl_dir, f_name): os.path.join(output_dir, f_name)
             for f_name in input_files}

    for file_in, file_out in files.items():
        generate_file(params, file_in, file_out)


def generate_application_source(params, template_dir='application'):
    """Generate source files of an application."""
    generate_source(params, template_dir, ['main.c', 'Makefile', 'README.md'])
