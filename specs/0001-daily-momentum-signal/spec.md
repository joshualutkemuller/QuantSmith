# Spec: Daily cross-sectional momentum signal

- **ID:** 0001-daily-momentum-signal
- **Status:** Approved
- **Author:** QF Workflow SDK
- **Approver:** QF Workflow SDK
- **Last updated:** 2026-07-10

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.

## Problem & Context

The research desk needs a documented, reproducible daily momentum signal over a
liquid equity universe to use as a baseline in cross-sectional model comparisons.
Today the calculation lives in an undocumented notebook, so results cannot be
reviewed or reproduced. This spec defines the baseline as a first-class artifact.

## Goals

- A reproducible daily momentum score per name that another researcher can rerun.
- A documented, point-in-time-safe construction with no look-ahead.
- A baseline others can compare their signals against.

## Non-Goals

- Portfolio construction, sizing, or execution.
- Transaction-cost modelling or live trading.
- Any universe beyond the specified liquid equity set.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall compute a daily momentum score per name as the trailing 12-month return skipping the most recent month. | must |
| REQ-002 | The system shall cross-sectionally rank and z-score the raw momentum each day so scores are comparable across dates. | must |
| REQ-003 | The system shall exclude names failing the liquidity filter on a given date from that date's cross-section. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | Re-running on the same input snapshot yields bitwise-identical output. |
| NFR-002 | Runtime | Full-history rebuild over the reference universe completes in < 10 minutes on one core. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a price history, when the signal is computed for date D, then only data on or before D minus one month is used (no look-ahead). | REQ-001 |
| AC-002 | Given a day's raw momentum, when it is normalized, then the cross-section has mean ~0 and unit standard deviation. | REQ-002 |
| AC-003 | Given the same input snapshot, when the pipeline runs twice, then the two outputs are identical. | NFR-001 |

## Data & Dependencies

- Adjusted daily close prices for the reference universe, point-in-time.
- A daily liquidity metric (e.g. 20-day median dollar volume).
- Dependency: the shared price-snapshot store. Access is read-only; no private
  data is written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Survivorship bias if the universe excludes delisted names. | Overstated backtest performance. | Use point-in-time universe membership; document coverage in the dataset card. |

## Assumptions & Open Questions

- Assumption: adjusted prices already incorporate splits and dividends.
- Open question: should the liquidity filter use a fixed threshold or a universe
  percentile? Tracked as an open decision for the plan.

## Exceptions

None.
