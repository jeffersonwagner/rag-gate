# Contributing

Thanks for your interest in `rag-gate`. The core (Phase 1) is implemented
and tested — see [`docs/architecture.md`](docs/architecture.md) for what's
done and what's next. The CLI and runnable examples (Phase 2) are still
being built, so the project isn't taking large external contributions yet,
but feedback, bug reports, and small fixes are welcome.

Good places to help right now:

- `stores/pgvector.py` and `stores/qdrant.py` are typed stubs — a real
  implementation with a docker-compose-based integration test would be
  very welcome.
- Anything in `docs/adr/` you disagree with — open an issue with the
  alternative and the trade-off.

## Development setup

```bash
# Skips sentence-transformers on purpose — it pulls in a multi-GB PyTorch
# download. Add --extra sentence-transformers if you're touching that file.
uv sync --extra dev --extra anthropic --extra openai --extra ollama --extra chroma --extra pdf
uv run pytest
uv run ruff check .
uv run mypy src/rag_gate
```

## Adding a new provider / store / embedder

Implement the relevant `Protocol` in `providers/base.py`, `stores/base.py`,
or `embeddings/base.py`. Import the vendor SDK lazily (inside `__init__` or
the method that needs it, not at module level) and raise `ImportError` with
a message naming the extra to install — see any existing implementation
(e.g. `providers/anthropic.py`) for the pattern. Add the SDK as a new
optional dependency in `pyproject.toml`, and mock the SDK client in tests
rather than calling the real API (see `tests/test_providers.py`).

## Commit style

This project uses [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:`, `chore:`, …) to keep the changelog generatable.
