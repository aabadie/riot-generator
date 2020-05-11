"""Utility functions"""

import shlex
from configparser import ConfigParser
from subprocess import check_output, check_call, CalledProcessError


def parse_list_option(opt):
    """Split list element separated by a comma."""
    if not opt:
        return []
    return sorted(opt.split(','))


def _get_git_config(config):
    cmd = 'git config --get {config}'.format(config=config)
    try:
        config = check_output(shlex.split(cmd)).decode()[:-1]
    except CalledProcessError:
        config = ''

    return config


def get_username():
    return _get_git_config('user.name')


def get_usermail():
    return _get_git_config('user.email')


def clone_repository(url, version, dest):
    cmd = 'git clone --depth=1 -b {version} {url} {dest}'.format(
        dest=dest, url=url, version=version
    )
    return check_call(shlex.split(cmd))


def read_config(filename):
    parser = ConfigParser()
    parser.readfp(filename)
    return parser._sections
