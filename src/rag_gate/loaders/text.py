"""Plain-text document loader. Lands in Phase 1."""

from __future__ import annotations

from rag_gate.schemas import Document


def load_text(path: str) -> Document:
    raise NotImplementedError("Phase 1")
