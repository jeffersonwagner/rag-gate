"""Tests for the hallucination-rate benchmark script — a regression guard
on the exact numbers the README/docs quote."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from benchmark import OUT_OF_SCOPE_QUESTIONS, run  # noqa: E402


def test_gate_refuses_every_out_of_scope_question():
    results = run()

    assert len(results) == len(OUT_OF_SCOPE_QUESTIONS)
    assert all(not r.gated_answered for r in results)


def test_naive_chunk_is_always_returned_regardless_of_relevance():
    # There's exactly one (unrelated) chunk in the benchmark's index, so a
    # naive, un-gated pipeline retrieves and would answer from it for every
    # question, illustrating why "no gate" means "no refusal path" at all.
    results = run()

    assert all(r.naive_chunk_text for r in results)
