"""Utils tests."""

import subprocess
import pytest
from mock import patch

from riotgen.utils import get_usermail, get_username
from riotgen.utils import clone_repository, read_config


@patch('subprocess.check_output')
def test_get_usermail(m_check):
    """Test the get_usermail function."""
    m_check.return_value = b"email\n"
    assert get_usermail() == "email"

    m_check.side_effect = subprocess.CalledProcessError(42, "test")
    assert get_usermail() == ''


@patch('subprocess.check_output')
def test_get_username(m_check):
    """Test the get_username function."""
    m_check.return_value = b"name\n"
    assert get_username() == "name"

    m_check.side_effect = subprocess.CalledProcessError(42, "test")
    assert get_username() == ''


@patch('subprocess.check_call')
def test_clone_repository(m_check):
    """Test the clone_repository function."""
    m_check.return_value = 0
    assert clone_repository("test", "test", "test") == 0


TEST_CONFIG = """[common]
name=test
[board]
name=test_board"""


@pytest.fixture()
def config_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("config").join("test.cfg")
    with open(filename, "w") as cfg_test:
        cfg_test.write(TEST_CONFIG)
    return filename


def test_read_config(config_file):
    """Test the read_config function."""
    with open(config_file.strpath) as f_config:
        config = read_config(f_config)
    assert 'common' in config
    assert 'name' in config['common']
    assert config['common']['name'] == 'test'
    assert 'board' in config
    assert 'name' in config['board']
    assert config['board']['name'] == 'test_board'
