import os
import sys
import types
import importlib
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def _import_recon():
    # Remove any existing modules that might interfere
    for name in ['recon', 'models', 'transcripts', 'scdb']:
        sys.modules.pop(name, None)

    # Stub out heavy dependencies
    models_stub = types.ModuleType('models')
    class Dummy:
        pass
    models_stub.Transcript = Dummy
    models_stub.Statement = Dummy
    models_stub.Case = Dummy
    sys.modules['models'] = models_stub

    transcripts_stub = types.ModuleType('transcripts')
    transcripts_stub.preprocess_all_transcripts = lambda: None
    sys.modules['transcripts'] = transcripts_stub

    scdb_stub = types.ModuleType('scdb')
    scdb_stub.load_cases = lambda: None
    sys.modules['scdb'] = scdb_stub

    return importlib.import_module('recon')


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
