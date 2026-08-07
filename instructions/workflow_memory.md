# Workflow Memory Instructions

## Purpose

Use this instruction set when a workflow reads from or writes to persistent memory —
the durable store where a workflow accumulates what it learns about databases,
datasets, schemas, fields, and their quirks over time. It is the standard behind the
`memory/` store and is served by the `knowledge/` agents. The goal is a memory that
lets a workflow arrive already knowing the kinks of a dataset, without being misled
by stale or leaked knowledge.

## Layout (two-axis)

```
memory/
  manifest.yaml                    # where memory lives, access levels, committed/external
  _shared/datasets/<ds>/           # facts about a source, reused by any workflow
    schema.md quirks.md pitfalls.md provenance.yaml
  <workflow>/                      # one per workflow in docs/workflows.md
    index.yaml lessons.md
    datasets/<ds>/ patterns.md decisions.md
```

`_shared/` holds what is true about a source; `<workflow>/` holds how a workflow uses
it. This prevents every workflow re-learning the same database.

## Record Schema

Every learning is a record with: `id`; `scope` (dataset/table/field); `type`
(schema | quirk | pattern | pitfall | decision | metric | performance); `statement`;
`evidence` (source run reference, optional sample query — never data); `confidence`
and `corroboration_count`; `first_seen`, `last_confirmed`; `status`
(active | stale | superseded | retired); `access_level`; and `pit_scope` (the data
window the learning came from).

## Lifecycle

- **Prime (read):** load relevant records before a run so the workflow already knows
  the dataset. Use `knowledge/knowledge_retrieval`.
- **Learn (write):** after a run, append new observations as candidate records with
  provenance and low confidence. Use `knowledge/knowledge_ingestion`.
- **Confirm:** repeated corroboration raises confidence; a contradiction flags it.
- **Curate:** consolidate, dedupe, resolve conflicts, flag stale/superseded. Use
  `knowledge/knowledge_curation`.
- **Persist decisions:** durable decisions via `knowledge/institutional_memory`.

## Standards (guardrails)

- **Provenance always.** Every record cites its source run and carries `first_seen`,
  `last_confirmed`, `confidence`, and `access_level`. No provenance, no record.
- **Point-in-time firewall.** A research or backtest run may use only records whose
  `pit_scope` is on or before the decision date; operational memory must not leak the
  future into research. See `instructions/point_in_time.md` (constitution P4).
- **Metadata only.** Never store credentials, connection strings, raw data rows, or
  PII in memory. See `agents/secrets_management/` (P9).
- **Freshness.** Treat old records as hypotheses; re-validate schema memory before
  trusting it, and mark drift-invalidated records `stale`.
- **Access inheritance.** Memory about a restricted dataset inherits its access level;
  retrieval enforces it (information barriers).
- **Honest confidence.** State confidence; low-confidence memory is not fact.
- **Reproducible.** Version memory; record the memory version a run used in its run card.
- **No silent overwrite.** Contradictions are resolved to `superseded`, not deleted.

## Checks

- Does every record carry provenance and an access level?
- Are research/backtest runs bounded to `pit_scope` ≤ decision date?
- Is the store free of secrets, connection strings, and PII?
- Are stale/superseded records flagged rather than served as current?
- Is the memory version recorded in the run card?

## Common Failure Modes

- Serving stale schema memory after the schema changed.
- Using a learning derived from future data in a backtest (leakage).
- Storing a connection string, credential, or PII "for convenience".
- Silently overwriting a record instead of superseding it.
- Treating a low-confidence, single-observation record as established fact.

## Spec-Driven Alignment

Defined by `specs/0002-workflow-memory/`. Guarantees become testable: "provenance
present", "no secrets/PII", and "pit_scope-bounded" are `AC-*`; staleness, leakage,
secrets, and irreproducibility are the spec's `RISK-*`. Validated by the
`memory-check` gate and `secret-scan`; served by the `knowledge/` agents.
