# AI Case Studies · Prompt at Work

Engineering case studies by **Niharika Dhande**, AI Solutions Engineer: multi-agent systems, RAG pipelines, AI automation and the engineering patterns underneath them. Each case study covers the problem, the design decisions and their trade-offs, the architecture and what I learned.

Full write-ups: [promptatwork.com](https://promptatwork.com/ai-lab/work) · [LinkedIn](https://www.linkedin.com/in/niharikasaxenadhande)

## Case studies

| Case study | Category |
|---|---|
| [AI Executive Command Center](case-studies/ai-executive-command-center/README.md) | Custom Multi-Agent Orchestration · Framework-Free Runtime |
| [Automated SDLC Artifact & Technical Specification Generation Pipeline](case-studies/sdlc-artifact-generation-pipeline/README.md) | Knowledge Retrieval · SDLC Automation · Framework-Free Pipelines |
| [AI Enablement: Moving Multi-Domain Teams to an AI-Enabled SDLC](case-studies/ai-enablement-aidlc-transformation/README.md) | AI Enablement · AIDLC Transformation · Enterprise Rollout |
| [AI Enterprise Blueprint: Building Content-Driven Business Platforms](case-studies/content-driven-business-platform-blueprint/README.md) | Solution Blueprint · Enterprise Web Platforms |
| [Framework-Based Knowledge Retrieval Pipeline (LangChain Reference Build)](case-studies/langchain-knowledge-retrieval-reference-build/README.md) | Reference Build · RAG · LangChain |
| [WhatsApp Business Automation Platform](case-studies/poc-whatsapp-business-automation-platform/README.md) | Client POC · Conversational Automation · Multi-Tenant Platform |

## Engineering areas

| Area | Case studies | Experiments | Automations |
|---|---|---|---|
| [Full-Stack AI Engineering](engineering-areas/full-stack-ai.md) | 4 | 1 | 1 |
| [RAG & Retrieval](engineering-areas/rag-retrieval.md) | 3 | 2 | 0 |
| [Generative AI Engineering](engineering-areas/generative-ai.md) | 2 | 3 | 2 |
| [Agentic AI](engineering-areas/agentic-ai.md) | 1 | 1 | 0 |
| [AI Automation & Integrations](engineering-areas/ai-automation.md) | 3 | 2 | 4 |
| [Systems, Reliability & Security Engineering](engineering-areas/systems-reliability-security.md) | 3 | 0 | 0 |

## More

- [Engineering patterns](patterns/README.md)
- [Experiments](experiments/README.md) (6)
- [Automations](automations/README.md) (6)

## How this repository is built

The content lives in Sanity CMS, the same source that powers promptatwork.com. A GitHub Action runs `scripts/sync_from_sanity.py`, which reads the published content with GROQ and regenerates these Markdown files, so the site and this repository never drift apart. Client names, credentials, endpoints and configuration are never included.

---

<sub>Generated from Sanity by `scripts/sync_from_sanity.py`. Edit the content in Sanity Studio, not in this file.</sub>
