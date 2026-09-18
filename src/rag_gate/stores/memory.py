"""In-memory VectorStore — exact cosine similarity, no external dependency.

Reference implementation for tests and for trying rag-gate without a real
vector database. Full implementation lands in Phase 1.
"""

from __future__ import annotations

from rag_gate.schemas import Chunk


class InMemoryStore:
    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def add(self, chunks: list[Chunk]) -> None:
        self._chunks.extend(chunks)

    def query(self, text: str, *, top_k: int = 5, topic: str | None = None) -> list[Chunk]:
        raise NotImplementedError("Embedding-based similarity lands in Phase 1")
