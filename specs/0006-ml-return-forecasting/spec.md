# Spec: Cross-sectional short-horizon return forecasting model

- **ID:** 0006-ml-return-forecasting
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-07

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> First runtime workflow promoted from the `agents/machine_learning/` and
> `agents/deep_learning/` groups (spec `0004`). Demonstrates the ML build chain
> end to end with a deep-learning challenger.

## Problem & Context

The desk has a documented momentum baseline (`specs/0001-daily-momentum-signal`)
but no *learned* forecast of forward returns. Ad-hoc models live in notebooks with
inconsistent labels, leaky validation, and no monitoring, so they cannot be
compared, reproduced, or promoted. This spec defines a first-class, learned
cross-sectional return forecast: a supervised baseline the desk can trust, a
deep-learning challenger evaluated under identical rules, and a monitored
production candidate. It is the first runtime workflow that routes the ML/DL
specialist agents from labeling through serving.

## Goals

- A point-in-time-safe, leakage-controlled label and feature pipeline for a
  cross-sectional forward-return forecast.
- A supervised baseline model that beats the momentum signal out-of-sample, net of
  costs, and is registered with a model card.
- A deep-learning challenger evaluated on identical folds, promoted only if it
  earns its added complexity and serving cost.
- A monitored production candidate with drift, calibration, decay, and retraining
  triggers documented.

## Non-Goals

- Portfolio construction, sizing, execution, or live trading (consumes the forecast
  downstream; out of scope here).
- New data acquisition or vendor integration beyond the existing price-snapshot
  store and the `0001` signal.
- Model *runtime* implementation is illustrative in `plan.md`; executable code lands
  under `src/quantsmith/` only when a task authorizes it.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall define the prediction target as the cross-sectional 5-day forward excess return, labeled at an explicit decision time, using only returns realized strictly after that time. | must |
| REQ-002 | The system shall assemble features from a point-in-time feature store with offline/online parity, including the `0001` momentum signal, so training and serving see identical values as-of each decision time. | must |
| REQ-003 | The system shall use a leakage-controlled validation design — purged, embargoed, walk-forward cross-validation — with the momentum signal as the economic baseline to beat. | must |
| REQ-004 | The system shall train and register a supervised baseline model (gradient-boosted trees) with a model card and reproducible metrics. | must |
| REQ-005 | The system shall evaluate a deep-learning temporal challenger under the same folds and snapshot, and promote it only if it beats the baseline out-of-sample net of cost and serving overhead. | should |
| REQ-006 | The system shall emit a monitored production candidate whose drift, calibration, decay, and retraining triggers are documented in a run card and model card. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | Re-running on the pinned snapshot with fixed seeds reproduces reported metrics within a documented tolerance. |
| NFR-002 | No look-ahead / leakage | Every feature and label is as-of the decision time; validation folds are purged and embargoed so train and test label windows never overlap. |
| NFR-003 | Cost & capacity realism | Model comparison is reported net of transaction costs, with turnover and capacity, not on gross information coefficient alone. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a labeled dataset, when a label for decision time D is built, then it uses only forward returns realized strictly after D and no feature observed after D. | REQ-001, NFR-002 |
| AC-002 | Given the feature store, when a feature vector is requested as-of D, then the offline (training) and online (serving) paths return identical values for the same (name, D). | REQ-002 |
| AC-003 | Given walk-forward folds, when the purge and embargo are applied, then no training sample's label window overlaps any validation sample's feature or label window. | REQ-003, NFR-002 |
| AC-004 | Given the same folds and snapshot, when the baseline and challenger are evaluated, then rank IC and net-of-cost metrics are computed on identical, non-overlapping test periods. | REQ-004, REQ-005, NFR-003 |
| AC-005 | Given a registered candidate, when monitoring runs, then drift, calibration, and decay metrics with thresholds and a retraining trigger are emitted. | REQ-006 |
| AC-006 | Given the pinned snapshot and seeds, when training runs twice, then reported metrics match within the documented tolerance. | NFR-001 |

## Data & Dependencies

- Adjusted daily close prices for the reference universe, point-in-time (shared
  price-snapshot store; read-only).
- The `0001` momentum score panel as an input feature (point-in-time).
- Daily liquidity and realized-volatility metrics for feature construction and the
  liquidity filter.
- Dependency: the ML/DL agent groups for routing (`agents/machine_learning/`,
  `agents/deep_learning/`) and the standards `instructions/machine_learning.md`,
  `instructions/deep_learning.md`, `instructions/model_development.md`,
  `instructions/model_validation.md`, `instructions/point_in_time.md`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Label leakage from overlapping forward-return windows. | Inflated out-of-sample metrics; a model that fails live. | Purge and embargo of one label horizon between train and test; label built strictly forward of the decision time (AC-001, AC-003). |
| RISK-002 | Offline/online feature skew. | Training-serving mismatch degrades live predictions silently. | Single point-in-time feature store with an offline/online parity test (AC-002). |
| RISK-003 | Overfitting via challenger complexity or search. | Deep model wins in-sample, loses net of cost/serving. | Identical folds, net-of-cost comparison, and a promotion bar above the baseline (REQ-005, AC-004). |
| RISK-004 | Alpha decay after deployment. | Forecast quality erodes unmonitored. | Drift/calibration/decay monitors with a retraining trigger (AC-005). |

## Assumptions & Open Questions

- Assumption: adjusted prices already incorporate splits and dividends; the `0001`
  signal is available point-in-time.
- Assumption: excess return is measured against the universe (equal-weight) return;
  a factor-model residual is a later refinement.
- Open question: forecast horizon fixed at 5 trading days for v1 — revisit 1-day and
  21-day variants once the baseline is trusted (tracked, not silently deferred).

## Exceptions

None.
