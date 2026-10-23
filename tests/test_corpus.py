from pathlib import Path

import pytest
import yaml

from resumebot.corpus import (
    CorpusError,
    chunks_from_document,
    load_corpus,
    parse_document,
    slugify,
    split_sections,
)

ROOT = Path(__file__).resolve().parents[1]

DOC = """---
id: exp-demo
title: Demo Role, Demo Corp
status: approved
source_type: cv
sources:
  - CV (2026)
section_sources:
  about-demo-corp:
    - Demo Corp website
open_questions: []
---

## Role overview
Kheirie worked at Demo Corp.

## About Demo Corp
Demo Corp makes demos.
"""


# --- slugify -----------------------------------------------------------------


@pytest.mark.parametrize(
    "heading, expected",
    [
        ("Role overview", "role-overview"),
        ("Designing master's-level AI courses", "designing-masters-level-ai-courses"),
        (
            "BSc and MSc in Computer & Communication Engineering",
            "bsc-and-msc-in-computer-communication-engineering",
        ),
        ("Interests: writing", "interests-writing"),
        ("  Spaces   and -- hyphens  ", "spaces-and-hyphens"),
    ],
)
def test_slugify(heading, expected):
    assert slugify(heading) == expected


# --- parse_document and split_sections ---------------------------------------


def test_parse_document_splits_frontmatter_from_body():
    meta, body = parse_document(DOC)
    assert meta["id"] == "exp-demo"
    assert body.strip().startswith("## Role overview")


def test_parse_document_rejects_missing_frontmatter():
    with pytest.raises(CorpusError):
        parse_document("## Just a heading\nSome text.\n")


def test_split_sections_returns_headings_and_text_in_order():
    _, body = parse_document(DOC)
    assert split_sections(body) == [
        ("Role overview", "Kheirie worked at Demo Corp."),
        ("About Demo Corp", "Demo Corp makes demos."),
    ]


def test_split_sections_rejects_text_before_first_heading():
    with pytest.raises(CorpusError):
        split_sections("Orphan text that would be silently lost.\n\n## Heading\nBody.\n")


def test_split_sections_rejects_empty_section():
    with pytest.raises(CorpusError):
        split_sections("## Empty\n\n## Full\nBody.\n")


# --- chunks_from_document -----------------------------------------------------


def test_chunks_get_ids_and_default_sources():
    meta, body = parse_document(DOC)
    first = chunks_from_document(meta, body)[0]
    assert first.id == "exp-demo#role-overview"
    assert first.doc_title == "Demo Role, Demo Corp"
    assert first.source_type == "cv"
    assert first.sources == ("CV (2026)",)


def test_section_keywords_attach_to_their_section_only():
    meta, body = parse_document(DOC)
    meta["section_keywords"] = {"role-overview": ["employment", "work history"]}
    role, about = chunks_from_document(meta, body)
    assert role.keywords == ("employment", "work history")
    assert about.keywords == ()
    assert "employment" not in role.text  # keywords never become part of the section text


def test_section_sources_override_document_sources():
    meta, body = parse_document(DOC)
    about = chunks_from_document(meta, body)[1]
    assert about.id == "exp-demo#about-demo-corp"
    assert about.sources == ("Demo Corp website",)


@pytest.mark.parametrize(
    "break_rule",
    [
        lambda meta: meta.pop("sources"),
        lambda meta: meta.update(status="draft"),
        lambda meta: meta.update(open_questions=["Still unresolved?"]),
        lambda meta: meta.update(section_sources={"no-such-heading": ["x"]}),
        lambda meta: meta.update(section_keywords={"no-such-heading": ["x"]}),
        lambda meta: meta.update(section_keywords={"role-overview": "nlp, data science"}),
    ],
    ids=[
        "missing-key",
        "not-approved",
        "open-questions",
        "typo-in-section-sources",
        "typo-in-section-keywords",
        "keywords-not-a-list",
    ],
)
def test_invalid_documents_are_rejected(break_rule):
    meta, body = parse_document(DOC)
    break_rule(meta)
    with pytest.raises(CorpusError):
        chunks_from_document(meta, body)


# --- load_corpus ----------------------------------------------------------------


def test_load_corpus_reads_only_markdown_files(tmp_path):
    (tmp_path / "demo.md").write_text(DOC, encoding="utf-8")
    (tmp_path / "golden.yaml").write_text("not: corpus\n", encoding="utf-8")
    assert [c.id for c in load_corpus(tmp_path)] == [
        "exp-demo#role-overview",
        "exp-demo#about-demo-corp",
    ]


def test_load_corpus_rejects_duplicate_chunk_ids(tmp_path):
    (tmp_path / "a.md").write_text(DOC, encoding="utf-8")
    (tmp_path / "b.md").write_text(DOC, encoding="utf-8")
    with pytest.raises(CorpusError):
        load_corpus(tmp_path)


# --- integrity of the real corpus and eval set --------------------------------------


def test_real_corpus_loads_without_errors():
    chunks = load_corpus(ROOT / "corpus" / "approved")
    assert chunks
    assert all(c.text for c in chunks)


def test_every_golden_expected_source_exists():
    ids = {c.id for c in load_corpus(ROOT / "corpus" / "approved")}
    golden = yaml.safe_load((ROOT / "evals" / "golden.yaml").read_text(encoding="utf-8"))
    missing = [
        (item["question"], source)
        for item in golden
        for source in item.get("expected_sources", [])
        if source not in ids
    ]
    assert missing == []


def test_every_heldout_expected_source_exists():
    ids = {c.id for c in load_corpus(ROOT / "corpus" / "approved")}
    heldout = yaml.safe_load((ROOT / "evals" / "heldout.yaml").read_text(encoding="utf-8"))
    missing = [
        (item["question"], source)
        for item in heldout
        for source in item.get("expected_sources", [])
        if source not in ids
    ]
    assert missing == []


def test_heldout_questions_are_not_golden_questions():
    # A held-out question that is also in the golden set has been tuned on, so it measures nothing new.
    def questions(name):
        items = yaml.safe_load((ROOT / "evals" / name).read_text(encoding="utf-8"))
        return {" ".join(i["question"].lower().split()) for i in items}

    assert questions("heldout.yaml") & questions("golden.yaml") == set()


def test_overview_sections_exist_in_the_real_corpus():
    from resumebot.retrieval import OVERVIEW_CHUNK_IDS

    ids = {c.id for c in load_corpus(ROOT / "corpus" / "approved")}
    assert set(OVERVIEW_CHUNK_IDS) <= ids  # renaming a profile heading must update the overview route


# The about.md summary sections repeat facts from the role files so that list questions retrieve
# one complete chunk. Each phrase must appear in both chunks: editing one side alone fails here.
SUMMARY_FACTS = [
    ("about#data-science-roles", "exp-quantcube#role-overview", "Junior Data Scientist"),
    ("about#data-science-roles", "exp-quantcube#role-overview", "October 2023 to October 2025"),
    ("about#data-science-roles", "exp-sanofi#role-overview", "NLP Data Scientist"),
    ("about#data-science-roles", "exp-sanofi#role-overview", "November 2021 to March 2022"),
    ("about#data-science-roles", "exp-sanofi#role-overview", "research and development (R&D) NLP team"),
    ("about#data-science-roles", "exp-braincities#role-overview", "Braincities Lab in Paris, France"),
    ("about#data-science-roles", "exp-braincities#role-overview", "August 2020 to August 2021"),
    ("about#nlp-projects", "exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis", "within the NLP team"),
    ("about#nlp-projects", "exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis", "80% correlation with the official Egyptian PMI"),
    ("about#nlp-projects", "exp-quantcube#pmi-nowcasting-with-arabic-and-english-sentiment-analysis", "88% correlation with the official Saudi Arabian PMI"),
    ("about#nlp-projects", "exp-quantcube#agentic-rag-research-tool-for-explaining-indicators", "within the NLP team"),
    ("about#nlp-projects", "exp-sanofi#extractive-summarization-of-medicine-and-drug-documents", "ROUGE-1 score of 47%"),
    ("about#nlp-projects", "exp-sanofi#extractive-summarization-of-medicine-and-drug-documents", "ROUGE-2 score of 25%"),
    ("about#nlp-projects", "exp-braincities#job-matching-project-for-enel", "NLP-based"),
    ("about#nlp-projects", "exp-braincities#job-matching-project-for-enel", "90% accuracy"),
    ("about#teaching-coaching-and-education-roles", "exp-tfl-fellow#role-overview", "July 2014 to July 2016"),
    ("about#teaching-coaching-and-education-roles", "exp-tfl-fellow#teaching-mathematics-and-computer-subjects-in-primary-school", "Grades 1 to 6"),
    ("about#teaching-coaching-and-education-roles", "exp-tfl-mentor#role-overview", "October to December 2016"),
    ("about#teaching-coaching-and-education-roles", "exp-tfl-mentor#coaching-and-supervising-teaching-fellows", "13 teaching fellows"),
    ("about#teaching-coaching-and-education-roles", "exp-simey#role-overview", "September to October 2017"),
    ("about#teaching-coaching-and-education-roles", "exp-simey#english-course-design-for-syrian-refugee-learners", "9 Syrian refugee learners"),
    ("about#teaching-coaching-and-education-roles", "exp-akureyri-curriculum#role-overview", "July 2026"),
    ("about#teaching-coaching-and-education-roles", "exp-akureyri-curriculum#designing-masters-level-ai-courses", "still in development"),
    ("about#degrees", "edu-dsti#applied-msc-in-data-science-artificial-intelligence", "Applied MSc in Data Science & Artificial Intelligence"),
    ("about#degrees", "edu-dsti#applied-msc-in-data-science-artificial-intelligence", "September 2023 to December 2025"),
    ("about#degrees", "edu-akureyri#ma-by-research-in-social-sciences", "University of Akureyri"),
    ("about#degrees", "edu-akureyri#ma-by-research-in-social-sciences", "September 2017 to February 2019"),
    ("about#degrees", "edu-rhu#bsc-and-msc-in-computer-communication-engineering", "January 2012 to December 2013"),
    ("about#degrees", "edu-rhu#bsc-and-msc-in-computer-communication-engineering", "September 2008 to December 2011"),
]


@pytest.mark.parametrize("summary_id, source_id, phrase", SUMMARY_FACTS)
def test_summary_sections_match_their_source_sections(summary_id, source_id, phrase):
    by_id = {c.id: c.text for c in load_corpus(ROOT / "corpus" / "approved")}
    assert phrase in by_id[summary_id], f"{phrase!r} missing from {summary_id}"
    assert phrase in by_id[source_id], f"{phrase!r} missing from {source_id}"


# Kheirie's rule (2026-10-16): career answers go from the most recent role to the oldest. Models
# copy the order they read, so the summary sections are written in that order too.
NEWEST_FIRST = [
    ("about#data-science-roles", ["QuantCube Technology", "Sanofi", "Braincities Lab"]),
    ("about#nlp-projects", ["QuantCube Technology", "Sanofi", "Braincities Lab"]),
    (
        "about#teaching-coaching-and-education-roles",
        ["University of Akureyri", "SÍMEY", "Temporary Educational Mentor", "a Fellow from July 2014"],
    ),
    ("about#degrees", ["September 2023", "September 2017", "January 2012", "September 2008"]),
]


@pytest.mark.parametrize("summary_id, newest_to_oldest", NEWEST_FIRST)
def test_summary_sections_list_the_most_recent_role_first(summary_id, newest_to_oldest):
    text = {c.id: c.text for c in load_corpus(ROOT / "corpus" / "approved")}[summary_id]
    positions = [text.index(name) for name in newest_to_oldest]
    assert positions == sorted(positions)
