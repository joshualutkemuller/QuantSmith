# Plan: Daily cross-sectional momentum signal

- **Spec:** 0001-daily-momentum-signal (`spec.md`)
- **Status:** Approved
- **Author:** QF Workflow SDK
- **Last updated:** 2026-07-10

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Build the signal as a pure, deterministic transform from a point-in-time price
snapshot to a per-name daily score. The pipeline is a sequence of stateless
functions — load, compute raw momentum, apply the liquidity filter, normalize —
so that reproducibility and no-look-ahead hold by construction rather than by
after-the-fact checks.

## Architecture & Components

- `load_prices(snapshot)` → tidy price panel indexed by (date, name).
- `raw_momentum(panel)` → trailing 12-1 month return per (date, name).
- `liquidity_filter(panel, metric)` → boolean mask per (date, name).
- `normalize(raw, mask)` → per-date cross-sectional z-score over included names.
- `build_signal(snapshot)` composes the above and returns the score panel.

## Interfaces & Data Contracts

- Input: adjusted daily close panel; monotonic dates; no duplicate (date, name).
- Momentum for date D uses only rows with date ≤ D − 1 month → no look-ahead.
- Output: score panel (date, name, score); NaN for excluded names.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Windowing excludes the current month; pure functions, seeded, no hidden state. |
| P5 Reversibility | yes | Offline batch artifact; regenerate by rerun, nothing to roll back live. |
| P6 Observability | yes | Emits per-run coverage and cross-section stats for monitoring. |
| P9 Security & data | yes | Read-only snapshot; no private data or credentials in the repo. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `raw_momentum` (12-1 window) | T-001 |
| REQ-002 | `normalize` (cross-sectional z-score) | T-002 |
| REQ-003 | `liquidity_filter` | T-003 |
| NFR-001 | Pure functions, pinned snapshot, seeded | T-004 |
| NFR-002 | Vectorized panel ops | T-004 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Normalization | Cross-sectional z-score | Min-max scaling | Z-score is robust to universe size and comparable across dates. |
| Liquidity filter | Universe percentile | Fixed dollar threshold | Percentile adapts across regimes; fixed threshold drifts over time. |

## Validation Strategy

- AC-001: unit test feeding a panel with a known future spike; assert the score on
  date D is unaffected (no look-ahead).
- AC-002: property test asserting each day's included cross-section has mean ≈ 0
  and std ≈ 1.
- AC-003: run the pipeline twice on a fixed snapshot; assert equal output.

## Rollout, Observability & Rollback

Offline batch artifact consumed by research. Rollout is publishing a new signal
version; rollback is pointing consumers at the prior version. Each run logs
coverage (names in/out) and cross-section mean/std for drift monitoring.

## Open Questions

- Confirm the liquidity percentile threshold with the research lead (defaulting to
  the top 80% by 20-day median dollar volume until confirmed).
