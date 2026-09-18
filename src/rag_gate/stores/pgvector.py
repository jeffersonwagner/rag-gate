"""pgvector implementation of VectorStore. Lands in Phase 1."""

from __future__ import annotations

from rag_gate.schemas import Chunk


class PgVectorStore:
    def __init__(self, dsn: str, table: str = "rag_gate_chunks") -> None:
        self.dsn = dsn
        self.table = table

    def add(self, chunks: list[Chunk]) -> None:
        raise NotImplementedError("Phase 1")

    def query(self, text: str, *, top_k: int = 5, topic: str | None = None) -> list[Chunk]:
        raise NotImplementedError("Phase 1")
