import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import aggressively_sanitize_string, RedFlag, Statement, Transcript


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


def test_add_paragraph_sanitizes_and_full_text():
    transcript = Transcript(
        raw_text="", term=2021, docket="2", file_name="g"
    ).get_or_create()
    statement = Statement(transcript=transcript, speaker="MR. SMITH").get_or_create()
    statement.add_paragraph("Hello\u2603")
    statement.add_paragraph("Hello\u2603")  # duplicate, should not add twice
    statement.add_paragraph("Second")
    assert statement.paragraphs() == ["Hello", "Second"]
    assert statement.full_text() == "Hello\n\nSecond"


def test_add_red_flag_dedupes():
    transcript = Transcript(
        raw_text="", term=2022, docket="3", file_name="h"
    ).get_or_create()
    transcript.add_red_flag("Issue")
    transcript.add_red_flag("Issue")  # duplicate
    assert transcript.has_red_flags()
    assert transcript.red_flags() == ["Issue"]
    assert RedFlag.select().where(RedFlag.transcript == transcript).count() == 1
