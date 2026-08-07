# Spec: Persistent Workflow Memory

- **ID:** 0002-workflow-memory
- **Status:** Approved
- **Author:** QF Workflow SDK
- **Approver:** QF Workflow SDK
- **Last updated:** 2026-08-07

> WHAT and WHY only. Implementation lives in `plan.md`.

## Problem & Context

When a workflow runs repeatedly on the same databases and datasets, it re-discovers
the same schema quirks, join keys, data-quality gotchas, and "need-to-knows" every
time. There is no durable place for a workflow to accumulate what it learns, so
knowledge lives in people's heads and conversational context. This spec defines a
persistent, provenance-tracked memory that lets a workflow arrive already knowing the
kinks of a dataset — without misleading it with stale or leaked knowledge.

## Goals

- A durable store where workflows accumulate learned knowledge over time.
- Memory that can be primed before a run and updated after, safely.
- Guardrails so memory never leaks future information or exposes secrets/PII.

## Non-Goals

- Building the runtime that reads/writes memory (the agent runtime does that).
- Storing raw data rows or credentials in memory.
- Replacing the knowledge base (`knowledge/`) — memory reuses its agents.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The store shall use a two-axis layout: `_shared/` for facts about a source and per-workflow folders for workflow-specific usage. | must |
| REQ-002 | Every memory record shall carry provenance: source run, first-seen and last-confirmed dates, confidence, and access level. | must |
| REQ-003 | The store shall support priming (read before a run) and updating (write after a run) via the knowledge agents. | must |
| REQ-004 | A manifest shall declare whether memory is committed or external, per workflow, with access levels. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | No secrets, credentials, connection strings, or PII in memory. | zero occurrences |
| NFR-002 | Research/backtest runs use point-in-time-scoped memory (leakage firewall). | no future-dated learning used |
| NFR-003 | Reproducibility: a run records the memory version it used. | run card references memory version |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a workflow and dataset, when memory is resolved, then it maps to a `_shared/datasets/<ds>/` path and a `<workflow>/datasets/<ds>/` path. | REQ-001 |
| AC-002 | Given any memory record, when it is validated, then it has source run, first-seen, last-confirmed, confidence, and access level. | REQ-002 |
| AC-003 | Given memory content, when the memory gate runs, then any secret, connection string, or PII is flagged. | NFR-001 |
| AC-004 | Given a research/backtest run, when memory is primed, then only records with a `pit_scope` on or before the decision date are used. | NFR-002 |
| AC-005 | Given a completed run, when its run card is written, then it records the memory version used. | NFR-003 |

## Data & Dependencies

- Reuses the `knowledge/` agents (ingestion, curation, retrieval, institutional_memory).
- Reuses the `knowledge_sources.yml` pattern for the manifest and external stores.
- Depends on `templates/docs/run_card.md` for the memory-version reference.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Stale memory misleads a workflow (schema drift, data change). | Wrong queries/results. | `last_confirmed` dates + re-validation; staleness flags. |
| RISK-002 | Memory leaks future information into a backtest. | Overstated performance. | `pit_scope` firewall; research memory bounded by decision date. |
| RISK-003 | Secrets or PII stored in memory. | Data exposure. | `memory-check` gate + `secret-scan`; metadata-only rule. |
| RISK-004 | Restricted-dataset memory served without authorization. | Barrier breach. | Access level inherited; retrieval enforces it. |
| RISK-005 | Evolving memory makes runs irreproducible. | Non-reproducible results. | Version/snapshot memory; record it in the run card. |

## Assumptions & Open Questions

- Assumption: memory is committed and secret/PII-scanned by default; sensitive
  deployments point the manifest at an external, gitignored store.
- Open question: memory versioning mechanism (content hash vs git ref) — decided in
  the plan, defaulting to a recorded snapshot reference.

## Exceptions

None.
