# Tasks: Persistent Workflow Memory

- **Spec:** 0002-workflow-memory (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

> Every task cites the requirement it advances; every acceptance criterion is named
> by a test.

## Definition of Done (applies to every task)

- Matches the plan; deviations noted in `plan.md`.
- Tests/gate checks pass deterministically.
- No secrets, credentials, or PII introduced.
- Docs/catalog updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Scaffold `memory/` (two-axis layout, `manifest.yaml`, example records with provenance). | REQ-001, REQ-002, REQ-004, AC-001, AC-002 | done | |
| T-002 | Write `instructions/workflow_memory.md` (schema, lifecycle, `pit_scope` firewall). | REQ-002, NFR-002, AC-004 | done | |
| T-003 | Add `hooks/stages/memory-check.sh` (layout, provenance, secret/PII scan). | NFR-001, NFR-002, AC-002, AC-003 | done | |
| T-004 | Wire the `knowledge/` agents to prime/learn/curate memory. | REQ-003 | done | |
| T-005 | Add a memory-version field to `templates/docs/run_card.md`. | NFR-003, AC-005 | done | |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `memory-check` layout resolution (AC-001) | done |
| AC-002 | `memory-check` provenance-fields check (AC-002) | done |
| AC-003 | `memory-check` secret/PII scan (AC-003) | done |
| AC-004 | runtime `pit_scope` assertion for research runs (AC-004) | todo (runtime) |
| AC-005 | run-card memory-version field present (AC-005) | done |

## Follow-ups

- Runtime enforcement of AC-004 (`pit_scope` bounding) lives in the agent runtime,
  not the SDK scaffold; tracked in `docs/handoffs/future_features.md`.
