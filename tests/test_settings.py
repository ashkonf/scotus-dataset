import importlib
import sys

def reload_settings():
    sys.modules.pop('settings', None)
    return importlib.import_module('settings')

def test_verbose_default_true(monkeypatch):
    monkeypatch.delenv('VERBOSE', raising=False)
    settings = reload_settings()
    assert settings.VERBOSE is True

def test_verbose_env_override(monkeypatch):
    monkeypatch.setenv('VERBOSE', '0')
    settings = reload_settings()
    assert settings.VERBOSE == '0'
