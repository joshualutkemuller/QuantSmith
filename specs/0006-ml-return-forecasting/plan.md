# Plan: Cross-sectional short-horizon return forecasting model

- **Spec:** 0006-ml-return-forecasting (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-07

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Build the forecast as a deterministic pipeline from a point-in-time snapshot to a
per-name daily prediction, with leakage safety and reproducibility holding *by
construction*: labels are built strictly forward of the decision time, features are
served as-of that time from one store, and validation folds are purged and
embargoed. A supervised gradient-boosted model is the trusted baseline; a deep
temporal model is a challenger held to the same rules and net-of-cost bar. Nothing
is promoted on gross information coefficient alone.

## Agent Routing

The workflow is the ML build chain with a DL challenger loop (see
`docs/workflows.md` → *Machine Learning Build* / *Deep Learning Build*):

```text
ml_orchestrator
  -> problem_framing_labeling      # target, decision time, label horizon, leakage boundary
  -> feature_store_engineering     # PIT features, offline/online parity, provenance
  -> supervised_learning           # gradient-boosted baseline
  -> model_selection_validation    # purged/embargoed walk-forward, baseline bar
  -> mlops_monitoring              # register, drift/decay, retraining triggers

# challenger loop, same folds and snapshot:
dl_orchestrator -> training_systems -> deep_time_series -> compression_serving
  -> model_selection_validation (shared) -> mlops_monitoring (shared)
```

Lifecycle handoffs: `testing_validation` owns the acceptance tests; `risk` and
`backtest_review` review the net-of-cost economics before promotion.

## Architecture & Components

- `build_labels(snapshot, horizon=5)` → forward excess-return label per
  (decision_date, name), realized strictly after the decision time.
- `assemble_features(as_of)` → point-in-time feature panel from the feature store
  (momentum from `0001`, realized volatility, liquidity, short-term reversal), with
  identical offline and online code paths.
- `make_folds(dates, purge, embargo)` → purged, embargoed walk-forward splits.
- `train_baseline(X, y, folds)` → gradient-boosted trees; returns a registered model
  and per-fold metrics.
- `train_challenger(X_seq, y, folds)` → compact deep temporal model built via
  `training_systems` (seeded, deterministic loaders); same folds.
- `evaluate(model, folds)` → rank IC, net-of-cost decile spread, turnover, capacity
  on the held-out test periods.
- `register_and_monitor(model)` → model card + run card + drift/calibration/decay
  monitors and a retraining trigger.

## Interfaces & Data Contracts

- Input: adjusted daily close panel and the `0001` score panel; monotonic dates; no
  duplicate (date, name).
- Label for decision date D uses only returns over (D, D+5 trading days]; features
  for D use only rows with timestamp ≤ D → no look-ahead.
- Output: prediction panel (date, name, score) plus a model card, run card, and a
  fold-level metrics table.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Forward-only labels, as-of features, purged/embargoed folds, seeded training — leakage and repro hold structurally. |
| P5 Reversibility | yes | Offline batch candidate; promote by registering a version, roll back by repointing consumers to the prior model. |
| P6 Observability | yes | Emits fold metrics, coverage, and drift/calibration/decay monitors with thresholds. |
| P9 Security & data | yes | Read-only snapshot; no private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Comparison is net of cost with turnover/capacity; the challenger is promoted only above the baseline bar. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `build_labels` (forward excess return, decision time) | T-001 |
| REQ-002 | `assemble_features` (PIT store, offline/online parity) | T-002 |
| REQ-003 | `make_folds` (purge + embargo, momentum baseline) | T-003 |
| REQ-004 | `train_baseline` + model card | T-004 |
| REQ-005 | `train_challenger` + net-of-cost comparison | T-005 |
| REQ-006 | `register_and_monitor` (drift/decay/retraining) | T-006 |
| NFR-001 | Pinned snapshot, seeded training, tolerance | T-004, T-005 |
| NFR-002 | Forward-only labels, as-of features, purge/embargo | T-001, T-002, T-003 |
| NFR-003 | Net-of-cost evaluation with turnover/capacity | T-005 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Target | 5-day forward *excess* return | Raw forward return | Excess isolates cross-sectional alpha from market beta. |
| Baseline model | Gradient-boosted trees | Linear/logistic | Captures nonlinear feature interactions while staying inspectable and cheap to serve. |
| Challenger | Compact deep temporal model | Large transformer | Start with the smallest deep model that could win; escalate only if data supports it (`deep_time_series`). |
| Validation | Purged, embargoed walk-forward | Random k-fold | k-fold leaks across the label horizon and shuffles time order. |
| Promotion bar | Net-of-cost OOS above baseline | Gross rank IC | Gross IC ignores turnover, cost, and serving overhead. |

## Validation Strategy

- AC-001: unit test building a label at D with a planted post-D-plus-6 spike; assert
  the label depends only on the (D, D+5] window and no future feature.
- AC-002: parity test requesting the same (name, D) vector from the offline and
  online paths; assert equality.
- AC-003: property test over generated folds asserting no train label window overlaps
  any test feature/label window after purge + embargo.
- AC-004: comparability test asserting baseline and challenger metrics come from
  identical, non-overlapping test periods on the same snapshot.
- AC-005: monitoring test asserting drift, calibration, and decay metrics and a
  retraining trigger are emitted with thresholds.
- AC-006: reproducibility test running training twice on the pinned snapshot/seed;
  assert reported metrics match within tolerance.

## Rollout, Observability & Rollback

Offline batch candidate consumed by downstream portfolio work. Rollout registers a
new model version behind the model card; rollback repoints consumers to the prior
version. Each run logs coverage, fold metrics, and the drift/calibration/decay
monitors that feed the retraining trigger.

## Open Questions

- Confirm the transaction-cost model and turnover budget with the desk before the
  net-of-cost promotion bar is finalized (defaulting to the shared cost assumptions
  in `instructions/backtesting.md` until confirmed).
