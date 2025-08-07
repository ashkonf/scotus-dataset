import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from scotus_dataset.models import aggressively_sanitize_string
from scotus_dataset.settings import DATA_DIR_PATH


def test_sanitize() -> None:
    assert aggressively_sanitize_string("hi\u2603") == "hi"


def test_settings_path() -> None:
    assert DATA_DIR_PATH.endswith("data")
