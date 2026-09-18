"""PDF document loader, with automatic OCR fallback (see loaders/ocr.py).

A scanned PDF has no extractable text layer; falling back to OCR
automatically (rather than as a manual step) avoids the silent failure of
"this document quietly never gets indexed." Lands in Phase 1.
"""

from __future__ import annotations

from rag_gate.schemas import Document


def load_pdf(path: str, *, ocr_fallback: bool = True) -> Document:
    raise NotImplementedError("Phase 1")
