# Example: compliance Q&A

Two policy documents (`documents/`) and a self-contained script answering
questions about them, with every claim cited back to a specific policy —
and refusing outright when a question falls outside what's documented, no
API key or vector database required to see that part work.

```bash
uv sync --extra dev  # from the repository root, if you haven't already
uv run python examples/compliance_qa/demo.py
```

Set `ANTHROPIC_API_KEY` first to also see a real, cited LLM answer for the
documented question — otherwise the demo prints the prompt that would
have been sent.
