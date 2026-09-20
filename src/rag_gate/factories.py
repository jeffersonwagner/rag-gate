"""Name -> instance factories for the CLI's --embedder/--provider/--store flags.

Kept separate from cli.py so the mapping of names to implementations can be
imported and tested without going through Typer.
"""

from __future__ import annotations

from rag_gate.embeddings.base import Embedder
from rag_gate.providers.base import LLMProvider
from rag_gate.stores.base import VectorStore

EMBEDDER_CHOICES = ("hashing", "openai", "sentence-transformers")
PROVIDER_CHOICES = ("anthropic", "openai", "ollama")
STORE_CHOICES = ("chroma", "memory")


def build_embedder(name: str) -> Embedder:
    if name == "hashing":
        from rag_gate.embeddings.hashing import HashingEmbedder

        return HashingEmbedder()
    if name == "openai":
        from rag_gate.embeddings.openai import OpenAIEmbedder

        return OpenAIEmbedder()
    if name == "sentence-transformers":
        from rag_gate.embeddings.sentence_transformers import SentenceTransformersEmbedder

        return SentenceTransformersEmbedder()
    raise ValueError(f"Unknown embedder '{name}'. Choose one of: {', '.join(EMBEDDER_CHOICES)}")


def build_provider(name: str, model: str | None) -> LLMProvider:
    if name == "anthropic":
        from rag_gate.providers.anthropic import AnthropicProvider

        return AnthropicProvider(model=model) if model else AnthropicProvider()
    if name == "openai":
        from rag_gate.providers.openai import OpenAIProvider

        return OpenAIProvider(model=model) if model else OpenAIProvider()
    if name == "ollama":
        from rag_gate.providers.ollama import OllamaProvider

        return OllamaProvider(model=model) if model else OllamaProvider()
    raise ValueError(f"Unknown provider '{name}'. Choose one of: {', '.join(PROVIDER_CHOICES)}")


def build_store(name: str, persist_dir: str | None) -> VectorStore:
    if name == "chroma":
        from rag_gate.stores.chroma import ChromaStore

        return ChromaStore(persist_dir=persist_dir)
    if name == "memory":
        from rag_gate.stores.memory import InMemoryStore

        return InMemoryStore()
    raise ValueError(f"Unknown store '{name}'. Choose one of: {', '.join(STORE_CHOICES)}")
