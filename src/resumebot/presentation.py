"""Turn an Answer into the Markdown a recruiter sees.

Kept out of app.py so the formatting is tested without starting a web server.
Only the answer text is shown (Kheirie's choice, 2026-10-16). Citations are still
required and validated in `answering.py`, and the eval reports list them.
"""

from __future__ import annotations

from resumebot.answering import Answer


def format_answer(answer: Answer, show_model: bool = False) -> str:
    """The answer text; with show_model, a line saying which model wrote it.

    The line also says when a fallback answered (and which providers failed first),
    when the answer came from the cache, and which models failed when none answered.
    """
    if not show_model:
        return answer.text
    if answer.answered_by:
        provider, _, model = answer.answered_by.partition(":")
        parts = [f"Model: {model} ({provider})"]
        if answer.fallback_from:
            parts.append("fallback after " + "; ".join(answer.fallback_from))
        if answer.from_cache:
            parts.append("from cache")
        return f"{answer.text}\n\n*{' · '.join(parts)}*"
    if answer.fallback_from:  # every provider failed
        return f"{answer.text}\n\n*All models failed: {'; '.join(answer.fallback_from)}*"
    return answer.text  # retrieval abstentions and refusals never reach a model
