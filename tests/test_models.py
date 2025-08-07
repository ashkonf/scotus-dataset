import os
import sys
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scotus_dataset.models import (
    aggressively_sanitize_string,
    RedFlag,
    Statement,
    Transcript,
    Case,
)


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


def test_transcript_full_text_combines_statements():
    transcript = Transcript(
        raw_text="", term=2023, docket="4", file_name="i"
    ).get_or_create()
    petitioner = Statement(
        transcript=transcript,
        speaker="PETITIONER",
        speaker_is_petitioner=True,
    ).get_or_create()
    petitioner.add_paragraph("Petitioner")
    respondent = Statement(
        transcript=transcript,
        speaker="RESPONDENT",
        speaker_is_respondent=True,
    ).get_or_create()
    respondent.add_paragraph("Respondent")
    assert transcript.full_text() == "Petitioner\n\nRespondent"


def test_case_is_well_formed_checks_required_fields():
    day = date(2024, 1, 1)
    case = Case(
        decision_label=1,
        vote_id="v",
        term=2024,
        month=day,
        day=day,
        docket="d",
        justice_name="Justice",
    )
    assert case.is_well_formed()
    case.justice_name = ""
    assert not case.is_well_formed()
