import importlib
from unittest.mock import patch

import mesop.server.server_utils as su
from mesop.env import env


def reload_utils():
  importlib.reload(su)


def test_remove_base_url_path_no_base():
  with patch.object(env, "MESOP_BASE_URL_PATH", ""):
    reload_utils()
    assert su.remove_base_url_path("/foo") == "/foo"


def test_remove_base_url_path_with_base():
  with patch.object(env, "MESOP_BASE_URL_PATH", "/base"):
    reload_utils()
    assert su.remove_base_url_path("/base/foo") == "/foo"
    assert su.remove_base_url_path("/base") == "/"
    assert su.remove_base_url_path("/base/") == "/"


def test_prefix_base_url_with_base():
  with patch.object(env, "MESOP_BASE_URL_PATH", "/base"):
    reload_utils()
    assert su.prefix_base_url("/foo") == "/base/foo"
    assert su.prefix_base_url("foo") == "/base/foo"


def test_prefix_base_url_no_base():
  with patch.object(env, "MESOP_BASE_URL_PATH", ""):
    reload_utils()
    assert su.prefix_base_url("/foo") == "/foo"
