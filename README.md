# rag-gate

**A hard gate that stops your RAG from answering without evidence.**

[Leia em português](README.pt-BR.md)

> Status: early development (Phase 2 — CLI and examples). Not yet published on PyPI.

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

**Phase 2 (CLI and examples) complete.** Both the library and the CLI work
end to end today. See [`docs/architecture.md`](docs/architecture.md) for
the full design and [`docs/adr/`](docs/adr) for the reasoning behind each
decision.

### Try it in two minutes — no API key needed

```bash
uv sync --extra dev --extra chroma
uv run python examples/helpdesk_bot/demo.py
```

This shows rag-gate's two core guarantees with sample documents bundled
in the repo: a documented question retrieves real chunks, and an
undocumented one is refused *before* any LLM would be called. See
[`examples/`](examples) for both runnable examples.

### CLI

```bash
rag-gate init my-project && cd my-project
# put a few .txt/.md/.pdf files in documents/, then:
rag-gate ingest documents --topic hr-policy
rag-gate ask "how many remote days are allowed?" --topic hr-policy
```

By default `ingest`/`ask` use the dependency-free `HashingEmbedder` (no API
key, but lower retrieval quality — see `docs/adr/0003`) and a local Chroma
store persisted under `.rag-gate/chroma`. Pass `--embedder openai` (with
`OPENAI_API_KEY` set) for real retrieval quality, and `--provider
anthropic|openai|ollama` to pick the LLM that generates the final answer.

### As a library

```python
from rag_gate.coverage import CoverageMap
from rag_gate.gate import DocumentGate
from rag_gate.retriever import GatedRetriever
from rag_gate.guardrails import build_answer
from rag_gate.prompting import build_prompt
from rag_gate.stores.memory import InMemoryStore
from rag_gate.embeddings.openai import OpenAIEmbedder
from rag_gate.providers.anthropic import AnthropicProvider

gate = DocumentGate(CoverageMap.from_file("coverage.yaml"))
retriever = GatedRetriever(gate, InMemoryStore(), OpenAIEmbedder())

question = "when do I get paid?"
decision, chunks = retriever.retrieve("payroll", question)
if not decision.allowed:
    print(decision.missing_documents_hint)
else:
    raw_answer = AnthropicProvider().generate(build_prompt(question, chunks))
    answer = build_answer(raw_answer, [c.id for c in chunks])
```

## Project layout

```
src/rag_gate/
├── gate.py            # decides: call the LLM, or refuse with a reason
├── coverage.py         # topic → documents map, auditable (YAML/JSON)
├── retriever.py        # retrieval + gate integration
├── guardrails.py        # citation extraction and verification
├── prompting.py          # builds the citation-required LLM prompt
├── chunking.py           # pure-Python, whitespace-safe text chunking
├── ingestion.py          # walks a directory into (Document, Chunk) pairs
├── factories.py          # name -> instance wiring for the CLI's flags
├── schemas.py          # Pydantic contracts
├── cli.py               # rag-gate init / ingest / ask / doctor
├── providers/           # LLM providers: anthropic, openai, ollama
├── stores/              # vector stores: chroma, pgvector, memory
├── embeddings/           # embedding backends, incl. the zero-setup HashingEmbedder
├── loaders/              # document loaders (PDF, OCR fallback, text)
└── api/                  # optional thin FastAPI wrapper
```

## Development

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
# Skips sentence-transformers on purpose — it pulls in a multi-GB PyTorch
# download. Add --extra sentence-transformers if you need that backend.
uv sync --extra dev --extra anthropic --extra openai --extra ollama --extra chroma --extra pdf
uv run pytest
uv run ruff check .
```

## License

[Apache 2.0](LICENSE).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).
