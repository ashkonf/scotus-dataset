import importlib
import pathlib
import sys


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))


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
    assert settings.VERBOSE is False


def test_verbose_env_truthy(monkeypatch):
    monkeypatch.setenv("VERBOSE", "1")
    settings = reload_settings()
    assert settings.VERBOSE is True
