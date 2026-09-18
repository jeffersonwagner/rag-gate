# Contributing

Thanks for your interest in `rag-gate`. The project is in **Phase 0 /
Phase 1** — the core API (`gate.py`, `guardrails.py`, the provider/store/
embedding interfaces) is still being designed, so it isn't ready for
external contributions yet.

Once the core lands (see [`docs/architecture.md`](docs/architecture.md) for
the roadmap), this file will describe:

- how to set up a dev environment (`uv sync --all-extras`)
- coding style (`ruff`, enforced in CI)
- how to add a new provider / vector store / embedding backend
- how PRs are reviewed

Until then, feel free to open an issue with feedback or questions.

## Development setup

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
```

## Commit style

This project uses [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:`, `chore:`, …) to keep the changelog generatable.
