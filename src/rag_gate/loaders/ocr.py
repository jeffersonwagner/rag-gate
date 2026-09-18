"""OCR fallback for scanned pages, used by loaders/pdf.py. Lands in Phase 1."""

from __future__ import annotations


def ocr_page(image_path: str, *, lang: str = "eng") -> str:
    raise NotImplementedError("Phase 1")
