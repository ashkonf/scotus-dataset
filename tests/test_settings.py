import importlib
import pathlib
import sys
from types import ModuleType

import pytest


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))


def reload_settings(monkeypatch: pytest.MonkeyPatch, value: str | None) -> ModuleType:
    """Reload ``settings`` with ``VERBOSE`` set to ``value``.

    ``value`` may be ``None`` to unset the environment variable.
    """

    if value is None:
        monkeypatch.delenv("VERBOSE", raising=False)
    else:
        monkeypatch.setenv("VERBOSE", value)

    import settings

    return importlib.reload(settings)


def test_verbose_true_values(monkeypatch: pytest.MonkeyPatch) -> None:
    assert reload_settings(monkeypatch, "true").VERBOSE is True
    assert reload_settings(monkeypatch, "1").VERBOSE is True


def test_verbose_false_values(monkeypatch: pytest.MonkeyPatch) -> None:
    assert reload_settings(monkeypatch, "false").VERBOSE is False
    assert reload_settings(monkeypatch, "0").VERBOSE is False


def test_verbose_default(monkeypatch: pytest.MonkeyPatch) -> None:
    assert reload_settings(monkeypatch, None).VERBOSE is True
