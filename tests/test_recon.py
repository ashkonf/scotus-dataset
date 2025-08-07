import os
import sys
import types
import importlib
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def _import_recon():
    """Import ``scotus_dataset.recon`` with heavy dependencies stubbed out."""
    # Remove any existing modules that might interfere
    module_names = [
        "scotus_dataset.recon",
        "scotus_dataset.models",
        "scotus_dataset.transcripts",
        "scotus_dataset.scdb",
    ]
    for name in module_names:
        sys.modules.pop(name, None)

    # Stub out heavy dependencies
    models_stub = types.ModuleType("scotus_dataset.models")

    class Dummy:
        pass

    models_stub.Transcript = Dummy
    models_stub.Statement = Dummy
    models_stub.Case = Dummy
    sys.modules["scotus_dataset.models"] = models_stub

    transcripts_stub = types.ModuleType("scotus_dataset.transcripts")
    transcripts_stub.preprocess_all_transcripts = lambda: None
    sys.modules["scotus_dataset.transcripts"] = transcripts_stub

    scdb_stub = types.ModuleType("scotus_dataset.scdb")
    scdb_stub.load_cases = lambda: None
    sys.modules["scotus_dataset.scdb"] = scdb_stub

    return importlib.import_module("scotus_dataset.recon")


recon = _import_recon()


@pytest.mark.parametrize(
    'raw,expected', [
        ('A-123 ORIG', '123'),
        ('12-345 (Original)', '12-345'),
        ('10-100, ORIG', '10-100'),
        ('16-123 ORIG ORIG', '16-123'),
        ('A-100', '100'),
        ('12-345 M', '12-345'),
    ]
)
def test_preprocess_docket(raw, expected):
    assert recon.preprocess_docket(raw) == expected
