# rag-gate

**A hard gate that stops your RAG from answering without evidence.**

[Leia em português](README.pt-BR.md)

> Status: early development (Phase 0 — scaffolding). Not yet published on PyPI.

## The problem

Most RAG (retrieval-augmented generation) pipelines always call the LLM, even
when retrieval finds nothing relevant. The model fills the gap with invented
information — confidently. In domains where a wrong answer has a real cost
(compliance, internal support, technical documentation, safety procedures),
that is not a UX bug, it is a liability.

## What rag-gate does

`rag-gate` is a small, opinionated Python library that adds two things on top
of whatever retrieval stack you already have:

1. **Documentary gate.** Before the LLM is ever called, `rag-gate` checks
   whether there is real coverage for the topic of the question, using an
   auditable `topic → documents` map that a non-engineer can read and edit.
   No coverage → the LLM is never called, and the caller gets an explicit
   "not documented, here's what to add" response instead of a guess.
2. **Verified citations.** Every factual claim the LLM makes must cite
   `[n]`. A verifier runs **after** generation and checks that every citation
   points to a chunk that was actually retrieved, flagging or stripping any
   claim that isn't traceable. A prompt asking the model to cite its sources
   is an instruction, not a guarantee — the verification in code is what
   makes it one.

`rag-gate` does not replace your retrieval stack, your vector database, or
your LLM provider. It sits in front of the LLM call and after the generation
step, as a thin, provider-agnostic layer.

## Why not just use LangChain / LlamaIndex / Guardrails AI?

Those are large, general-purpose frameworks. `rag-gate` is deliberately
narrow: it does two things — the gate and the citation check — and is meant
to drop into a stack you already have, including one built on LangChain or
LlamaIndex, without asking you to adopt a whole new framework.

## Status

This repository is in **Phase 0**: repository setup, license, CI, and the
project skeleton. The core logic (`gate.py`, `guardrails.py`, the pluggable
provider/store/embedding interfaces) lands in Phase 1. See
[`docs/architecture.md`](docs/architecture.md) for the full design and
[`docs/adr/`](docs/adr) for the reasoning behind each decision.

## Project layout

```
src/rag_gate/
├── gate.py            # decides: call the LLM, or refuse with a reason
├── coverage.py         # topic → documents map, auditable (YAML/JSON)
├── retriever.py        # retrieval + gate integration
├── guardrails.py        # citation extraction and verification
├── schemas.py          # Pydantic contracts
├── cli.py               # rag-gate init / ingest / ask / doctor
├── providers/           # LLM providers: anthropic, openai, ollama
├── stores/              # vector stores: chroma, pgvector, memory
├── embeddings/           # embedding backends
├── loaders/              # document loaders (PDF, OCR fallback, text)
└── api/                  # optional thin FastAPI wrapper
```

## Development

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
```

## License

[Apache 2.0](LICENSE).

## Contributing

Not accepting external contributions yet — the core API is still taking
shape. [`CONTRIBUTING.md`](CONTRIBUTING.md) will be updated once Phase 1
lands.
