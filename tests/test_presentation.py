from resumebot.answering import NOT_FOUND, Answer
from resumebot.corpus import Chunk
from resumebot.presentation import format_answer


def test_answer_lists_each_source_with_heading_and_document():
    chunk = Chunk(
        "exp-a#grant",
        "exp-a",
        "MA by Research, University of Akureyri",
        "Grant and presentations",
        "text",
        "cv",
        ("CV, Data Science version (2026)", "Clarifications from Kheirie (2026-10-12)"),
    )
    shown = format_answer(Answer("Kheirie received a grant.", True, [chunk], "answered"))
    assert shown.startswith("Kheirie received a grant.")
    assert "**Sources**" in shown
    assert (
        "- *Grant and presentations* · MA by Research, University of Akureyri · "
        "CV, Data Science version (2026); Clarifications from Kheirie (2026-10-12)"
    ) in shown


def test_answer_without_citations_is_shown_alone():
    assert format_answer(Answer(NOT_FOUND, False, [], "abstained_retrieval")) == NOT_FOUND
