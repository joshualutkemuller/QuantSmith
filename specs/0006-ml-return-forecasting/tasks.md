# Tasks: Cross-sectional short-horizon return forecasting model

- **Spec:** 0006-ml-return-forecasting (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Reproducibility preserved (pinned snapshot, seeded, no hidden state).
- Leakage controls hold: forward-only labels, as-of features, purged/embargoed folds.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs/cards updated alongside the change (model card, run card).

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `build_labels` (5-day forward excess return, explicit decision time). | REQ-001, NFR-002, AC-001 | done | `problem_framing_labeling` | `src/quantsmith/pipelines/return_forecasting.py`; label strictly forward of D. |
| T-002 | Implement `assemble_features` from the PIT feature store with offline/online parity (incl. `0001` momentum). | REQ-002, NFR-002, AC-002 | done | `feature_store_engineering` | `FeatureStore` single as-of code path; parity test. |
| T-003 | Implement `make_folds` (purged, embargoed walk-forward) with the momentum baseline. | REQ-003, NFR-002, AC-003 | done | `model_selection_validation` | Purge + embargo one label horizon. |
| T-004 | Train and register the gradient-boosted baseline; write the model card; pin snapshot and seed. | REQ-004, NFR-001, AC-006 | done | `supervised_learning` | `train_baseline` closed-form reference stand-in for GBT; deterministic. |
| T-005 | Train the deep temporal challenger on identical folds; compare net of cost with turnover/capacity. | REQ-005, NFR-001, NFR-003, AC-004 | done | `deep_time_series` / `training_systems` | `train_challenger` seeded reference stand-in; `evaluate` is net of cost. |
| T-006 | Register the production candidate; emit drift/calibration/decay monitors and a retraining trigger; write the run card. | REQ-006, AC-005 | done | `mlops_monitoring` / `compression_serving` | `monitor` emits metrics + retraining trigger with thresholds. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only *reference* pipeline in
`src/quantsmith/pipelines/return_forecasting.py` that makes the contracts
executable and testable everywhere. Production builds swap `train_baseline` /
`train_challenger` for real models (gradient-boosted trees, a deep temporal
network); the model card and run card are authored when a real model is trained.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_return_forecasting.py::test_label_forward_only_AC_001` | done |
| AC-002 | `tests/test_return_forecasting.py::test_feature_offline_online_parity_AC_002` | done |
| AC-003 | `tests/test_return_forecasting.py::test_folds_purged_embargoed_AC_003` | done |
| AC-004 | `tests/test_return_forecasting.py::test_baseline_challenger_comparable_AC_004` | done |
| AC-005 | `tests/test_return_forecasting.py::test_monitoring_emitted_AC_005` | done |
| AC-006 | `tests/test_return_forecasting.py::test_training_reproducible_AC_006` | done |

## Follow-ups

- Confirm the transaction-cost model and turnover budget with the desk; update
  REQ-005 / the plan if the promotion bar changes (tracked, not silently deferred).
- Once the baseline is trusted, spec 1-day and 21-day horizon variants (open
  question in `spec.md`).
- Add a factor-model residual target as a refinement over universe-excess return.
