"""Common tests."""

import os
import datetime
import pytest

from click import MissingParameter

from mock import patch

from riotgen import common
from riotgen.common import read_config_file, check_riotbase, check_param
from riotgen.common import check_common_params, prompt_param, prompt_param_list
from riotgen.common import prompt_common_params, render_file, render_source
from riotgen.utils import parse_list_option


TEST_CONFIG = """[common]
name=test
[board]
name=test_board
features=feature1,feature2
modules=
"""


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
    assert "common" in config
    assert "application" not in config
    assert "name" in config["common"]
    assert config["common"]["name"] == "test"
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
    """Test the check_param function."""
    with pytest.raises(MissingParameter):
        check_param({}, "test")

    with pytest.raises(MissingParameter):
        check_param({"test": ""}, "test")

    check_param({"test": "test"}, "test")


@patch("riotgen.common.prompt")
def test_prompt_param(m_prompt):
    """Test the prompt_param function."""
    prompt_param({"test": "test"}, "test", "Test text")
    assert m_prompt.call_count == 0
    prompt_param({"test": ""}, "test", "Test text")
    m_prompt.assert_called_with(text="Test text", default=None, show_default=True)
    prompt_param({}, "test", "Test text")
    m_prompt.assert_called_with(text="Test text", default=None, show_default=True)


@patch("riotgen.common.prompt")
def test_prompt_param_list(m_prompt):
    """Test the prompt_param function."""
    prompt_param_list({"test": "test"}, "test", "Test text")
    assert m_prompt.call_count == 0
    prompt_param_list({"test": ""}, "test", "Test text")
    m_prompt.assert_called_with(
        text="Test text", default="", value_proc=parse_list_option
    )
    prompt_param_list({}, "test", "Test text")
    m_prompt.assert_called_with(
        text="Test text", default="", value_proc=parse_list_option
    )


@pytest.fixture
def mock_utils(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""
    monkeypatch.setattr(common, "get_username", lambda: "test_user")
    monkeypatch.setattr(common, "get_usermail", lambda: "test_mail")


@patch("riotgen.common.check_param", lambda x, y: None)
def test_check_common_params(mock_utils):
    """Test the check_common_params function."""
    test_params = {"common": {}}
    check_common_params(test_params)
    assert test_params["common"]["year"] == datetime.datetime.now().year
    assert test_params["common"]["author_name"] == "test_user"
    assert test_params["common"]["author_email"] == "test_mail"
    assert test_params["common"]["organization"] == "test_user"

    test_params = {
        "common": {
            "year": "1970",
            "author_name": "user_test",
            "author_email": "mail_test",
            "organization": "orga",
        }
    }

    check_common_params(test_params)
    assert test_params["common"]["year"] == "1970"
    assert test_params["common"]["author_name"] == "user_test"
    assert test_params["common"]["author_email"] == "mail_test"
    assert test_params["common"]["organization"] == "orga"


def test_prompt_params_common(mock_utils):
    """Test the prompt_params_common function."""
    test_params = {"common": {}}
    with patch("riotgen.common.prompt") as m_prompt:
        m_prompt.return_value = "test"
        prompt_common_params(test_params)
        assert m_prompt.call_count == 3

    assert test_params["common"]["year"] == datetime.datetime.now().year
    assert test_params["common"]["author_name"] == "test"
    assert test_params["common"]["author_email"] == "test"
    assert test_params["common"]["organization"] == "test"

    test_params = {
        "common": {
            "year": "1970",
            "author_name": "user_test",
            "author_email": "mail_test",
            "organization": "orga",
        }
    }

    with patch("riotgen.common.prompt") as m_prompt:
        prompt_common_params(test_params)
        assert m_prompt.call_count == 0

    assert test_params["common"]["year"] == datetime.datetime.now().year
    assert test_params["common"]["author_name"] == "user_test"
    assert test_params["common"]["author_email"] == "mail_test"
    assert test_params["common"]["organization"] == "orga"


def test_render_file(tmpdir):
    """Test the render_file function."""
    dest = tmpdir.join("template_dest").strpath
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
    context = {
        "common": {"test": "test",},
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
        "common": {"test": "test",},
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
