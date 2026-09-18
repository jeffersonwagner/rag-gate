"""The documentary coverage map: the gate's single source of truth.

A coverage map is a plain ``topic -> [document ids]`` mapping. It is meant
to be small enough to be hand-edited by a domain expert who is not a
programmer — see docs/architecture.md.

Full implementation lands in Phase 1 (see docs/architecture.md's roadmap).
"""

from __future__ import annotations


class CoverageMap:
    """Loads and queries a topic -> documents coverage map."""

    def __init__(self, mapping: dict[str, list[str]] | None = None) -> None:
        self._mapping = mapping or {}

    def has_coverage(self, topic: str) -> bool:
        """Return True if at least one document is mapped to ``topic``."""
        return bool(self._mapping.get(topic))

    def documents_for(self, topic: str) -> list[str]:
        """Return the document ids mapped to ``topic``, if any."""
        return list(self._mapping.get(topic, []))

    @classmethod
    def from_file(cls, path: str) -> CoverageMap:
        raise NotImplementedError("YAML/JSON loading lands in Phase 1")
