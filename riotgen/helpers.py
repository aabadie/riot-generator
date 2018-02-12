"""Internal helper functions"""

import os.path
import datetime
from configparser import ConfigParser
from subprocess import check_output

import click

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(PKG_DIR, 'templates')


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


def _prompt_common_information():
    params = {}
    params['year'] = datetime.datetime.now().year
    params['author_name'] = click.prompt(
        text='Author name', default=_get_username())
    params['author_email'] = click.prompt(
        text='Author email', default=_get_usermail())
    params['organization'] = click.prompt(
        text='Organization', default=_get_username())
    return params


def _read_config(filename, section=None):
    parser = ConfigParser()
    parser.read(filename)
    config = dict(parser.items('common'))
    if section is not None:
        config.update(dict(parser.items(section)))
    return config


def _read_board_config(filename):
    return _read_config(filename, section='board')


def _read_driver_config(filename):
    return _read_config(filename, section='driver')


def _read_test_config(filename):
    return _read_config(filename, section='test')
