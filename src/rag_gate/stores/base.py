"""The VectorStore interface every retrieval backend implements.

See docs/adr/0001-domain-agnostic-core.md — rag-gate's core depends only
on this Protocol, never on a specific vector database's client.
"""

from __future__ import annotations

from typing import Protocol

from rag_gate.schemas import Chunk


class VectorStore(Protocol):
    """Minimal surface rag-gate needs from any vector backend."""

    def add(self, chunks: list[Chunk]) -> None:
        """Index ``chunks`` for later retrieval."""
        ...

    def query(self, text: str, *, top_k: int = 5, topic: str | None = None) -> list[Chunk]:
        """Return the ``top_k`` chunks most relevant to ``text``.

        When ``topic`` is given, results are restricted to chunks whose
        document is mapped to that topic in the coverage map.
        """
        ...
