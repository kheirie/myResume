"""Load approved corpus files and split them into citable chunks.

Each `## ` section of a corpus file becomes one Chunk. The chunk ID
("<doc id>#<heading slug>") is the citation key the bot shows recruiters,
so the rules here are strict: a file that breaks them raises CorpusError
instead of being silently skipped or half-loaded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

REQUIRED_KEYS = ("id", "title", "status", "source_type", "sources")


class CorpusError(ValueError):
    """Raised when a corpus file breaks the corpus rules."""


@dataclass(frozen=True)
class Chunk:
    id: str  # "<doc id>#<heading slug>": the citation key
    doc_id: str
    doc_title: str
    heading: str
    text: str
    source_type: str  # "cv" or "article"
    sources: tuple[str, ...]


def slugify(heading: str) -> str:
    """Turn a heading into a URL-style slug.

    Lowercase; remove punctuation except hyphens; turn runs of whitespace
    into a single hyphen; collapse repeated hyphens; trim hyphens at the ends.
    Example: "Designing master's-level AI courses" -> "designing-masters-level-ai-courses"
    """
    s = heading.lower() # lowercase
    s = re.sub(r"[^\w\s-]", "", s) # remove punctuation except hyphens
    s = re.sub(r"\s+", "-", s.strip()) #runs of whitespace into a single hyphen
    s = re.sub(r"-+", "-", s) # collapse repeated hyphens
    return s.strip("-") # trim hyphens at the ends
    


def parse_document(raw: str) -> tuple[dict, str]:
    """Split a Markdown file into (frontmatter dict, body).

    The file must start with a line "---", followed by YAML, followed by a
    closing "---" line. Use yaml.safe_load. Raise CorpusError if the
    frontmatter is missing or does not parse to a dict.
    """
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if not m:
        raise CorpusError("file must start with a '---' frontmatter block")
    meta = yaml.safe_load(m.group(1))
    if not isinstance(meta, dict):
        raise CorpusError("frontmatter must be a YAML mapping (key: value lines)")
    return meta, m.group(2)


def split_sections(body: str) -> list[tuple[str, str]]:
    """Return (heading, text) for each "## " section, in order.

    Text is stripped of surrounding whitespace. Raise CorpusError if there is
    non-blank text before the first heading, or if a section is empty.
    """
    # With a capturing group, re.split keeps the headings:
    # [preamble, heading1, text1, heading2, text2, ...]
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    if parts[0].strip():
        raise CorpusError("text found before the first '## ' heading would be lost")
    sections = []
    for heading, text in zip(parts[1::2], parts[2::2]):
        if not text.strip():
            raise CorpusError(f"section '{heading.strip()}' is empty")
        sections.append((heading.strip(), text.strip()))
    return sections


def chunks_from_document(meta: dict, body: str) -> list[Chunk]:
    """Validate one document and turn its sections into Chunks.

    Rules (raise CorpusError if broken):
      - every key in REQUIRED_KEYS is present
      - status is "approved"
      - open_questions, if present, is empty
      - every key in section_sources matches the slug of a real heading
    A section's sources come from section_sources[slug] if present,
    otherwise from the document's `sources`.
    """
    missing = [key for key in REQUIRED_KEYS if key not in meta]
    if missing:
        raise CorpusError(f"missing required keys: {', '.join(missing)}")
    if meta["status"] != "approved":
        raise CorpusError(f"status is '{meta['status']}', expected 'approved'")
    if meta.get("open_questions"):
        raise CorpusError("open_questions must be resolved before approval")

    sections = split_sections(body)
    slugs = [slugify(heading) for heading, _ in sections]
    overrides = meta.get("section_sources") or {}
    unknown = set(overrides) - set(slugs)
    if unknown:
        raise CorpusError(f"section_sources keys match no heading: {', '.join(sorted(unknown))}")

    return [
        Chunk(
            id=f"{meta['id']}#{slug}",
            doc_id=meta["id"],
            doc_title=meta["title"],
            heading=heading,
            text=text,
            source_type=meta["source_type"],
            sources=tuple(overrides.get(slug, meta["sources"])),
        )
        for (heading, text), slug in zip(sections, slugs)
    ]


def load_corpus(directory: Path) -> list[Chunk]:
    """Load every *.md file in `directory` (sorted by name) into Chunks.

    Raise CorpusError if two chunks share an ID. Include the file name in
    error messages so a broken file is easy to find.
    """
    chunks: list[Chunk] = []
    seen: dict[str, str] = {}  # chunk id -> file it came from
    for path in sorted(directory.glob("*.md")):
        try:
            meta, body = parse_document(path.read_text(encoding="utf-8"))
            doc_chunks = chunks_from_document(meta, body)
        except CorpusError as err:
            raise CorpusError(f"{path.name}: {err}") from err
        for chunk in doc_chunks:
            if chunk.id in seen:
                raise CorpusError(f"{path.name}: duplicate chunk id {chunk.id} (also in {seen[chunk.id]})")
            seen[chunk.id] = path.name
        chunks.extend(doc_chunks)
    return chunks
