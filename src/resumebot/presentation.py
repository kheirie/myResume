"""Turn an Answer into the Markdown a recruiter sees.

Kept out of app.py so the formatting is tested without starting a web server.
"""

from __future__ import annotations

from resumebot.answering import Answer


def format_answer(answer: Answer) -> str:
    """The answer text, followed by the sources it is based on."""
    if not answer.citations:
        return answer.text
    lines = [answer.text, "", "**Sources**"]
    for chunk in answer.citations:
        lines.append(f"- *{chunk.heading}* · {chunk.doc_title} · {'; '.join(chunk.sources)}")
    return "\n".join(lines)
