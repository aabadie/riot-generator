"""Common generator module."""

import os
import datetime
import textwrap

from configparser import ConfigParser, ParsingError

import yaml

from jinja2 import Environment, FileSystemLoader
from click import prompt, Choice, MissingParameter, BadParameter, Abort

from .utils import get_usermail, get_username, parse_list_option


TEMPLATE_BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)

PARAMS_LIST_AVAILABLE = [
    "modules",
    "packages",
    "features_required",
    "features_provided",
]

LICENSES = ["LGPL21", "BSD", "MIT", "MPL2", "Apache2", "AGPL3"]


def read_config_file(config_file, *command_args):
    """Read a configuration file and return the content as a dict."""
    try:
        params = yaml.load(config_file, Loader=yaml.FullLoader)
    except yaml.parser.ParserError:
        try:
            config_file.seek(0)
            parser = ConfigParser()
            parser.read_file(config_file)
            params = parser._sections  # pylint:disable=protected-access
        except ParsingError:
            # pylint: disable=raise-missing-from
            raise BadParameter("Cannot parse config file '{config_file.filename}'")

    for command in command_args:
        if command not in params:
            continue
        _params = params[command]
        for param in PARAMS_LIST_AVAILABLE:
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


def check_global_params(params):
    """Check global parameters."""
    if "global" not in params:
        params.update({"global": {}})
    _params = params["global"]
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


def check_params(params, params_descriptor, group):
    """Check a list of parameters."""
    if group not in params:
        raise BadParameter(f"'{group}' group not in parameters.")
    for param_name, param_values in params_descriptor.items():
        if param_name not in params[group] or params[group][param_name] == "":
            if "kwargs" in param_values and "default" in param_values["kwargs"]:
                params[group][param_name] = param_values["kwargs"]["default"]
            else:
                raise MissingParameter(param_type=param_name.replace("_", " "))
        if param_name == "name":
            param = params[group][param_name]
            params[group][param_name] = param.replace(" ", "_")


def _prompt_param(
    params,
    param,
    text,
    default=None,
    show_default=True,
    param_type=None,
    show_choices=True,
):
    if param not in params or not params[param]:
        params[param] = prompt(
            text=text,
            default=default,
            show_default=show_default,
            type=param_type,
            show_choices=show_choices,
        )


def prompt_params(params, params_descriptor, group):
    """Prompt a list of parameters."""
    for param, values in params_descriptor.items():
        _prompt_param(params[group], param, *values["args"], **values["kwargs"])


def prompt_params_list(params, group, *param_list):
    """Prompt a list of list parameters."""
    for param in param_list:
        if param not in params[group] or not params[group][param]:
            params[group][param] = prompt(
                text=f"{param.replace('_', ' ').capitalize()} (comma separated)",
                default="",
                value_proc=parse_list_option,
            )


def prompt_global_params(params):
    """Prompt global parameters."""
    _params = params["global"]
    if "year" not in params or not _params["year"]:
        _params["year"] = datetime.datetime.now().year
    if "license" not in params:
        _prompt_param(
            _params,
            "license",
            "License",
            param_type=Choice(LICENSES),
            show_choices=True,
        )
    _prompt_param(_params, "author_name", "Author name", default=get_username())
    _prompt_param(_params, "author_email", "Author email", default=get_usermail())
    _prompt_param(_params, "organization", "Organization", default=get_username())


def render_file(context, group, source, dest):
    """Generate a file from an input template and a dict of parameters."""
    loader = FileSystemLoader(searchpath=TEMPLATE_BASE_DIR)
    env = Environment(
        loader=loader, trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True
    )
    source_file = group + "/" + source
    env.globals.update(zip=zip)
    template = env.get_template(source_file)
    render = template.render(**context)
    with open(dest, "w") as f_dest:
        f_dest.write(render)


def render_source(context, group, input_files, output_dir):
    """Generate a list of files given from an input template directory."""
    output_dir = os.path.abspath(os.path.expanduser(output_dir))

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    for source, dest in input_files.items():
        if dest is None:
            dest = source
        else:
            dest = dest.format(name=context[group]["name"])
        dest = os.path.join(output_dir, dest)
        render_file(context, group, source + ".j2", dest)


def load_license(params, prefix):
    """Load the license_header in params from the data."""
    licences_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "licenses"
    )

    if "global" in params and "license" in params["global"]:
        with open(
            os.path.join(licences_dir, params["global"]["license"] + ".txt")
        ) as f_license:
            license_header = textwrap.indent(f_license.read(), prefix)
            params["global"]["license_header"] = license_header


def load_and_check_params(
    group,
    params_descriptor,
    params_as_list,
    interactive,
    config,
    riotbase,
    in_riot_dir=None,
):
    """Load, prompt and check configuration parameters."""
    if not interactive and config is None:
        raise MissingParameter(param_type="--interactive and/or --config options")

    check_riotbase(riotbase)
    riotbase = os.path.abspath(os.path.expanduser(riotbase))

    params = {group: {}, "global": {}}
    if config is not None:
        params = read_config_file(config, group)

    if in_riot_dir is None:
        params[group]["riotbase"] = riotbase
    elif "global" in params:
        params["global"]["license"] = "LGPL21"

    if interactive:
        prompt_params(params, params_descriptor, group)
        prompt_params_list(params, group, *params_as_list)
        prompt_global_params(params)

    load_license(params, " * ")

    check_params(params, params_descriptor, group)
    if "global" in params:
        check_global_params(params)

    return params


def check_overwrite(output_dir):
    """Check if output directory exists and prompt for overwrite."""
    if os.path.exists(output_dir):
        reply = prompt(
            f"{output_dir} directory already exists, overwrite (y/N)?",
            default=False,
            show_default=False,
        )
        if not reply or reply == "N":
            raise Abort()
