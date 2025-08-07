import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scotus_dataset.models import aggressively_sanitize_string, Statement, Transcript


def make_statement(speaker: str) -> Statement:
    transcript = Transcript(raw_text="", term=2020, docket="1", file_name="f")
    return Statement(transcript=transcript, speaker=speaker)


def test_aggressively_sanitize_string_removes_non_ascii():
    text = "Hello\u2014World"  # contains an em dash
    assert aggressively_sanitize_string(text) == "HelloWorld"


def test_speaker_is_justice_true_cases():
    assert make_statement("JUSTICE SMITH").speaker_is_justice()
    assert make_statement("CHIEF JUSTICE DOE").speaker_is_justice()
    assert make_statement("QUESTION").speaker_is_justice()


def test_speaker_is_justice_false_case():
    assert not make_statement("MR. SMITH").speaker_is_justice()
