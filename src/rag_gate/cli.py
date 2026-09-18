"""rag-gate command-line interface.

`init`, `ingest`, and `ask` land in Phase 2, once the core pipeline
(gate + retriever + guardrails) is implemented. `doctor` and `version` are
available from Phase 0 as basic sanity checks.
"""

from __future__ import annotations

import typer

from rag_gate import __version__

app = typer.Typer(help="A hard documentary gate and citation verifier for RAG pipelines.")


@app.command()
def version() -> None:
    """Print the installed rag-gate version."""
    typer.echo(__version__)


@app.command()
def doctor() -> None:
    """Check that rag-gate is installed correctly."""
    typer.echo(f"rag-gate {__version__} — core package importable, no core pipeline yet (Phase 1).")


@app.command()
def init() -> None:
    """Scaffold a new rag-gate project (coverage map, config). Lands in Phase 2."""
    raise NotImplementedError("Phase 2")


@app.command()
def ingest(path: str) -> None:
    """Ingest documents from PATH into the configured vector store. Lands in Phase 2."""
    raise NotImplementedError("Phase 2")


@app.command()
def ask(question: str) -> None:
    """Ask a question through the gated pipeline. Lands in Phase 2."""
    raise NotImplementedError("Phase 2")


if __name__ == "__main__":
    app()
