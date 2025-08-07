from __future__ import annotations

import os
from typing import Final


def _env_flag(name: str, default: bool) -> bool:
    """Return a boolean parsed from environment variable ``name``.

    Recognizes common truthy strings ("1", "true", "yes", "on") and
    falsy strings ("0", "false", "no", "off"), case-insensitively.
    Unrecognized values fall back to ``default``.
    """

    value = os.environ.get(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "f", "no", "n", "off"}:
        return False
    return default


DATA_DIR_PATH: Final[str] = os.path.join(os.path.dirname(__file__), "data")
TRANSCRIPTS_DIR_PATH: Final[str] = os.path.join(DATA_DIR_PATH, "transcripts")
SCDB_FILE_PATH: Final[str] = os.path.join(
    DATA_DIR_PATH, "SCDB_2019_01_caseCentered_Docket.csv"
)
DATABASE_FILE_PATH: Final[str] = os.path.join(DATA_DIR_PATH, "db.sqlite")
VERBOSE: Final[bool] = _env_flag("VERBOSE", True)
