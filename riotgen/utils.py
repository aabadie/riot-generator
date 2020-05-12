"""Utility functions"""

import shlex
import subprocess
from configparser import ConfigParser


def parse_list_option(opt):
    """Split list element separated by a comma.

    >>> parse_list_option('')
    []
    >>> parse_list_option('opt1,opt2,opt3')
    ['opt1', 'opt2', 'opt3']
    """
    print(opt)
    if not opt:
        return []
    return sorted(opt.split(","))


def _get_git_config(config):
    cmd = "git config --get {config}".format(config=config)
    try:
        config = subprocess.check_output(shlex.split(cmd)).decode()[:-1]
    except subprocess.CalledProcessError:
        config = ""

    return config


def get_username():
    """Get the user name from git config."""
    return _get_git_config("user.name")


def get_usermail():
    """Get the user email from git config."""
    return _get_git_config("user.email")


def clone_repository(url, version, dest):
    """Clone a git repository."""
    cmd = "git clone --depth=1 -b {version} {url} {dest}".format(
        dest=dest, url=url, version=version
    )
    return subprocess.check_call(shlex.split(cmd))


def read_config(config_file):
    """Read a configuration file and return the content as a dict."""
    parser = ConfigParser()
    parser.read_file(config_file)
    return parser._sections
