"""Local Ollama implementation of LLMProvider. Lands in Phase 1."""

from __future__ import annotations


class OllamaProvider:
    def __init__(
        self,
        model: str = "qwen2.5:7b-instruct-q4_K_M",
        host: str = "http://localhost:11434",
    ) -> None:
        self.model = model
        self.host = host

    def generate(self, prompt: str, *, temperature: float = 0.1) -> str:
        raise NotImplementedError("Phase 1")
