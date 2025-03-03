"""Common tests."""

import datetime
import os

import pytest
from click import BadParameter, MissingParameter
from mock import patch

import riotgen.common as common
from riotgen.common import (
    _check_param,
    _prompt_param,
    check_global_params,
    check_params,
    check_riotbase,
    prompt_global_params,
    prompt_params,
    prompt_params_list,
    read_config_file,
    render_file,
    render_source,
)
from riotgen.utils import parse_list_option

TEST_CONFIG = """[global]
name=test
[board]
name=test_board
features_provided=feature1,feature2
modules=
"""

TEST_YAML = """global:
  name: test
board:
  name: test_board
  features_provided: [feature1, feature2]
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
    """Test the read_config_file function."""
    with open(config_file.strpath) as f_config:
        config = read_config_file(f_config, "application", "board")
    assert "global" in config
    assert "application" not in config
    assert "name" in config["global"]
    assert config["global"]["name"] == "test"
    assert "board" in config
    assert "name" in config["board"]
    assert config["board"]["name"] == "test_board"
    assert "features_provided" in config["board"]
    assert config["board"]["features_provided"] == ["feature1", "feature2"]


@pytest.fixture()
def yaml_file(tmpdir_factory):
    """A fixture returning a temporary yaml filename."""
    filename = tmpdir_factory.mktemp("config").join("test.yml")
    with open(filename, "w") as yml_test:
        yml_test.write(TEST_YAML)
    return filename


def test_read_yaml_file(yaml_file):
    """Test the read_config_file function with a yaml input."""
    with open(yaml_file.strpath) as f_config:
        config = read_config_file(f_config, "application", "board")
    assert "global" in config
    assert "application" not in config
    assert "name" in config["global"]
    assert config["global"]["name"] == "test"
    assert "board" in config
    assert "name" in config["board"]
    assert config["board"]["name"] == "test_board"
    assert "features_provided" in config["board"]
    assert config["board"]["features_provided"] == ["feature1", "feature2"]


def test_invalid_config_file(tmpdir):
    """Test the read_config_file function with an invalid input file."""
    filename = tmpdir.join("config")
    with open(filename, "w") as f_config:
        f_config.write("[invalid_content]\n-")

    with pytest.raises(BadParameter):
        with open(filename) as f_config:
            read_config_file(f_config)


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

    # Regular test: all params in descriptor are set in the params
    params_descriptor = {
        "name": {
            "args": ["test name"],
            "kwargs": {},
        },
        "board": {
            "args": ["test board"],
            "kwargs": {"default": "native"},
        },
    }
    params = {"test": {"name": "test name", "board": "test_board"}}
    check_params(params, params_descriptor, "test")
    assert params["test"]["name"] == "test_name"
    assert params["test"]["board"] == "test_board"

    # Use default param: all but one are set, the remaining one has a default
    # value set in the descriptor
    params = {"test": {"name": "test name"}}
    check_params(params, params_descriptor, "test")
    assert params["test"]["name"] == "test_name"
    assert params["test"]["board"] == "native"

    # Missing default param
    params = {"test": {"name": "test name", "board": ""}}
    params_descriptor = {
        "name": {
            "args": ["test name"],
            "kwargs": {},
        },
        "board": {
            "args": ["test board"],
            "kwargs": {},
        },
    }
    with pytest.raises(MissingParameter):
        check_params(params, params_descriptor, "test")


@patch("riotgen.common.prompt")
def test_prompt_param(m_prompt):
    """Test the _prompt_param function."""
    _prompt_param({"test": "test"}, "test", "Test text")
    assert m_prompt.call_count == 0
    _prompt_param({"test": ""}, "test", "Test text")
    m_prompt.assert_called_with(
        text="Test text",
        default=None,
        show_default=True,
        type=None,
        show_choices=True,
    )
    _prompt_param({}, "test", "Test text")
    m_prompt.assert_called_with(
        text="Test text",
        default=None,
        show_default=True,
        type=None,
        show_choices=True,
    )


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
        text="board description",
        default="test",
        show_default=True,
        type=None,
        show_choices=True,
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
        text="Test3 (comma separated)",
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
    test_params = {}
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
        assert m_prompt.call_count == 4

    assert test_params["global"]["year"] == datetime.datetime.now().year
    for param in ["license", "author_name", "author_name", "organization"]:
        assert test_params["global"][param] == "test"

    test_params = {
        "global": {
            "year": "1970",
            "license": "BSD",
            "author_name": "user_test",
            "author_email": "mail_test",
            "organization": "orga",
        }
    }

    with patch("riotgen.common.prompt") as m_prompt:
        prompt_global_params(test_params)
        assert m_prompt.call_count == 0

    assert test_params["global"]["year"] == datetime.datetime.now().year
    assert test_params["global"]["license"] == "BSD"
    assert test_params["global"]["author_name"] == "user_test"
    assert test_params["global"]["author_email"] == "mail_test"
    assert test_params["global"]["organization"] == "orga"


def test_render_file(tmpdir):
    """Test the render_file function."""
    dest = tmpdir.join("template_dest").strpath
    context = {
        "global": {
            "test": "test",
        },
        "test_template": {"tests": ["test1", "test2", "test3"]},
    }

    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    with patch("riotgen.common.TEMPLATE_BASE_DIR", template_dir):
        render_file(context, "test_template", "template.j2", dest)
    with open(dest, "r") as f_dest:
        dest_content = f_dest.read()

    with open(os.path.join(template_dir, "expected"), "r") as f_expected:
        expected_content = f_expected.read()

    assert dest_content == expected_content


def test_render_source(tmpdir):
    template_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_data"
    )
    context = {
        "global": {
            "test": "test",
        },
        "test_template": {"tests": ["test1", "test2", "test3"]},
    }
    with patch("riotgen.common.TEMPLATE_BASE_DIR", template_dir):
        render_source(
            context, "test_template", {"template": None}, tmpdir.strpath
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
            context,
            "test_template",
            {"template": None},
            tmpdir.join("subdir").strpath,
        )

    dest_file = tmpdir.join("subdir", "template").strpath
    assert os.path.exists(dest_file)
    with open(dest_file, "r") as f_dest:
        dest_content = f_dest.read()

    with open(os.path.join(template_dir, "expected"), "r") as f_expected:
        expected_content = f_expected.read()

    assert dest_content == expected_content
