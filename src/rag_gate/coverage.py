"""The documentary coverage map: the gate's single source of truth.

A coverage map is a plain ``topic -> [document ids]`` mapping. It is meant
to be small enough to be hand-edited by a domain expert who is not a
programmer — see docs/architecture.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


class CoverageError(ValueError):
    """Raised when a coverage map file is malformed."""


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

    def topics(self) -> list[str]:
        """Return every topic with at least one document mapped to it."""
        return [topic for topic, documents in self._mapping.items() if documents]

    @classmethod
    def from_file(cls, path: str | Path) -> CoverageMap:
        """Load a coverage map from a YAML or JSON file.

        The file must contain a mapping of ``topic -> [document ids]``.
        Malformed content raises :class:`CoverageError` rather than failing
        silently or half-loading — a broken coverage map must never be
        mistaken for an empty (and therefore fully-refusing) one.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise CoverageError(f"Coverage map file not found: {file_path}")

        raw = file_path.read_text(encoding="utf-8")
        try:
            if file_path.suffix.lower() == ".json":
                data = json.loads(raw)
            else:
                data = yaml.safe_load(raw)
        except (json.JSONDecodeError, yaml.YAMLError) as exc:
            raise CoverageError(f"Could not parse coverage map {file_path}: {exc}") from exc

        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise CoverageError(
                f"Coverage map {file_path} must be a mapping of topic -> [documents], "
                f"got {type(data).__name__}"
            )

        mapping: dict[str, list[str]] = {}
        for topic, documents in data.items():
            if not isinstance(topic, str):
                raise CoverageError(f"Coverage map {file_path}: topic keys must be strings")
            if documents is None:
                mapping[topic] = []
                continue
            if not isinstance(documents, list) or not all(isinstance(d, str) for d in documents):
                raise CoverageError(
                    f"Coverage map {file_path}: topic '{topic}' must map to a list of "
                    "document id strings"
                )
            mapping[topic] = documents

        return cls(mapping)
