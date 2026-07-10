# Tasks: <feature name>

- **Spec:** NNNN-short-slug (`spec.md`, `plan.md`)
- **Last updated:** YYYY-MM-DD

> Ordered, testable units of work. Every task cites the requirement(s) it advances
> and carries a Definition of Done. No task without a requirement.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Reproducibility preserved (pinned inputs, seeded randomness, no hidden state).
- No secrets, credentials, or private data introduced.
- Docs/configs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | … | REQ-001 | todo | |
| T-002 | … | REQ-001, AC-001 | todo | |
| T-003 | … | NFR-001 | todo | |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

Every acceptance criterion must be named by at least one test.

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | test_… (names AC-001) | todo |
| AC-002 | test_… (names AC-002) | todo |

## Follow-ups

Tracked work intentionally deferred (no silent "temporary" shortcuts — P8).

- …
