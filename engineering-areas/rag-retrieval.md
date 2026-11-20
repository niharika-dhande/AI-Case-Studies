# RAG & Retrieval

Answers grounded in an organisation's own material. Custom ingestion cleans transcripts and documents and chunks them by speaker with overlap; sentence embeddings go into a FAISS index alongside a custom BM25 keyword index; every question is searched both ways and fused with Reciprocal Rank Fusion, narrowed by metadata such as project and date. A slot-state flow rebuilds each follow-up into a standalone query. A separate LangChain reference build lets us compare the framework approach against this first-principles one.

## Capabilities

- Custom ingestion & chunking
- Hybrid search (FAISS + BM25)
- Reciprocal Rank Fusion
- Metadata filters
- Multi-turn slot state
- Framework vs first-principles comparison

## Case studies

- [Automated SDLC Artifact & Technical Specification Generation Pipeline](../case-studies/sdlc-artifact-generation-pipeline/README.md)
- [AI Enablement: Moving Multi-Domain Teams to an AI-Enabled SDLC](../case-studies/ai-enablement-aidlc-transformation/README.md)
- [Framework-Based Knowledge Retrieval Pipeline (LangChain Reference Build)](../case-studies/langchain-knowledge-retrieval-reference-build/README.md)

## Experiments

- [Framework-Based vs First-Principles Retrieval Pipelines: Same Problem, Two Build Approaches](../experiments/README.md#framework-vs-first-principles-retrieval-pipelines)
- [Hybrid Lexical + Semantic Retrieval: Chunk Size, Fusion Weight and Latency vs Recall](../experiments/README.md#hybrid-retrieval-chunk-size-fusion-latency-recall)

---

<sub>Generated from Sanity by `scripts/sync_from_sanity.py`. Edit the content in Sanity Studio, not in this file.</sub>
