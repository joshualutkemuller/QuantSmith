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
| T-001 | Implement `build_labels` (5-day forward excess return, explicit decision time). | REQ-001, NFR-002, AC-001 | todo | `problem_framing_labeling` | Label strictly forward of D; no future feature. |
| T-002 | Implement `assemble_features` from the PIT feature store with offline/online parity (incl. `0001` momentum). | REQ-002, NFR-002, AC-002 | todo | `feature_store_engineering` | Single as-of code path; parity test. |
| T-003 | Implement `make_folds` (purged, embargoed walk-forward) with the momentum baseline. | REQ-003, NFR-002, AC-003 | todo | `model_selection_validation` | Purge + embargo one label horizon. |
| T-004 | Train and register the gradient-boosted baseline; write the model card; pin snapshot and seed. | REQ-004, NFR-001, AC-006 | todo | `supervised_learning` | Reproducible metrics within tolerance. |
| T-005 | Train the deep temporal challenger on identical folds; compare net of cost with turnover/capacity. | REQ-005, NFR-001, NFR-003, AC-004 | todo | `deep_time_series` / `training_systems` | Promote only above the baseline bar. |
| T-006 | Register the production candidate; emit drift/calibration/decay monitors and a retraining trigger; write the run card. | REQ-006, AC-005 | todo | `mlops_monitoring` / `compression_serving` | Thresholds documented in the run card. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `test_label_forward_only_AC-001` | todo |
| AC-002 | `test_feature_offline_online_parity_AC-002` | todo |
| AC-003 | `test_folds_purged_embargoed_AC-003` | todo |
| AC-004 | `test_baseline_challenger_comparable_AC-004` | todo |
| AC-005 | `test_monitoring_emitted_AC-005` | todo |
| AC-006 | `test_training_reproducible_AC-006` | todo |

## Follow-ups

- Confirm the transaction-cost model and turnover budget with the desk; update
  REQ-005 / the plan if the promotion bar changes (tracked, not silently deferred).
- Once the baseline is trusted, spec 1-day and 21-day horizon variants (open
  question in `spec.md`).
- Add a factor-model residual target as a refinement over universe-excess return.
