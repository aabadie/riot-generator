"""Common generator module."""

import os
import datetime

from configparser import ConfigParser

from jinja2 import Environment, FileSystemLoader
from click import prompt, MissingParameter, BadParameter

from .utils import get_usermail, get_username, parse_list_option


def read_config_file(config_file, *command_args):
    """Read a configuration file and return the content as a dict."""
    parser = ConfigParser()
    parser.read_file(config_file)
    params = parser._sections
    for command in command_args:
        if command not in params:
            continue
        _params = params[command]
        for param in ["modules", "packages", "features"]:
            if param not in _params:
                _params[param] = []
            else:
                _params[param] = parse_list_option(_params[param])
    return params


def check_riotbase(riotbase):
    """Check the given path is a valid RIOTBASE directory."""
    if riotbase is None or not riotbase:
        raise MissingParameter(param_type="riotbase directory")


def _check_param(params, param):
    if param not in params or params[param] == "":
        raise MissingParameter(param_type=param.replace("_", " "))


def check_common_params(params):
    _params = params["common"]
    if "year" not in _params or not _params["year"]:
        _params["year"] = datetime.datetime.now().year
    if "author_name" not in _params or not _params["author_name"]:
        _params["author_name"] = get_username()
    if "author_email" not in _params or not _params["author_email"]:
        _params["author_email"] = get_usermail()
    if "organization" not in _params or not _params["organization"]:
        _params["organization"] = get_username()
    for param_name in ("author_name", "author_email", "organization"):
        _check_param(_params, param_name)


def check_params(params, param_names, group):
    if group not in params:
        raise BadParameter("'{}' group not in parameters.".format(group))
    for param_name in param_names:
        if param_name not in params[group] or params[group][param_name] == "":
            raise MissingParameter(param_type=param_name.replace("_", " "))
        if param_name == "name":
            param = params[group][param_name]
            params[group][param_name] = param.replace(" ", "_")


def _prompt_param(params, param, text, default=None, show_default=True):
    if param not in params or not params[param]:
        params[param] = prompt(text=text, default=default, show_default=show_default)


def prompt_params(params, params_dict, group):
    for param, values in params_dict.items():
        _prompt_param(params[group], param, *values['args'], **values['kwargs'])


def prompt_params_list(params, group, *param_list):
    for param in param_list:
        if param not in params[group] or not params[group][param]:
            params[group][param] = prompt(
                text="Required {} (comma separated)".format(param),
                default="", value_proc=parse_list_option)


def prompt_common_params(params):
    _params = params["common"]
    if "year" not in params or not _params["year"]:
        _params["year"] = datetime.datetime.now().year
    _prompt_param(_params, "author_name", "Author name", default=get_username())
    _prompt_param(_params, "author_email", "Author email", default=get_usermail())
    _prompt_param(_params, "organization", "Organization", default=get_username())


def render_file(context, template_dir, source, dest):
    """Generate a file from an input template and a dict of parameters."""
    loader = FileSystemLoader(searchpath=template_dir)
    env = Environment(
        loader=loader, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True
    )
    env.globals.update(zip=zip)
    template = env.get_template(source)
    render = template.render(**context)
    with open(dest, "w") as f_dest:
        f_dest.write(render)


TEMPLATE_BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)


def render_source(context, template_dir, input_files, output_dir, output_subdir=""):
    """Generate a list of files given from an input template directory."""
    template_dir = os.path.join(TEMPLATE_BASE_DIR, template_dir)
    if output_subdir:
        output_dir = os.path.join(output_dir, output_subdir)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    files = {
        filename + ".j2": os.path.join(output_dir, filename) for filename in input_files
    }

    for source, dest in files.items():
        render_file(context, template_dir, source, dest)
