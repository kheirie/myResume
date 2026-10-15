"""One client for any OpenAI-compatible chat API, plus a fallback chain.

Ollama (local), Groq and Hugging Face Inference Providers all speak the OpenAI
chat API, so a provider is just a base URL, a model name, and a key. Settings
live in `.env`; keys live in `raw/secrets.env`. `--provider` picks one per run,
or "chain" tries several in order when one is rate-limited or down.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv

PROVIDERS = ("ollama", "groq", "huggingface")
SECRETS_FILE = Path("raw/secrets.env")
DEFAULT_CHAIN = "groq,huggingface,ollama"


@dataclass(frozen=True)
class Usage:
    """Tokens used by one or more LLM calls."""

    prompt_tokens: int = 0  # what we send: system prompt + context + question
    completion_tokens: int = 0  # what the model writes, including hidden reasoning

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def __add__(self, other: Usage) -> Usage:
        return Usage(self.prompt_tokens + other.prompt_tokens, self.completion_tokens + other.completion_tokens)


class LLM(Protocol):
    label: str
    last_usage: Usage | None  # tokens used by the most recent call

    def complete_json(self, system: str, user: str) -> str:
        """Return the model's reply, asked to be a single JSON object.

        Raises LLMUnavailable when the provider cannot answer right now.
        """
        ...


class LLMConfigError(RuntimeError):
    """Raised when a provider is selected but not configured."""


class LLMUnavailable(RuntimeError):
    """The provider could not answer: rate limit, timeout, server error, bad model name."""


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    base_url: str
    model: str
    api_key: str

    @classmethod
    def for_provider(cls, provider: str | None = None) -> LLMSettings:
        """Settings for one provider, read from the environment, `.env` and `raw/secrets.env`.

        Without an explicit provider, LLM_PROVIDER decides, defaulting to local Ollama.
        """
        load_dotenv()  # settings in .env
        load_dotenv(SECRETS_FILE)  # keys kept privately in raw/ (git-ignored)
        provider = provider or os.environ.get("LLM_PROVIDER", "ollama")
        if provider == "ollama":
            return cls(
                provider="ollama",
                base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                model=os.environ.get("OLLAMA_MODEL", "llama3.1:8b"),
                api_key="ollama",  # Ollama ignores the key, but the client requires one
            )
        if provider == "groq":
            return cls(
                provider="groq",
                base_url="https://api.groq.com/openai/v1",
                model=os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b"),
                api_key=_require_key("GROQ_API_KEY"),
            )
        if provider == "huggingface":
            return cls(
                provider="huggingface",
                base_url="https://router.huggingface.co/v1",
                # Same model as Groq, so a fallback answer has the same quality.
                model=os.environ.get("HF_MODEL", "openai/gpt-oss-120b"),
                api_key=_require_key("HF_TOKEN"),
            )
        raise LLMConfigError(f"unknown provider {provider!r}; choose one of {', '.join(PROVIDERS)}")


def _require_key(name: str) -> str:
    key = os.environ.get(name, "")
    if not key:
        raise LLMConfigError(f"{name} is not set. Add it to raw/secrets.env (never commit or paste keys).")
    return key


class OpenAICompatibleLLM:
    def __init__(self, settings: LLMSettings | None = None, timeout: float = 120, max_retries: int = 6):
        from openai import OpenAI

        self.settings = settings or LLMSettings.for_provider()
        self.label = f"{self.settings.provider}:{self.settings.model}"
        self.last_usage: Usage | None = None
        self.rate_limit: dict[str, str] = {}  # latest x-ratelimit-* headers, if the provider sends them
        # The client waits and retries on HTTP 429 (rate limit) and 5xx errors.
        self._client = OpenAI(
            base_url=self.settings.base_url,
            api_key=self.settings.api_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def complete_json(self, system: str, user: str) -> str:
        from openai import APIError

        try:
            raw = self._client.chat.completions.with_raw_response.create(
                model=self.settings.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0,  # same question, same answer: needed for trust and for evals
                response_format={"type": "json_object"},
            )
        except APIError as err:  # every error the API client can raise
            raise LLMUnavailable(f"{self.label}: {type(err).__name__}") from err
        response = raw.parse()
        usage = response.usage
        self.last_usage = Usage(usage.prompt_tokens, usage.completion_tokens) if usage else None
        self.rate_limit = {k: v for k, v in raw.headers.items() if k.lower().startswith("x-ratelimit")}
        return response.choices[0].message.content or ""


class FallbackLLM:
    """Try providers in order; move to the next one when a provider is unavailable.

    Every model in the chain must pass the golden eval: a recruiter who hits a
    fallback should not get a worse bot.
    """

    def __init__(self, llms: list[LLM]):
        if not llms:
            raise LLMConfigError("the fallback chain has no configured provider")
        self._llms = llms
        self.label = "chain(" + " > ".join(llm.label for llm in llms) + ")"
        self.last_used: str | None = None  # which provider produced the latest reply
        self.last_usage: Usage | None = None
        self.rate_limit: dict[str, str] = {}
        self.failures: list[str] = []  # providers that failed during the latest call

    def complete_json(self, system: str, user: str) -> str:
        self.failures = []
        for llm in self._llms:
            try:
                reply = llm.complete_json(system, user)
            except LLMUnavailable as err:
                self.failures.append(str(err))
                continue
            self.last_used = llm.label
            self.last_usage = getattr(llm, "last_usage", None)
            self.rate_limit = getattr(llm, "rate_limit", {})
            return reply
        self.last_used = None
        raise LLMUnavailable("every provider failed: " + "; ".join(self.failures))


def build_llm(provider: str | None = None) -> LLM:
    """One provider by name, or "chain" for the fallback chain in LLM_FALLBACK_ORDER."""
    load_dotenv()
    provider = provider or os.environ.get("LLM_PROVIDER", "ollama")
    if provider != "chain":
        return OpenAICompatibleLLM(LLMSettings.for_provider(provider))
    llms = []
    for name in os.environ.get("LLM_FALLBACK_ORDER", DEFAULT_CHAIN).split(","):
        try:
            settings = LLMSettings.for_provider(name.strip())
        except LLMConfigError:
            continue  # no key for this provider: leave it out of the chain
        # Few retries per provider: switching is faster than waiting out a rate limit.
        llms.append(OpenAICompatibleLLM(settings, max_retries=1))
    return FallbackLLM(llms)
