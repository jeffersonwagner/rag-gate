"""Wires a VectorStore to the DocumentGate.

Full implementation (top-k retrieval, topic resolution) lands in Phase 1
once a reference VectorStore exists (see rag_gate.stores).
"""

from __future__ import annotations

from rag_gate.gate import DocumentGate
from rag_gate.schemas import Chunk, GateDecision


class GatedRetriever:
    """Retrieves chunks for a topic only if the gate allows it."""

    def __init__(self, gate: DocumentGate) -> None:
        self._gate = gate

    def retrieve(self, topic: str, query: str, top_k: int = 5) -> tuple[GateDecision, list[Chunk]]:
        decision = self._gate.check(topic)
        if not decision.allowed:
            return decision, []
        raise NotImplementedError("Vector retrieval lands in Phase 1")
