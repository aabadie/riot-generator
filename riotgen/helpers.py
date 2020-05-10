"""Internal helper functions"""

import os
import os.path
import datetime
from configparser import ConfigParser
from subprocess import check_output

import click
from click import MissingParameter, BadParameter

from jinja2 import Environment, FileSystemLoader, select_autoescape


def _parse_list_option(opt):
    """Split list element separated by a comma."""
    return sorted(opt.split(','))


def _get_git_config(config):
    try:
        config = check_output(
            ['git', 'config', '--get', config]).decode()[:-1]
    except:
        config = ''

    return config

def _get_username():
    return _get_git_config('user.name')


def _get_usermail():
    return _get_git_config('user.email')


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


def render_file(context, template_dir, source, dest):
    """Generate a file from an input template and a dict of parameters."""
    loader = FileSystemLoader(searchpath=template_dir)
    env = Environment(loader=loader,
                      trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=True)
    env.globals.update(zip=zip)
    template = env.get_template(source)
    render = template.render(context=context)
    with open(dest, 'w') as f_dest:
        f_dest.write(render)


def render_source(context, template_dir, input_files, output_dir,
                  output_subdir=""):
    """Generate a list of files given from an input template directory."""
    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates', template_dir
    )
    if output_subdir:
        output_dir = os.path.join(output_dir, output_subdir)

    files = {
        filename + '.j2': os.path.join(output_dir, filename)
        for filename in input_files
    }

    for source, dest in files.items():
        render_file(context, template_dir, source, dest)
