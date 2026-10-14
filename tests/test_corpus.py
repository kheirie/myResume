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
    ],
    ids=["missing-key", "not-approved", "open-questions", "typo-in-section-sources"],
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
