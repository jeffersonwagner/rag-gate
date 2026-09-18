# Architecture

## 1. Scope

`rag-gate` adds two things to a RAG pipeline: a **documentary gate** that
decides whether the LLM should be called at all, and a **citation
verifier** that checks the LLM's answer after the fact. It does not
implement retrieval, chunking, or an LLM itself — those are provided by
whatever stack the caller already has, through small pluggable interfaces.

## 2. Decision flow

```
User question
      │
      ▼
Retrieval over indexed documents (top-k chunks)
      │
      ▼
GATE: is there documentary coverage for this question's topic?
   (topic → documents map, an auditable, hand-editable config)
      │
 ┌────┴────┐
 NO         YES
 │           │
 ▼           ▼
Refuse      Call the LLM with the retrieved chunks as context
+ explain   (prompt requires a [n] citation per claim)
what's           │
missing          ▼
           GUARDRAIL: extract the citations from the answer and check
           that each one points to a chunk that was actually retrieved
                 │
                 ▼
           Final answer, with verified, cited sources
```

## 3. Components

| Layer | Module | Responsibility | Replaceable by |
|---|---|---|---|
| Gate | `gate.py` | decide: call the LLM or refuse, based on coverage | — |
| Coverage | `coverage.py` | topic → documents map, the gate's source of truth | — |
| Retrieval | `retriever.py` | wraps a `VectorStore`, applies the gate before generation | — |
| Reliability | `guardrails.py` | citation extraction + post-generation verification | — |
| Generation | `providers/*` | one `LLMProvider` per backend | Anthropic, OpenAI, Ollama, or a custom implementation |
| Storage | `stores/*` | one `VectorStore` per backend | Chroma, pgvector, Qdrant, in-memory |
| Embeddings | `embeddings/*` | one embedding backend | sentence-transformers, OpenAI, custom |
| Ingestion | `loaders/*` | text extraction, with automatic OCR fallback for scanned PDFs | — |

All four pluggable layers (`LLMProvider`, `VectorStore`, `Embedder`, and
document loaders) are `Protocol`-based: `rag-gate`'s core never imports a
specific vendor SDK directly, so swapping Chroma for pgvector or Ollama for
Anthropic never touches `gate.py` or `guardrails.py`.

## 4. Design principles

- **The gate is a hard stop, not a soft hint.** If coverage is missing, the
  LLM is never called — there is no context for it to hallucinate against.
- **Citation is verified in code, not just requested in the prompt.** A
  prompt asking the model to cite `[n]` is an instruction the model can
  ignore or fake; the verifier checks it after the fact.
- **The coverage map is auditable by a non-engineer.** It is a plain
  YAML/JSON file — `topic → [documents]` — that a domain expert can read
  and correct without touching code.
- **Document tagging is conservative by default.** A document is only
  considered to cover a topic if that's stated explicitly (a manifest
  entry), inferred from its filename/folder, or found by keyword match in
  its text — in that order. When nothing matches, the gate treats the
  topic as undocumented rather than guessing.
- **Nothing about the core is domain-specific.** `gate.py` and
  `guardrails.py` operate on generic `Document`, `Chunk`, and `Answer`
  types — the same core works for HR policies, technical manuals, or API
  documentation.

## 5. Roadmap

See the repository's [issues](https://github.com/jeffersonwagner/rag-gate/issues)
and [`docs/adr/`](adr) for in-progress design decisions. At a high level:

| Phase | Deliverables |
|---|---|
| 0 — Setup | repository, license, CI, project skeleton, first ADR |
| 1 — Core | gate, coverage map, guardrails, pluggable interfaces, one reference implementation per interface |
| 2 — DX & examples | CLI, two runnable examples, quickstart docs |
| 3 — Packaging | PyPI release, docs site, hallucination-rate benchmark |
| 4 — Launch | public announcement |
| 5 — Post-launch | issue triage, community-requested integrations |
