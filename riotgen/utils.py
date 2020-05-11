"""Utility functions"""

from configparser import ConfigParser
from subprocess import check_output, CalledProcessError


def parse_list_option(opt):
    """Split list element separated by a comma."""
    if not opt:
        return []
    return sorted(opt.split(','))


def _get_git_config(config):
    try:
        config = check_output(
            ['git', 'config', '--get', config]).decode()[:-1]
    except CalledProcessError:
        config = ''

    return config


def get_username():
    return _get_git_config('user.name')


def get_usermail():
    return _get_git_config('user.email')


def read_config(filename, section=None):
    parser = ConfigParser()
    parser.readfp(filename)
    config = dict(parser.items('common'))
    if section is not None:
        config.update(dict(parser.items(section)))
    return config
