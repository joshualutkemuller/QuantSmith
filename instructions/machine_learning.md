# Machine Learning Instructions

## Purpose

Use this standard when designing, reviewing, or operating machine-learning systems for forecasting, classification, ranking, anomaly detection, causal inference, and online decisioning.

## Required Inputs

- Decision supported by the model and the cost of wrong decisions.
- Entity, timestamp, target, horizon, label source, and feature availability.
- Training, validation, test, and production windows.
- Baseline model, candidate model classes, metrics, and acceptance thresholds.
- Monitoring, retraining, and rollback expectations.

## Standards

- Define labels at the decision time; prevent leakage through future labels, global preprocessing, joins, and target encodings.
- Use chronological or deployment-faithful validation for time-dependent data.
- Establish a baseline before model selection.
- Separate exploration, selection, final validation, and production monitoring.
- Track the number of experiments and protect against multiple-testing overconfidence.
- Evaluate by segment, regime, calibration, ranking quality, and business impact where relevant.
- Produce a model card, run card, feature contract, and monitoring plan for production candidates.

## Common Failure Modes

- Random train/test splits for temporal decisions.
- Labels revised after decision time without a point-in-time correction.
- Aggregate metrics hiding failure in the segment that matters.
- AutoML or broad search with no search-space record.
- Monitoring only model latency while ignoring drift, calibration, and outcome decay.

## Spec-Driven Alignment

ML work maps target, horizon, and prediction purpose to `REQ-*`; latency, retraining, interpretability, and monitoring to `NFR-*`; validation, baseline lift, calibration, and drift evidence to `AC-*`; and leakage, overfitting, label noise, fairness/compliance, and data drift to `RISK-*`.
