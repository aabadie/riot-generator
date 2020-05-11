"""Common generator module."""

import os
import datetime

from jinja2 import Environment, FileSystemLoader
from click import prompt, MissingParameter

from .utils import get_usermail, get_username, parse_list_option


def check_riotbase(riotbase):
    """Check the given path is a valid RIOTBASE directory."""
    if riotbase is None or not riotbase:
        raise MissingParameter(param_type='riotbase directory')


def check_common_params(params):
    _params = params['common']
    if 'year' not in _params or not _params['year']:
        _params['year'] = datetime.datetime.now().year
    if 'author_name' not in _params or not _params['author_name']:
        _params['author_name'] = get_username()
    if 'author_email' not in _params or not _params['author_email']:
        _params['author_email'] = get_usermail()
    if 'organization' not in _params or not _params['organization']:
        _params['organization'] = get_username()
    check_param(_params, 'author_name')
    check_param(_params, 'author_email')
    check_param(_params, 'organization')


def check_param(params, param):
    if param not in params or params[param] == '':
        raise MissingParameter(param_type=param.replace('_', ' '))


def prompt_param(params, param, text, default=None, show_default=True):
    if param not in params or not params[param]:
        params[param] = prompt(
            text=text, default=default, show_default=show_default
        )


def prompt_param_list(params, param, text):
    if param not in params or not params[param]:
        params[param] = prompt(
            text=text, default='', value_proc=parse_list_option
        )


def prompt_common_params(params):
    _params = params['common']
    if 'year' not in params or not _params['year']:
        _params['year'] = datetime.datetime.now().year
    prompt_param(_params, 'author_name', 'Author name', default=get_username())
    prompt_param(
        _params, 'author_email', 'Author email', default=get_usermail())
    prompt_param(
        _params, 'organization', 'Organization', default=get_username())


def render_file(context, template_dir, source, dest):
    """Generate a file from an input template and a dict of parameters."""
    loader = FileSystemLoader(searchpath=template_dir)
    env = Environment(loader=loader,
                      trim_blocks=True,
                      lstrip_blocks=True,
                      keep_trailing_newline=True)
    env.globals.update(zip=zip)
    template = env.get_template(source)
    render = template.render(**context)
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
