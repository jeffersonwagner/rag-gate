"""sentence-transformers implementation of Embedder (local, offline).

Default embedding backend — no API key required. Lands in Phase 1.
"""

from __future__ import annotations


class SentenceTransformersEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("Phase 1")
