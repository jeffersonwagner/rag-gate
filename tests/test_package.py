"""Phase 0 sanity checks: the package imports and its skeleton holds together."""

from typer.testing import CliRunner

from rag_gate import __version__
from rag_gate.cli import app

runner = CliRunner()


def test_version_is_set():
    assert __version__ == "0.0.1"


def test_cli_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_doctor_command():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
