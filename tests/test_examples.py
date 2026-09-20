"""Runs the example demo scripts as subprocesses to catch regressions —
these are the first thing a new user tries, so they must never silently
break. ANTHROPIC_API_KEY is deliberately unset so both scripts take their
zero-setup path deterministically."""

import subprocess
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _run_example(name: str, env: dict) -> subprocess.CompletedProcess:
    script = EXAMPLES_DIR / name / "demo.py"
    return subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )


def _env_without_api_keys(monkeypatch) -> dict:
    import os

    env = dict(os.environ)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
        env.pop(key, None)
    return env


def test_helpdesk_bot_demo_runs_clean(monkeypatch):
    result = _run_example("helpdesk_bot", _env_without_api_keys(monkeypatch))

    assert result.returncode == 0, result.stderr
    assert "Gate decision: allowed=True" in result.stdout
    assert "Gate decision: allowed=False" in result.stdout
    assert "Set ANTHROPIC_API_KEY" in result.stdout


def test_compliance_qa_demo_runs_clean(monkeypatch):
    result = _run_example("compliance_qa", _env_without_api_keys(monkeypatch))

    assert result.returncode == 0, result.stderr
    assert "Gate decision: allowed=True" in result.stdout
    assert "Gate decision: allowed=False" in result.stdout
    assert "Set ANTHROPIC_API_KEY" in result.stdout
