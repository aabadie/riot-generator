"""Utility functions"""

import shlex
import subprocess


def parse_list_option(opt):
    """Parse options as list.

    Strings are splitted based on comma separated elements.
    Result is sorted.

    >>> parse_list_option('')
    []
    >>> parse_list_option('opt1,opt2,opt3')
    ['opt1', 'opt2', 'opt3']
    >>> parse_list_option(['opt1','opt3','opt2'])
    ['opt1', 'opt2', 'opt3']
    """
    if not opt:
        return []
    if isinstance(opt, (list, tuple)):
        return sorted(opt)
    return sorted(opt.split(","))


def _get_git_config(config):
    cmd = f"git config --get {config}"
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
    cmd = f"git clone --depth=1 -b {version} {url} {dest}"
    return subprocess.check_call(shlex.split(cmd))
