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
VERBOSE: Final[bool] = bool(os.environ.get("VERBOSE", True))
