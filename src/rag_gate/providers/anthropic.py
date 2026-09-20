"""Anthropic implementation of LLMProvider."""

from __future__ import annotations


class AnthropicProvider:
    """Calls the Anthropic Messages API. Requires the ``anthropic`` extra."""

    def __init__(self, model: str = "claude-haiku-4-5", api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:
                raise ImportError(
                    "AnthropicProvider requires the 'anthropic' package. "
                    "Install it with: pip install rag-gate[anthropic]"
                ) from exc
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, *, temperature: float = 0.1) -> str:
        client = self._get_client()
        response = client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
