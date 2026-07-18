# Agentic Workflow Blueprint

## 1) System Objective

Design a command-line analytics copilot that turns natural-language user intents into reliable data and dashboard operations by coordinating specialist agents.

## 2) Core Agent Topology

1. **Orchestrator Agent**
   - Interprets intent, decomposes tasks, chooses execution path.
2. **Data Prep Agent**
   - Cleans, normalizes, and transforms datasets.
3. **SQL Integration Agent**
   - Connects to SQL systems, profiles schemas, executes guarded queries.
4. **Tableau Dashboard Agent**
   - Generates dashboard specs with RAG context and validator checks.
5. **Reporting Agent**
   - Converts dashboard/data outputs into consumable report artifacts.
6. **Quality Guard Agent**
   - Validates payloads, enforces contracts, tracks observability metrics.

## 3) Execution Lifecycle

1. Intent capture from terminal.
2. Task planning and routing by Orchestrator.
3. Data access via SQL Integration Agent.
4. Data cleaning/transformation via Data Prep Agent.
5. Dashboard generation via Tableau Dashboard Agent.
6. Validation and policy checks by Quality Guard Agent.
7. Reporting/export actions via Reporting Agent.
8. Artifact summary returned to user in terminal.

## 4) RAG + Validation Pattern for Tableau

- Index reusable dashboard patterns, schema docs, and prior templates.
- Retrieve top-k context relevant to user request.
- Produce structured dashboard payload.
- Validate with Pydantic contracts before any API submission.
- Auto-repair invalid payloads through bounded retry loop.

## 5) Current Implementation Slice

The repository currently ships a runnable short-term scaffold in `src/li_agent/`:

- Local SQLite SQL integration (`sql_tools.py`) with demo data bootstrap.
- Deterministic cleaning pass (`data_prep.py`).
- File-backed lightweight retrieval store (`rag.py`).
- Tableau payload generation + validation (`tableau.py`) with optional Pydantic usage.
- End-to-end orchestrator (`orchestrator.py`) and CLI entrypoint (`cli.py`).

## 6) Recommended Interfaces

- Agent-to-agent contract format: JSON schema typed envelopes.
- Skill library format: per-agent `SKILL.md` with deterministic workflow steps.
- Tool adapters: SQL client, Tableau API wrapper, report exporter.

## 6) Delivery Roadmap

### Phase A (Short-Term)
- Orchestrator, Data Prep, and base SQL execution flow.
- Minimal CLI and prompt contracts.

### Phase B (Intermediate)
- Full Tableau generation path with RAG + Pydantic guardrails.
- Schema-aware query planning and reusable transformations.
- Production SQL connectors and governed query templates.

### Phase C (End State)
- Multi-platform outputs (Tableau + PowerPoint/reporting channels).
- Persistent memory of analytical workflows and reusable playbooks.
