from datetime import date

from resumebot.answering import NOT_FOUND, TOO_LONG, MAX_QUESTION_CHARS, Answer
from resumebot.chat import (
    AI_ANSWERS_PER_DAY,
    PASSAGE_CLOSE_MARGIN,
    PASSAGES_NOTE,
    UNAVAILABLE_NOTE,
    Chat,
    PassageAnswerer,
    QuestionQuota,
    visitor_id,
    with_previous_question,
)
from resumebot.corpus import Chunk
from resumebot.retrieval import ABSTAIN_BELOW, Hit, SearchResult


def chunk(cid, heading, text):
    return Chunk(cid, cid.split("#")[0], "Demo Role, Demo Corp", heading, text, "cv", ("CV (2026)",))


GRANT = chunk("exp-a#grant", "Grant", "At Demo Corp, Kheirie received a grant.")
TEACHING = chunk("exp-a#teaching", "Teaching", "At Demo Corp, Kheirie taught.")
OTHER = chunk("exp-a#other", "Other", "A third passage.")
HITS = [Hit(GRANT, 0.80), Hit(TEACHING, 0.78), Hit(OTHER, 0.60)]  # the second is close to the first


class FakeRetriever:
    def __init__(self, top_similarity=0.8, hits=HITS):
        self.result = SearchResult(hits, top_similarity)

    def search(self, query, k=4):
        return self.result


class FakeClock:
    def __init__(self):
        self.today = date(2026, 10, 16)

    def __call__(self):
        return self.today


class FakeAnswerer:
    """Stands in for CachedAnswerer: an LLM answer, or a cached one for questions in `cached`."""

    def __init__(self, cached=()):
        self.cached = set(cached)
        self.asked = []

    def lookup(self, question):
        if question in self.cached:
            return Answer("Cached answer.", True, [], "answered", answered_by="groq:m", from_cache=True)
        return None

    def ask(self, question):
        self.asked.append(question)
        if question == "unknown":
            return Answer(NOT_FOUND, False, [], "abstained_retrieval")
        return Answer("AI answer.", True, [], "answered", answered_by="groq:m")


def make_chat(answerer=None, clock=None):
    return Chat(answerer or FakeAnswerer(), PassageAnswerer(FakeRetriever()), QuestionQuota(clock=clock or FakeClock()))


# --- quota ---------------------------------------------------------------------------


def test_quota_allows_three_ai_answers_per_visitor_per_day():
    quota = QuestionQuota(clock=FakeClock())
    for _ in range(AI_ANSWERS_PER_DAY):
        assert quota.remaining("v1") > 0
        quota.record("v1")
    assert quota.remaining("v1") == 0
    assert quota.remaining("v2") == AI_ANSWERS_PER_DAY  # another visitor has their own count


def test_quota_resets_the_next_day():
    clock = FakeClock()
    quota = QuestionQuota(clock=clock)
    for _ in range(AI_ANSWERS_PER_DAY):
        quota.record("v1")
    clock.today = date(2026, 10, 17)
    assert quota.remaining("v1") == AI_ANSWERS_PER_DAY


def test_visitor_id_prefers_the_forwarded_address_and_never_stores_it():
    behind_proxy = visitor_id(client_host="10.0.0.1", forwarded_for="203.0.113.7, 10.0.0.1")
    direct = visitor_id(client_host="203.0.113.7", forwarded_for=None)
    assert behind_proxy == direct
    assert "203.0.113.7" not in behind_proxy  # only a salted hash is kept


# --- passages mode ---------------------------------------------------------------------


def test_passages_show_only_the_best_section_when_the_second_matches_much_less():
    far = [Hit(GRANT, 0.80), Hit(TEACHING, 0.80 - PASSAGE_CLOSE_MARGIN - 0.01)]
    answer = PassageAnswerer(FakeRetriever(hits=far)).ask("Grants?")
    assert "At Demo Corp, Kheirie received a grant." in answer.text
    assert "At Demo Corp, Kheirie taught." not in answer.text


def test_passages_keep_a_second_section_the_reranker_placed_below_a_closer_match():
    # The reranker can put the more similar section second; it is then clearly worth showing.
    reordered = [Hit(GRANT, 0.70), Hit(TEACHING, 0.78)]
    answer = PassageAnswerer(FakeRetriever(hits=reordered)).ask("Grants?")
    assert "At Demo Corp, Kheirie taught." in answer.text


def test_passages_show_the_two_best_sections_with_a_note():
    answer = PassageAnswerer(FakeRetriever()).ask("Grants?")
    assert answer.outcome == "passages"
    assert answer.text.startswith(PASSAGES_NOTE)
    assert "At Demo Corp, Kheirie received a grant." in answer.text
    assert "At Demo Corp, Kheirie taught." in answer.text
    assert "A third passage." not in answer.text
    assert answer.answered_by is None  # no model wrote it


def test_passages_abstain_when_nothing_is_close():
    answer = PassageAnswerer(FakeRetriever(top_similarity=ABSTAIN_BELOW - 0.1)).ask("Rust?")
    assert answer.text == NOT_FOUND


def test_passages_refuse_long_questions():
    assert PassageAnswerer(FakeRetriever()).ask("x" * (MAX_QUESTION_CHARS + 1)).text == TOO_LONG


# --- choosing between AI answers and passages ---------------------------------------------


def test_first_three_questions_get_ai_answers_then_passages():
    chat = make_chat()
    outcomes = [chat.reply(f"question {i}", "v1").outcome for i in range(AI_ANSWERS_PER_DAY + 1)]
    assert outcomes == ["answered"] * AI_ANSWERS_PER_DAY + ["passages"]


def test_answers_that_cost_nothing_do_not_use_up_a_question():
    answerer = FakeAnswerer(cached={"example"})
    chat = make_chat(answerer)
    chat.reply("example", "v1")  # cached
    chat.reply("unknown", "v1")  # nothing found, no model call
    assert chat.remaining("v1") == AI_ANSWERS_PER_DAY


def test_cached_answers_are_served_even_after_the_limit():
    chat = make_chat(FakeAnswerer(cached={"example"}))
    for i in range(AI_ANSWERS_PER_DAY):
        chat.reply(f"question {i}", "v1")
    assert chat.reply("example", "v1").text == "Cached answer."


def test_passages_are_used_when_every_model_is_busy():
    class BusyAnswerer(FakeAnswerer):
        def ask(self, question):
            return Answer("busy", False, [], "llm_unavailable")

    chat = make_chat(BusyAnswerer())
    answer = chat.reply("Grants?", "v1")
    assert answer.outcome == "passages"
    assert chat.remaining("v1") == AI_ANSWERS_PER_DAY


def test_without_any_model_every_question_gets_passages():
    chat = Chat(None, PassageAnswerer(FakeRetriever()), QuestionQuota(clock=FakeClock()))
    assert chat.reply("Grants?", "v1").outcome == "passages"


def test_passages_explain_why_no_ai_answer_was_given():
    limit_reached = make_chat()
    for i in range(AI_ANSWERS_PER_DAY):
        limit_reached.reply(f"question {i}", "v1")
    assert limit_reached.reply("Grants?", "v1").text.startswith(PASSAGES_NOTE)
    no_model = Chat(None, PassageAnswerer(FakeRetriever()), QuestionQuota(clock=FakeClock()))
    assert no_model.reply("Grants?", "v1").text.startswith(UNAVAILABLE_NOTE)


def test_visitor_id_never_fails_on_missing_or_unusual_values():
    class Odd:
        def __str__(self):
            return "198.51.100.4"

    assert visitor_id(None, None) == visitor_id("unknown", None)
    assert visitor_id(Odd(), None) == visitor_id("198.51.100.4", None)


# --- follow-up questions -----------------------------------------------------------------


def test_follow_up_is_asked_with_the_previous_question():
    combined = with_previous_question("can you give more details?", "Has Kerry worked in NLP?")
    assert combined == "Has Kerry worked in NLP? can you give more details?"


def test_question_with_its_own_topic_is_asked_alone():
    assert with_previous_question("What are her NLP skills?", "Has Kerry worked in NLP?") == "What are her NLP skills?"


def test_follow_up_without_a_previous_question_is_asked_alone():
    assert with_previous_question("Tell me more", None) == "Tell me more"


def test_follow_up_is_asked_alone_when_the_two_questions_are_too_long():
    previous = "x" * MAX_QUESTION_CHARS
    assert with_previous_question("More details?", previous) == "More details?"
