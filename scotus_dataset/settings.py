from __future__ import annotations

import os
from typing import Final

BASE_DIR: Final[str] = os.path.dirname(os.path.dirname(__file__))
DATA_DIR_PATH: Final[str] = os.path.join(BASE_DIR, "data")
TRANSCRIPTS_DIR_PATH: Final[str] = os.path.join(DATA_DIR_PATH, "transcripts")
SCDB_FILE_PATH: Final[str] = os.path.join(
    DATA_DIR_PATH, "SCDB_2019_01_caseCentered_Docket.csv"
)
DATABASE_FILE_PATH: Final[str] = os.path.join(DATA_DIR_PATH, "db.sqlite")


def _env_flag(name: str, default: bool = False) -> bool:
    """Return ``True`` if the environment variable is truthy.

    The check is case insensitive and treats ``1``, ``true``, ``yes``, ``y`` and
    ``t`` as truthy values. Any other non-empty string is considered ``False``.
    """

    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "t"}


VERBOSE: Final[bool] = _env_flag("VERBOSE", default=True)
