"""Utils tests."""

import subprocess

from mock import patch

from riotgen.utils import clone_repository, get_usermail, get_username


@patch("subprocess.check_output")
def test_get_usermail(m_check):
    """Test the get_usermail function."""
    m_check.return_value = b"email\n"
    assert get_usermail() == "email"

    m_check.side_effect = subprocess.CalledProcessError(42, "test")
    assert get_usermail() == ""


@patch("subprocess.check_output")
def test_get_username(m_check):
    """Test the get_username function."""
    m_check.return_value = b"name\n"
    assert get_username() == "name"

    m_check.side_effect = subprocess.CalledProcessError(42, "test")
    assert get_username() == ""


@patch("subprocess.check_call")
def test_clone_repository(m_check):
    """Test the clone_repository function."""
    m_check.return_value = 0
    assert clone_repository("test", "test", "test") == 0
