"""Tests for the name -> instance factories used by the CLI."""

import pytest

from rag_gate.factories import build_embedder, build_provider, build_store
from rag_gate.stores.chroma import ChromaStore
from rag_gate.stores.memory import InMemoryStore


def test_build_embedder_hashing():
    from rag_gate.embeddings.hashing import HashingEmbedder

    assert isinstance(build_embedder("hashing"), HashingEmbedder)


def test_build_embedder_unknown_name_raises():
    with pytest.raises(ValueError, match="Unknown embedder"):
        build_embedder("not-a-real-embedder")


def test_build_provider_unknown_name_raises():
    with pytest.raises(ValueError, match="Unknown provider"):
        build_provider("not-a-real-provider", None)


def test_build_provider_anthropic_default_model():
    from rag_gate.providers.anthropic import AnthropicProvider

    provider = build_provider("anthropic", None)
    assert isinstance(provider, AnthropicProvider)


def test_build_provider_with_model_override():
    provider = build_provider("openai", "gpt-4o")
    assert provider.model == "gpt-4o"


def test_build_store_memory():
    assert isinstance(build_store("memory", None), InMemoryStore)


def test_build_store_chroma():
    assert isinstance(build_store("chroma", None), ChromaStore)


def test_build_store_unknown_name_raises():
    with pytest.raises(ValueError, match="Unknown store"):
        build_store("not-a-real-store", None)
