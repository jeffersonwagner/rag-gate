# ADR-0006 — Don't pin mypy's `python_version` when checking across a matrix

## Context

`[tool.mypy]` pinned `python_version = "3.11"`, matching the project's
minimum supported version. CI's mypy step passed locally (Python 3.11) but
failed in GitHub Actions on the 3.12 and 3.13 jobs with:

```
.venv/lib/python3.13/site-packages/numpy/__init__.pyi:737: error:
Type statement is only supported in Python 3.12 and greater  [syntax]
```

`numpy` is a transitive dependency (via `chromadb`, used lazily in
`stores/chroma.py`) — not imported directly anywhere in this codebase.
`uv` resolves a different numpy release per Python target (2.4.6 for
3.11, 2.5.3 for 3.13 in this case), and the 3.13-targeted release ships a
`.pyi` stub using a PEP 695 `type` alias statement, which is syntax only
valid from Python 3.12 onward. Pinning mypy's target to 3.11 made it parse
*every* file it touched — including that stub — with pre-3.12 grammar,
which is a hard syntax error, not a typing warning `ignore_missing_imports`
could suppress.

## Decision

Remove the `python_version` pin entirely. Left unset, mypy defaults to the
version of the interpreter actually running it, which is exactly the
Python version `uv` resolved that job's dependencies for — the mismatch
disappears structurally instead of needing a per-dependency workaround.

## Consequences

- Verified locally against all three supported versions (3.11, 3.12, 3.13)
  before pushing the fix, rather than trusting a single local run — this
  bug specifically couldn't have been caught by mypy under 3.11 alone.
- A future dependency could reintroduce a similar mismatch in the other
  direction (a stub requiring syntax older than some job's target
  wouldn't happen — newer syntax is the only failure mode this way).
  Nothing currently guards against that beyond CI's matrix itself
  surfacing it again, which is an acceptable trade-off given how narrow
  the failure mode is.

## What would invalidate this

If the project ever needs to assert "this code must type-check as valid
Python 3.11" as a real constraint (not just "the library must run on
3.11"), that check belongs in a dedicated, single-version CI job with its
own `python_version` override — not as the default for every job in the
matrix.
