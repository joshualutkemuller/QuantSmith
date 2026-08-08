# Plan: End-to-end analytics pipeline

- **Spec:** 0010-analytics-pipeline (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Compose the Data Analyst chain as a sequence of pure functions, so reproducibility
and governance hold *by construction*: metrics flow only through the `0008` semantic
layer, and the report is assembled only after a quality guard has run. A failing
check yields a "blocked" report with a `None` value rather than a misleading number.

## Agent Routing

The workflow is the Data Analyst / Analytics Pipeline chain (see `docs/workflows.md`
→ *Data Analyst* and *Analytics Pipeline (runtime)*):

```text
orchestrator-agent
  -> sql-integration-agent       # run_query (source -> rows)
  -> data-prep-agent             # prepare (dedup, type, profile) + data_quality
  -> eda-specialist-agent        # profile_facts (summary stats)
  -> analytics/metrics_semantic_layer   # compute via SemanticLayer (spec 0008)
  -> quality-guard-agent         # block on empty / ungoverned / reconciliation
  -> reporting-agent             # build the report artifact with provenance
```

## Architecture & Components

- `Table` / `run_query(table, where)` — the source and its query (SQL stand-in).
- `FactSchema` — maps source fields to period, dimensions, and measures.
- `prepare(rows, schema)` → `PreparedData(facts, profile)` — dedup, type, profile.
- `profile_facts(facts, measure)` — the EDA summary.
- `SemanticLayer.compute` (from `0008`) — the only place metrics are computed.
- `QualityResult` / the guard inside `run_pipeline` — findings + ok flag.
- `Report` — value, quality, profile, eda, provenance; `status` derives from quality.
- `run_pipeline(...)` — composes all of the above.

## Interfaces & Data Contracts

- Input: a `Table`, a populated `SemanticLayer`, a metric name, a `FactSchema`, and
  optional `period` / `group_by` / `where`.
- Output: a `Report`; `value` is a scalar, a `{slice: value}` map, or `None` when
  blocked; `status` is `ok` or `blocked`.
- The period filter is delegated to the semantic layer → point-in-time (NFR-002).

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Pure functions; metrics only via the governed layer; report gated on the quality guard. |
| P5 Reversibility | yes | Pure analysis; nothing to roll back. |
| P6 Observability | yes | Profile, EDA summary, quality findings, and provenance travel with every report. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Blocked reports return `None`, not a misleading number; provenance enables audit. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `run_pipeline` end-to-end composition | T-001 |
| REQ-002 | `prepare` (dedup, type, profile) | T-002 |
| REQ-003 | `SemanticLayer.compute` inside `run_pipeline` | T-003 |
| REQ-004 | quality guard + `QualityResult` | T-004 |
| REQ-005 | `Report.provenance` | T-005 |
| NFR-001 | pure, deterministic functions | T-001 |
| NFR-002 | period filter via the semantic layer | T-003 |
| NFR-003 | metrics only through the governed layer | T-003, T-004 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Metric computation | Reuse the `0008` semantic layer | Recompute in the pipeline | Reuse guarantees one source of truth; recomputation reintroduces drift. |
| Failure handling | Block with `None` + findings | Return best-effort number | A misleading number is worse than an explicit block (P10). |
| Dedup | Exact-row dedup | Fuzzy/near-duplicate | Deterministic and safe; near-duplicate resolution is a follow-up. |
| Report form | Structured artifact | Direct BI payload | Keeps the reference tool-agnostic; dashboard agents consume the artifact. |

## Validation Strategy

- AC-001: run end to end; assert a numeric answer and "ok" status.
- AC-002: prepare rows with duplicates/missing/absent-period; assert the profile.
- AC-003: assert the report value equals `SemanticLayer.compute` on the same facts.
- AC-004: assert ungoverned metric and empty result block; a valid request is ok.
- AC-005: assert provenance fields are present and correct.
- AC-006: run twice; assert identical reports.

## Rollout, Observability & Rollback

A library consumed by the reporting and orchestrator agents. There is nothing to roll
back; a changed source or registry simply changes the report, and the quality guard
plus provenance make every published answer auditable.

## Open Questions

- Should the report optionally render to a Tableau/Power BI payload here, or remain a
  structured artifact the dashboard agents transform? Deferred until a consumer needs
  it.
