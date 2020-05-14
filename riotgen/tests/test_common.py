"""Common tests."""

import os
import datetime
import pytest

from click import MissingParameter, BadParameter

from mock import patch

from riotgen import common
from riotgen.common import read_config_file, check_riotbase
from riotgen.common import _check_param, check_params
from riotgen.common import check_global_params, _prompt_param, prompt_params
from riotgen.common import prompt_global_params, prompt_params_list
from riotgen.common import render_file, render_source
from riotgen.utils import parse_list_option


TEST_CONFIG = """[global]
name=test
[board]
name=test_board
features=feature1,feature2
modules=
"""

TEST_PARAMS = {
    "name": {"args": ["name description"], "kwargs": {}},
    "board": {"args": ["board description"], "kwargs": {"default": "test"}},
}


@pytest.fixture()
def config_file(tmpdir_factory):
    """A fixture returning a temporary config filename."""
    filename = tmpdir_factory.mktemp("config").join("test.cfg")
    with open(filename, "w") as cfg_test:
        cfg_test.write(TEST_CONFIG)
    return filename


def test_read_config_file(config_file):
    """Test the read_config function."""
    with open(config_file.strpath) as f_config:
        config = read_config_file(f_config, "application", "board")
    assert "global" in config
    assert "application" not in config
    assert "name" in config["global"]
    assert config["global"]["name"] == "test"
    assert "board" in config
    assert "name" in config["board"]
    assert config["board"]["name"] == "test_board"
    assert "features" in config["board"]
    assert config["board"]["features"] == ["feature1", "feature2"]


def test_check_riotbase():
    """Test the check_riotbase function."""
    with pytest.raises(MissingParameter):
        check_riotbase(None)

    with pytest.raises(MissingParameter):
        check_riotbase("")

    check_riotbase("test")


def test_check_param():
    """Test the _check_param function."""
    with pytest.raises(MissingParameter):
        _check_param({}, "test")

    with pytest.raises(MissingParameter):
        _check_param({"test": ""}, "test")

    _check_param({"test": "test"}, "test")


def test_check_params():
    """Test the _check_params function."""
    with pytest.raises(BadParameter):
        check_params({}, ["test"], "test")

    params = {"test": {"name": "test name", "board": "test_board"}}
    check_params(params, params["test"].keys(), "test")
    assert params["test"]["name"] == "test_name"
    assert params["test"]["board"] == "test_board"

    params = {"test": {"name": "test name", "board": ""}}
    with pytest.raises(MissingParameter):
        check_params(params, params["test"].keys(), "test")


@patch("riotgen.common.prompt")
def test_prompt_param(m_prompt):
    """Test the _prompt_param function."""
    _prompt_param({"test": "test"}, "test", "Test text")
    assert m_prompt.call_count == 0
    _prompt_param({"test": ""}, "test", "Test text")
    m_prompt.assert_called_with(text="Test text", default=None, show_default=True)
    _prompt_param({}, "test", "Test text")
    m_prompt.assert_called_with(text="Test text", default=None, show_default=True)


@patch("riotgen.common.prompt")
def test_prompt_params(m_prompt):
    """Test the prompt_params function."""
    params = {"test": {"name": "test_name", "board": "test_board"}}
    prompt_params(params, TEST_PARAMS, "test")
    assert m_prompt.call_count == 0
    params = {"test": {"name": "test_name", "board": ""}}
    prompt_params(params, TEST_PARAMS, "test")
    assert m_prompt.call_count == 1
    m_prompt.assert_called_with(
        text="board description", default="test", show_default=True
    )
    m_prompt.call_count = 0
    params = {"test": {"name": "", "board": ""}}
    prompt_params(params, TEST_PARAMS, "test")
    assert m_prompt.call_count == 2


@patch("riotgen.common.prompt")
def test_prompt_params_list(m_prompt):
    """Test the prompt_params_list function."""
    params = {"test": {"test1": "test", "test2": "test3", "test3": "test3"}}
    prompt_params_list(params, "test", "test1", "test2", "test3")
    assert m_prompt.call_count == 0
    params = {"test": {"test1": "test", "test2": "test3"}}
    prompt_params_list(params, "test", "test1", "test2", "test3")
    assert m_prompt.call_count == 1  # for missing test3
    m_prompt.assert_called_with(
        text="Required test3 (comma separated)",
        default="",
        value_proc=parse_list_option,
    )

    m_prompt.call_count = 0
    params = {"test": {}}
    prompt_params_list(params, "test", "test1", "test2", "test3")
    assert m_prompt.call_count == 3


@pytest.fixture
def mock_utils(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""
    monkeypatch.setattr(common, "get_username", lambda: "test_user")
    monkeypatch.setattr(common, "get_usermail", lambda: "test_mail")


@patch("riotgen.common._check_param", lambda x, y: None)
def test_check_global_params(mock_utils):
    """Test the check_global_params function."""
    test_params = {"global": {}}
    check_global_params(test_params)
    assert test_params["global"]["year"] == datetime.datetime.now().year
    assert test_params["global"]["author_name"] == "test_user"
    assert test_params["global"]["author_email"] == "test_mail"
    assert test_params["global"]["organization"] == "test_user"

    test_params = {
        "global": {
            "year": "1970",
            "author_name": "user_test",
            "author_email": "mail_test",
            "organization": "orga",
        }
    }

    check_global_params(test_params)
    assert test_params["global"]["year"] == "1970"
    assert test_params["global"]["author_name"] == "user_test"
    assert test_params["global"]["author_email"] == "mail_test"
    assert test_params["global"]["organization"] == "orga"


def test_prompt_global_params(mock_utils):
    """Test the prompt_global_params function."""
    test_params = {"global": {}}
    with patch("riotgen.common.prompt") as m_prompt:
        m_prompt.return_value = "test"
        prompt_global_params(test_params)
        assert m_prompt.call_count == 3

    assert test_params["global"]["year"] == datetime.datetime.now().year
    assert test_params["global"]["author_name"] == "test"
    assert test_params["global"]["author_email"] == "test"
    assert test_params["global"]["organization"] == "test"

    test_params = {
        "global": {
            "year": "1970",
            "author_name": "user_test",
            "author_email": "mail_test",
            "organization": "orga",
        }
    }

    with patch("riotgen.common.prompt") as m_prompt:
        prompt_global_params(test_params)
        assert m_prompt.call_count == 0

    assert test_params["global"]["year"] == datetime.datetime.now().year
    assert test_params["global"]["author_name"] == "user_test"
    assert test_params["global"]["author_email"] == "mail_test"
    assert test_params["global"]["organization"] == "orga"


def test_render_file(tmpdir):
    """Test the render_file function."""
    dest = tmpdir.join("template_dest").strpath
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    context = {
        "global": {"test": "test",},
        "test": {"tests": ["test1", "test2", "test3"]},
    }

    render_file(context, template_dir, "template.j2", dest)
    with open(dest, "r") as f_dest:
        dest_content = f_dest.read()

    with open(os.path.join(template_dir, "expected"), "r") as f_expected:
        expected_content = f_expected.read()

    assert dest_content == expected_content


def test_render_source(tmpdir):
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    context = {
        "global": {"test": "test",},
        "test": {"tests": ["test1", "test2", "test3"]},
    }
    with patch("riotgen.common.TEMPLATE_BASE_DIR", template_dir):
        render_source(
            context, template_dir, ["template"], tmpdir.strpath, output_subdir=""
        )

    dest_file = tmpdir.join("template").strpath
    assert os.path.exists(dest_file)
    with open(dest_file, "r") as f_dest:
        dest_content = f_dest.read()

    with open(os.path.join(template_dir, "expected"), "r") as f_expected:
        expected_content = f_expected.read()

    assert dest_content == expected_content

    with patch("riotgen.common.TEMPLATE_BASE_DIR", template_dir):
        render_source(
            context, template_dir, ["template"], tmpdir.strpath, output_subdir="subdir"
        )

    dest_file = tmpdir.join("subdir", "template").strpath
    assert os.path.exists(dest_file)
    with open(dest_file, "r") as f_dest:
        dest_content = f_dest.read()

    with open(os.path.join(template_dir, "expected"), "r") as f_expected:
        expected_content = f_expected.read()

    assert dest_content == expected_content
