"""OpenAI implementation of Embedder. Lands in Phase 1."""

from __future__ import annotations


class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("Phase 1")
