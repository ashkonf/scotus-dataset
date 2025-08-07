import types
import pytest
import recon


class Dummy:
    pass


def test_reconciliation_skips_objects_without_docket(monkeypatch):
    case_missing = Dummy()
    transcript_missing = Dummy()

    monkeypatch.setattr(
        recon, "Case", types.SimpleNamespace(select=lambda: [case_missing])
    )
    monkeypatch.setattr(
        recon, "Transcript", types.SimpleNamespace(select=lambda: [transcript_missing])
    )

    recon.reconciliate_cases_and_transcripts()


def test_reconciliation_propagates_unexpected_errors(monkeypatch):
    class Bad:
        @property
        def docket(self):
            raise ValueError("boom")

    bad_case = Bad()
    monkeypatch.setattr(recon, "Case", types.SimpleNamespace(select=lambda: [bad_case]))
    monkeypatch.setattr(recon, "Transcript", types.SimpleNamespace(select=list))

    with pytest.raises(ValueError):
        recon.reconciliate_cases_and_transcripts()
