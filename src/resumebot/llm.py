"""One client for any OpenAI-compatible chat API.

Ollama (local, for development and evals) and Groq (hosted, for the public demo)
both speak the OpenAI chat API, so switching provider is a change in `.env`,
not in code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from dotenv import load_dotenv


class LLM(Protocol):
    def complete_json(self, system: str, user: str) -> str:
        """Return the model's reply, asked to be a single JSON object."""
        ...


@dataclass(frozen=True)
class LLMSettings:
    base_url: str
    model: str
    api_key: str

    @classmethod
    def from_env(cls) -> LLMSettings:
        """Read LLM_BASE_URL, LLM_MODEL and LLM_API_KEY; default to local Ollama."""
        load_dotenv()
        return cls(
            base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
            model=os.environ.get("LLM_MODEL", "llama3.1:8b"),
            api_key=os.environ.get("LLM_API_KEY", "ollama"),  # Ollama ignores the key
        )


class OpenAICompatibleLLM:
    def __init__(self, settings: LLMSettings | None = None, timeout: float = 120):
        from openai import OpenAI

        self.settings = settings or LLMSettings.from_env()
        self._client = OpenAI(base_url=self.settings.base_url, api_key=self.settings.api_key, timeout=timeout)

    def complete_json(self, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=self.settings.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,  # same question, same answer: needed for trust and for evals
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content or ""
