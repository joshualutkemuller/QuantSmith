# Tasks: Daily cross-sectional momentum signal

- **Spec:** 0001-daily-momentum-signal (`spec.md`, `plan.md`)
- **Last updated:** 2026-07-10

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Reproducibility preserved (pinned snapshot, seeded, no hidden state).
- No secrets, credentials, or private data introduced.
- Docs/configs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Implement `raw_momentum` with the 12-1 month window. | REQ-001, AC-001 | done | No-look-ahead guaranteed by the windowing. |
| T-002 | Implement `normalize` (per-date cross-sectional z-score). | REQ-002, AC-002 | done | |
| T-003 | Implement `liquidity_filter` (universe percentile). | REQ-003 | done | Threshold pending research-lead confirmation. |
| T-004 | Compose `build_signal`; pin snapshot and seed; vectorize. | NFR-001, NFR-002, AC-003 | done | |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `test_no_lookahead_AC-001` | done |
| AC-002 | `test_cross_section_normalized_AC-002` | done |
| AC-003 | `test_reproducible_output_AC-003` | done |

## Follow-ups

- Confirm the liquidity percentile threshold and update REQ-003 / the plan if it
  changes (tracked, not silently deferred).
