"""Tests for the coverage map: the gate's single source of truth."""

import pytest

from rag_gate.coverage import CoverageError, CoverageMap


def test_from_file_loads_yaml(tmp_path):
    path = tmp_path / "coverage.yaml"
    path.write_text("billing:\n  - doc-1\n  - doc-2\npayroll: []\n")

    coverage = CoverageMap.from_file(path)

    assert coverage.has_coverage("billing") is True
    assert coverage.documents_for("billing") == ["doc-1", "doc-2"]
    assert coverage.has_coverage("payroll") is False


def test_from_file_loads_json(tmp_path):
    path = tmp_path / "coverage.json"
    path.write_text('{"billing": ["doc-1"]}')

    coverage = CoverageMap.from_file(path)

    assert coverage.documents_for("billing") == ["doc-1"]


def test_from_file_missing_file_raises(tmp_path):
    with pytest.raises(CoverageError, match="not found"):
        CoverageMap.from_file(tmp_path / "missing.yaml")


def test_from_file_rejects_non_mapping(tmp_path):
    path = tmp_path / "coverage.yaml"
    path.write_text("- billing\n- payroll\n")

    with pytest.raises(CoverageError, match="mapping"):
        CoverageMap.from_file(path)


def test_from_file_rejects_non_list_value(tmp_path):
    path = tmp_path / "coverage.yaml"
    path.write_text("billing: doc-1\n")

    with pytest.raises(CoverageError, match="list of document id strings"):
        CoverageMap.from_file(path)


def test_from_file_rejects_malformed_yaml(tmp_path):
    path = tmp_path / "coverage.yaml"
    path.write_text("billing: [unclosed\n")

    with pytest.raises(CoverageError, match="Could not parse"):
        CoverageMap.from_file(path)


def test_topics_excludes_empty_entries():
    coverage = CoverageMap({"billing": ["doc-1"], "payroll": []})
    assert coverage.topics() == ["billing"]
