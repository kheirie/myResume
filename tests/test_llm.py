import pytest

from resumebot.llm import FallbackLLM, LLMConfigError, LLMSettings, LLMUnavailable, Usage, build_llm


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, tmp_path):
    # Run from an empty folder so the real .env is never read, and clear related variables.
    monkeypatch.chdir(tmp_path)
    names = ("LLM_PROVIDER", "LLM_FALLBACK_ORDER", "OLLAMA_BASE_URL", "OLLAMA_MODEL")
    for name in names + ("GROQ_API_KEY", "GROQ_MODEL", "HF_TOKEN", "HF_MODEL"):
        monkeypatch.delenv(name, raising=False)


def test_defaults_to_local_ollama():
    settings = LLMSettings.for_provider()
    assert settings.provider == "ollama"
    assert settings.base_url == "http://localhost:11434/v1"
    assert settings.model == "llama3.1:8b"


def test_llm_provider_variable_selects_the_default(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    assert LLMSettings.for_provider().provider == "groq"


def test_groq_uses_its_key_and_model(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("GROQ_MODEL", "some-model")
    settings = LLMSettings.for_provider("groq")
    assert settings.api_key == "test-key"
    assert settings.model == "some-model"
    assert settings.base_url == "https://api.groq.com/openai/v1"


def test_groq_without_a_key_fails_with_a_clear_message():
    with pytest.raises(LLMConfigError, match="GROQ_API_KEY"):
        LLMSettings.for_provider("groq")


def test_unknown_provider_is_rejected():
    with pytest.raises(LLMConfigError, match="unknown provider"):
        LLMSettings.for_provider("openai")


def test_huggingface_uses_the_router_and_the_same_model_as_groq(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "hf-test")
    settings = LLMSettings.for_provider("huggingface")
    assert settings.base_url == "https://router.huggingface.co/v1"
    assert settings.model == "openai/gpt-oss-120b"


class FakeProvider:
    def __init__(self, label, reply=None):
        self.label = label
        self.reply = reply
        self.calls = 0
        self.last_usage = Usage(100, 10) if reply is not None else None

    def complete_json(self, system, user):
        self.calls += 1
        if self.reply is None:
            raise LLMUnavailable(f"{self.label}: RateLimitError")
        return self.reply


def test_fallback_uses_the_first_provider_that_answers():
    busy, ok, unused = FakeProvider("groq"), FakeProvider("hf", '{"ok": 1}'), FakeProvider("ollama", "{}")
    chain = FallbackLLM([busy, ok, unused])
    assert chain.complete_json("s", "u") == '{"ok": 1}'
    assert chain.last_used == "hf"
    assert chain.failures == ["groq: RateLimitError"]
    assert unused.calls == 0  # stops at the first success


def test_fallback_raises_when_every_provider_fails():
    chain = FallbackLLM([FakeProvider("groq"), FakeProvider("hf")])
    with pytest.raises(LLMUnavailable, match="every provider failed"):
        chain.complete_json("s", "u")
    assert chain.last_used is None


def test_chain_skips_providers_without_a_key(monkeypatch):
    monkeypatch.setenv("LLM_FALLBACK_ORDER", "groq,huggingface,ollama")
    monkeypatch.setenv("HF_TOKEN", "hf-test")  # no GROQ_API_KEY
    chain = build_llm("chain")
    assert chain.label == "chain(huggingface:openai/gpt-oss-120b > ollama:llama3.1:8b)"


def test_fallback_reports_the_usage_of_the_provider_that_answered():
    chain = FallbackLLM([FakeProvider("groq"), FakeProvider("hf", "{}")])
    chain.complete_json("s", "u")
    assert chain.last_usage == Usage(100, 10)


def test_usage_adds_up():
    assert Usage(1, 2) + Usage(10, 20) == Usage(11, 22)
