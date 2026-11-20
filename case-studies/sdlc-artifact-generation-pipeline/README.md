# Automated SDLC Artifact & Technical Specification Generation Pipeline

**Knowledge Retrieval · SDLC Automation · Framework-Free Pipelines**

> A centralized knowledge and synthesis pipeline that ingests a team's meeting transcripts and project documents from Google Workspace, answers questions across them with hybrid retrieval, and generates standard SDLC artifacts (executive summaries, high-level requirements documents, user stories and delivery timelines) in a fixed structure every time, built on deterministic pipelines with no agent framework.

**Engineering areas:** [Full-Stack AI Engineering](../../engineering-areas/full-stack-ai.md) · [RAG & Retrieval](../../engineering-areas/rag-retrieval.md)

## At a glance

- 4 SDLC artifact types generated
- 3 generation strategies (single-pass, two-stage, chained)
- Hybrid semantic + lexical retrieval
- 5 role-based guided flows

## Tech stack

`Python` · `FastAPI` · `Pydantic` · `FAISS` · `Sentence-Transformers` · `BM25 (custom implementation)` · `Google Workspace APIs (service account)` · `Document parsers (PDF, DOCX, XLSX, PPTX)` · `React` · `TypeScript` · `Vite` · `Tailwind CSS` · `pytest` · `GitHub Actions`

## Related work

**Experiments**

- [Single-Pass vs Two-Stage vs Chained Generation of SDLC Artifacts from Unstructured Transcripts](../../experiments/README.md#fast-vs-two-stage-vs-chained-document-generation)
- [Hybrid Lexical + Semantic Retrieval: Chunk Size, Fusion Weight and Latency vs Recall](../../experiments/README.md#hybrid-retrieval-chunk-size-fusion-latency-recall)
- [Framework-Based vs First-Principles Retrieval Pipelines: Same Problem, Two Build Approaches](../../experiments/README.md#framework-vs-first-principles-retrieval-pipelines)

**Automations**

- [Incremental Knowledge Ingestion & Indexing Pipeline](../../automations/README.md#drive-to-meeting-search-index)
- [Transcript-to-SDLC-Artifact Generation Pipeline](../../automations/README.md#meeting-transcripts-to-delivery-documents)

**Prompt patterns**

- Cross-Document Synthesis Answer Prompt (Grounded RAG Q&A)
- Schema-Steered Structured Extraction (JSON Without Extra Libraries)

Read the full case study on [Prompt at Work](https://promptatwork.com/ai-lab/sdlc-artifact-generation-pipeline).

---

<sub>Generated from Sanity by `scripts/sync_from_sanity.py`. Edit the content in Sanity Studio, not in this file.</sub>
