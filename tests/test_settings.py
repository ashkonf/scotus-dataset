import importlib
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def reload_settings():
    sys.modules.pop("scotus_dataset.settings", None)
    return importlib.import_module("scotus_dataset.settings")


def test_verbose_default_true(monkeypatch):
    monkeypatch.delenv("VERBOSE", raising=False)
    settings = reload_settings()
    assert settings.VERBOSE is True


def test_verbose_env_override(monkeypatch):
    monkeypatch.setenv("VERBOSE", "0")
    settings = reload_settings()
    assert settings.VERBOSE is True
