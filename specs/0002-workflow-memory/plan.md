# Plan: Persistent Workflow Memory

- **Spec:** 0002-workflow-memory (`spec.md`)
- **Status:** Approved
- **Last updated:** 2026-08-07

> HOW. Requires the approved `spec.md`.

## Approach

Persistent memory is the `knowledge/` group applied to a dedicated `memory/` store
with a fixed schema and guardrails. The SDK provides the convention, layout, record
schema, manifest, and a validation gate; the agent runtime performs the actual
read (prime) and write (learn) using the knowledge agents. Correctness holds by
construction: provenance is required on every record, and point-in-time scoping keeps
research memory from leaking the future.

## Architecture & Components

Two-axis layout:

```
memory/
  README.md          manifest.yaml
  _shared/datasets/<ds>/   schema.md quirks.md pitfalls.md provenance.yaml
  <workflow>/              README.md index.yaml lessons.md
    datasets/<ds>/         patterns.md decisions.md
```

- `_shared/` holds facts about a source (schema, quirks) reused by any workflow.
- `<workflow>/` holds workflow-specific usage (patterns, decisions).

## Record Schema

Each record (in `provenance.yaml`/`index.yaml`) has: `id`, `scope`
(dataset/table/field), `type` (schema|quirk|pattern|pitfall|decision|metric|
performance), `statement`, `evidence` (source run ref, optional sample query — no
data), `confidence` + `corroboration_count`, `first_seen`, `last_confirmed`,
`status` (active|stale|superseded|retired), `access_level`, and `pit_scope`.

## Lifecycle (prime → learn → curate)

- **Prime:** `knowledge_retrieval` loads relevant records before a run.
- **Learn:** `knowledge_ingestion` appends candidate records with provenance.
- **Curate:** `knowledge_curation` dedupes, resolves conflicts, flags stale/superseded.
- **Persist:** `institutional_memory` writes durable decisions.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Provenance required; `pit_scope` prevents leakage; memory version pinned per run. |
| P5 Reversibility | yes | Records are versioned and `superseded`, never destructively overwritten. |
| P9 Security & data | yes | Metadata-only; secrets/PII forbidden and gated; access level inherited. |
| P10 Honest reporting | yes | Confidence stated; low-confidence memory is a hypothesis, not fact. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | Two-axis layout | T-001 |
| REQ-002 | Record schema (provenance) | T-001, T-002 |
| REQ-003 | Lifecycle via knowledge agents | T-004 |
| REQ-004 | `manifest.yaml` | T-001 |
| NFR-001 | `memory-check` gate + secret-scan | T-003 |
| NFR-002 | `pit_scope` firewall | T-002, T-003 |
| NFR-003 | Run-card memory version | T-005 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected | Why |
| --- | --- | --- | --- |
| Scope axis | Two-axis (`_shared` + workflow) | Per-workflow only | Avoids re-learning the same source per workflow. |
| Persistence | Committed + scanned | External-only | Reproducible and shareable; sensitive stores opt out via manifest. |
| New agents | Reuse `knowledge/` | Dedicated memory agents | Memory is a knowledge application; avoids duplication. |

## Validation Strategy

- AC-001/002: `memory-check` verifies layout and required provenance fields.
- AC-003: `memory-check` scans memory content for secrets, connection strings, PII.
- AC-004: research runs assert every primed record's `pit_scope` ≤ decision date.
- AC-005: the run card template carries a memory-version field.

## Rollout, Observability & Rollback

Additive: the `memory/` store and gate ship advisory-first. Memory records are
versioned; a bad learning is marked `superseded`, not deleted. The `memory-check`
gate provides observability over structure and safety.

## Open Questions

- Confirm the memory-version mechanism (snapshot ref vs content hash) with the owner.
