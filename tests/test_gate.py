"""Unit tests for the documentary gate — the core guarantee of rag-gate:
without coverage, the caller must never proceed to call an LLM."""

from rag_gate.coverage import CoverageMap
from rag_gate.gate import DocumentGate


def test_allows_documented_topic():
    gate = DocumentGate(CoverageMap({"billing": ["doc-1"]}))
    decision = gate.check("billing")
    assert decision.allowed is True
    assert decision.reason == "documented"
    assert decision.missing_documents_hint is None


def test_refuses_undocumented_topic():
    gate = DocumentGate(CoverageMap({"billing": ["doc-1"]}))
    decision = gate.check("payroll")
    assert decision.allowed is False
    assert decision.reason == "no_documentation"
    assert "payroll" in decision.missing_documents_hint


def test_refuses_topic_mapped_to_no_documents():
    # A topic present in the map but with an empty document list is
    # indistinguishable from "not covered" — coverage means at least one
    # real document, not just a key in the map.
    gate = DocumentGate(CoverageMap({"payroll": []}))
    decision = gate.check("payroll")
    assert decision.allowed is False
