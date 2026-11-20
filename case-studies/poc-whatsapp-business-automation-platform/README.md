# WhatsApp Business Automation Platform

**Client POC · Conversational Automation · Multi-Tenant Platform**

> A multi-tenant platform that runs a business's WhatsApp number: patients book, reschedule, cancel and pay entirely in chat, staff approve and reply from a live dashboard, and new automation modules plug in without touching the core. The first module is clinic appointment scheduling.

**Engineering areas:** [AI Automation & Integrations](../../engineering-areas/ai-automation.md) · [Full-Stack AI Engineering](../../engineering-areas/full-stack-ai.md) · [Systems, Reliability & Security Engineering](../../engineering-areas/systems-reliability-security.md)

## At a glance

- Book, reschedule, cancel and pay in WhatsApp
- 3 payment options
- 190+ automated tests
- 11 recorded architecture decisions

## Tech stack

`Python` · `FastAPI` · `SQLAlchemy (async)` · `PostgreSQL with row-level security` · `Alembic` · `React` · `TypeScript` · `Vite` · `TanStack Query` · `Tailwind CSS` · `WhatsApp Business Cloud API` · `Razorpay` · `Vercel` · `GitHub Actions`

## Related work

**Experiments**

- [Rules-First vs LLM-First Intent Understanding in a Conversational Booking Flow](../../experiments/README.md#rules-first-vs-llm-first-intent-understanding)

**Automations**

- [Event-Driven Notification & Reminder Pipeline (Transactional Outbox + Scheduled Jobs)](../../automations/README.md#event-driven-notification-reminder-pipeline)

**Prompt patterns**

- Untrusted-Input Boundary Guardrail (Prompt-Injection Defence)
- Schema-Steered Structured Extraction (JSON Without Extra Libraries)

Read the full case study on [Prompt at Work](https://promptatwork.com/ai-lab/poc-whatsapp-business-automation-platform).

---

<sub>Generated from Sanity by `scripts/sync_from_sanity.py`. Edit the content in Sanity Studio, not in this file.</sub>
