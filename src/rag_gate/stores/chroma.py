"""Chroma implementation of VectorStore. Lands in Phase 1."""

from __future__ import annotations

from rag_gate.schemas import Chunk


class ChromaStore:
    def __init__(self, collection_name: str = "rag_gate", persist_dir: str | None = None) -> None:
        self.collection_name = collection_name
        self.persist_dir = persist_dir

    def add(self, chunks: list[Chunk]) -> None:
        raise NotImplementedError("Phase 1")

    def query(self, text: str, *, top_k: int = 5, topic: str | None = None) -> list[Chunk]:
        raise NotImplementedError("Phase 1")
