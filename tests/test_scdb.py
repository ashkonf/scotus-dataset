import pathlib
import sys
from types import SimpleNamespace

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

import scdb  # noqa: E402
from models import Case  # noqa: E402


def test_build_case_returns_case() -> None:
    row = SimpleNamespace(
        decisionType=1,
        voteId="1",
        term=2020,
        docket="123",
        chief="Roberts",
        dateDecision="01/02/2020",
    )
    case = scdb.__build_case(row)
    assert isinstance(case, Case)
