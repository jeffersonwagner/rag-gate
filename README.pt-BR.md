# rag-gate

**Uma trava que impede seu RAG de responder sem evidência.**

[Read in English](README.md)

> Este é um espelho em português do README principal. A documentação técnica
> detalhada (arquitetura, ADRs) é mantida em inglês para alcançar o maior
> público possível — este arquivo é atualizado por conveniência, mas pode
> ficar levemente atrás do README em inglês.

> Status: desenvolvimento inicial (Fase 0 — esqueleto do projeto). Ainda não
> publicado no PyPI.

## O problema

A maioria dos pipelines de RAG (geração aumentada por recuperação) sempre
chama o LLM, mesmo quando a recuperação não encontra nada relevante. O modelo
preenche a lacuna com informação inventada — com confiança. Em domínios onde
uma resposta errada tem custo real (compliance, suporte interno, documentação
técnica, procedimentos de segurança), isso não é um bug de UX, é um passivo.

## O que o rag-gate faz

`rag-gate` é uma biblioteca Python pequena e opinativa que adiciona duas
coisas em cima de qualquer stack de recuperação que você já tenha:

1. **Gate documental.** Antes de o LLM ser chamado, o `rag-gate` verifica se
   existe cobertura real para o tópico da pergunta, usando um mapa
   `tópico → documentos` auditável que uma pessoa não-programadora consegue
   ler e editar. Sem cobertura, o LLM nunca é chamado, e quem fez a pergunta
   recebe uma resposta explícita de "não documentado, cadastre isto" em vez
   de um chute.
2. **Citações verificadas.** Toda afirmação factual do LLM precisa citar
   `[n]`. Um verificador roda **depois** da geração e confere se cada
   citação aponta para um trecho realmente recuperado, sinalizando ou
   removendo qualquer afirmação não rastreável. Pedir ao modelo para citar
   fontes no prompt é uma instrução, não uma garantia — a verificação em
   código é o que transforma isso em garantia.

O `rag-gate` não substitui sua stack de recuperação, seu banco vetorial ou seu
provedor de LLM. Ele fica na frente da chamada ao LLM e depois da geração,
como uma camada fina e agnóstica de provedor.

## Por que não usar LangChain / LlamaIndex / Guardrails AI?

Esses são frameworks grandes e genéricos. O `rag-gate` é deliberadamente
estreito: faz duas coisas — o gate e a verificação de citação — e foi
pensado para encaixar em uma stack que você já tem, inclusive uma construída
sobre LangChain ou LlamaIndex, sem exigir que você adote um framework novo.

## Status

**Fase 1 concluída.** O núcleo está implementado e testado: o gate, o mapa
de cobertura (YAML/JSON), a verificação de citação e o retriever com gate
embutido, além de implementações de referência — `InMemoryStore` e
`ChromaStore` para vetores, OpenAI/sentence-transformers para embeddings, e
Anthropic/OpenAI/Ollama para geração. Ainda não há CLI nem exemplo
end-to-end — isso chega na Fase 2. Veja [`docs/architecture.md`](docs/architecture.md)
para o desenho completo e [`docs/adr/`](docs/adr) para o raciocínio por
trás de cada decisão.

## Desenvolvimento

Requer Python 3.11+ e [uv](https://docs.astral.sh/uv/).

```bash
# sentence-transformers fica de fora de propósito — puxa um download de
# GBs do PyTorch. Adicione --extra sentence-transformers se precisar dele.
uv sync --extra dev --extra anthropic --extra openai --extra ollama --extra chroma --extra pdf
uv run pytest
uv run ruff check .
```

## Licença

[Apache 2.0](LICENSE).
