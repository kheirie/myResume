"""Turn an Answer into the Markdown a recruiter sees.

Kept out of app.py so the formatting is tested without starting a web server.
Only the answer text is shown (Kheirie's choice, 2026-10-16). Citations are still
required and validated in `answering.py`, and the eval reports list them.
"""

from __future__ import annotations

import re
from dataclasses import replace

from resumebot.answering import Answer

# The web chat calls the candidate Kerry, how Kheirie is pronounced (Kheirie, 2026-10-23).
# The name is swapped here, not in the prompt: prompt v15 asked the model to write Kerry
# and lost quality (25/37 expected sources vs 30/38 for v14 on Ollama).
_CANDIDATE_NAME = re.compile(r"\bKheirie(?: El Hariri)?\b")
DISPLAY_NAME = "Kerry"
CACHED_NOTE = (
    "This question was answered earlier, so this is the saved answer. "
    "It doesn't count toward your AI answers."
)


def use_display_name(text: str) -> str:
    """Kheirie (and the full name) becomes Kerry; "Kheirie's" becomes "Kerry's"."""
    return _CANDIDATE_NAME.sub(DISPLAY_NAME, text)


def format_answer(answer: Answer, show_model: bool = False) -> str:
    """The answer text; with show_model, a line saying which model wrote it.

    The line also says when a fallback answered (and which providers failed first),
    and which models failed when none answered. A cached answer always says so, because
    it is served even after the visitor's AI answers run out (Kheirie, 2026-10-24).
    Every answer says Kerry, passages included (Kheirie, 2026-10-24); only the name changes.
    """
    answer = replace(answer, text=use_display_name(answer.text))
    if answer.from_cache:
        answer = replace(answer, text=f"{answer.text}\n\n*{CACHED_NOTE}*")
    if not show_model:
        return answer.text
    if answer.answered_by:
        provider, _, model = answer.answered_by.partition(":")
        parts = [f"Model: {model} ({provider})"]
        if answer.fallback_from:
            parts.append("fallback after " + "; ".join(answer.fallback_from))
        return f"{answer.text}\n\n*{' · '.join(parts)}*"
    if answer.fallback_from:  # every provider failed
        return f"{answer.text}\n\n*All models failed: {'; '.join(answer.fallback_from)}*"
    return answer.text  # retrieval abstentions and refusals never reach a model
