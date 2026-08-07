# Machine Learning Agents

The Machine Learning group covers predictive, causal, ranking, online, unsupervised, experiment, feature-store, validation, and MLOps workflows.

## Group Workflow

```text
ml_orchestrator -> problem_framing_labeling -> feature_store_engineering -> specialist ML agent -> model_selection_validation -> mlops_monitoring
```

## Agents

| Agent | Handles |
| --- | --- |
| `ml_orchestrator/` | Routes ML work from framing through labeling, features, validation, deployment, monitoring, and retraining. |
| `problem_framing_labeling/` | Defines targets, labels, horizons, decision times, leakage boundaries, class balance, and label quality. |
| `feature_store_engineering/` | Designs reusable ML features, point-in-time joins, entity keys, offline/online parity, and feature provenance. |
| `supervised_learning/` | Covers regression/classification models, baselines, calibration, imbalance, metric choice, and segment errors. |
| `time_series_forecasting/` | Handles forecasting, temporal validation, hierarchical series, exogenous drivers, revisions, and forecast reconciliation. |
| `ranking_recommendation/` | Designs ranking, recommendation, learning-to-rank, retrieval, candidate generation, and evaluation at rank. |
| `causal_uplift/` | Reviews treatment effects, uplift, experiments, observational bias, instruments, diff-in-diff, and causal identification. |
| `unsupervised_anomaly/` | Handles clustering, dimensionality reduction, outliers, novelty detection, drift probes, and alert quality. |
| `model_selection_validation/` | Owns baselines, validation design, hyperparameter search, leakage controls, robustness, and error analysis. |
| `automl_experimentation/` | Governs broad searches, experiment tracking, multiple-testing control, reproducibility, and search-space discipline. |
| `online_learning_bandits/` | Covers contextual bandits, exploration/exploitation, delayed feedback, guardrails, regret, and online updates. |
| `mlops_monitoring/` | Defines model packaging, serving, drift, calibration, retraining triggers, run cards, and production ownership. |

## Inputs

- Current `spec.md`, `plan.md`, `tasks.md`, or handoff memo when available.
- Business decision, objective, constraints, and risk limits.
- Data contracts, source provenance, point-in-time assumptions, and refresh cadence.
- Runtime expectations for `src/quantsmith/`, notebooks, adapters, or downstream systems.

## Outputs

- Specialist routing plan.
- Spec-ready requirements, risks, acceptance criteria, and task suggestions.
- Method, baseline, validation, monitoring, and deployment recommendations.
- Handoffs to lifecycle agents, data agents, risk, testing, reporting, and adapters.

## Rules

- Keep each specialist narrow and inspectable.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.
- Use adapters for provider/runtime boundaries and `src/quantsmith/` for executable code.
- Treat this group as decision support and workflow design unless a spec authorizes implementation.
