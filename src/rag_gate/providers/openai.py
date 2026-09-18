"""OpenAI implementation of LLMProvider. Lands in Phase 1."""

from __future__ import annotations


class OpenAIProvider:
    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key

    def generate(self, prompt: str, *, temperature: float = 0.1) -> str:
        raise NotImplementedError("Phase 1")
