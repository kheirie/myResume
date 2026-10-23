from resumebot.answering import NOT_FOUND, Answer
from resumebot.corpus import Chunk
from resumebot.presentation import format_answer, use_display_name


def test_answer_is_shown_without_its_sources():
    # Kheirie's choice (2026-10-16): recruiters see only the answer. Citations are still
    # required and checked in code; they just are not displayed.
    chunk = Chunk(
        "exp-a#grant",
        "exp-a",
        "MA by Research, University of Akureyri",
        "Grant and presentations",
        "text",
        "cv",
        ("CV, Data Science version (2026)",),
    )
    shown = format_answer(Answer("Kheirie received a grant.", True, [chunk], "answered"))
    assert shown == "Kheirie received a grant."


def test_answer_without_citations_is_shown_alone():
    assert format_answer(Answer(NOT_FOUND, False, [], "abstained_retrieval")) == NOT_FOUND


def test_model_line_names_the_model_and_provider_that_answered():
    answer = Answer("Kheirie received a grant.", True, [], "answered", answered_by="groq:openai/gpt-oss-120b")
    assert format_answer(answer, show_model=True) == "Kerry received a grant.\n\n*Model: openai/gpt-oss-120b (groq)*"


def test_no_model_line_when_no_model_was_called():
    answer = Answer(NOT_FOUND, False, [], "abstained_retrieval")
    assert format_answer(answer, show_model=True) == NOT_FOUND


def test_model_line_is_off_by_default():
    answer = Answer("Kheirie received a grant.", True, [], "answered", answered_by="groq:openai/gpt-oss-120b")
    assert format_answer(answer) == "Kerry received a grant."


def test_model_line_marks_a_fallback_and_why():
    answer = Answer(
        "Kheirie received a grant.", True, [], "answered",
        answered_by="openrouter:nvidia/nemotron",
        fallback_from=("groq:openai/gpt-oss-120b: RateLimitError",),
    )
    assert format_answer(answer, show_model=True).endswith(
        "*Model: nvidia/nemotron (openrouter) · fallback after groq:openai/gpt-oss-120b: RateLimitError*"
    )


def test_model_line_marks_a_cached_answer():
    answer = Answer("Kheirie received a grant.", True, [], "answered", answered_by="groq:m", from_cache=True)
    assert format_answer(answer, show_model=True).endswith("*Model: m (groq) · from cache*")


def test_busy_answer_lists_the_failed_models():
    answer = Answer("Busy.", False, [], "llm_unavailable", fallback_from=("groq:a: RateLimitError", "ollama:b: APIConnectionError"))
    assert format_answer(answer, show_model=True) == (
        "Busy.\n\n*All models failed: groq:a: RateLimitError; ollama:b: APIConnectionError*"
    )


def test_display_name_replaces_the_name_and_the_full_name():
    assert use_display_name("Kheirie El Hariri is a data scientist. Kheirie's CV lists Python.") == (
        "Kerry is a data scientist. Kerry's CV lists Python."
    )


def test_passages_keep_the_corpus_wording():
    # A passage answer has no model (answered_by is empty): it is quoted word for word.
    answer = Answer("At Sanofi, Kheirie built pipelines.", False, [], "passages")
    assert format_answer(answer) == "At Sanofi, Kheirie built pipelines."
