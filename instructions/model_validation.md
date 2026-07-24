# Model Validation Instructions

## Purpose

Use this instruction set to review forecasting models, classification models, ranking models, risk models, and other statistical or machine-learning systems.

## Required Inputs

- Model purpose and intended decision.
- Training, validation, and test windows.
- Feature and label definitions.
- Data lineage and point-in-time assumptions.
- Model class and configuration.
- Metrics and baseline.
- Error analysis and monitoring plan.

## Expected Output

- Model validation review.
- Baseline comparison.
- Data split and leakage assessment.
- Metric suitability review.
- Robustness and sensitivity checks.
- Known limitations.
- Monitoring and retraining recommendations.

## Standards

- Match validation design to the deployment setting.
- Use time-aware splits for time-series and market data.
- Compare against simple baselines.
- Report uncertainty where practical.
- Include error analysis by segment, time period, regime, and entity group.
- Document feature availability and transformation logic.
- Explain what will be monitored after deployment.

## Checks

- Are train, validation, and test boundaries appropriate?
- Is there leakage through preprocessing, scaling, imputation, target encoding, or feature selection?
- Are metrics aligned with business or investment use?
- Does the model improve over a simple baseline after realistic costs or constraints?
- Are errors concentrated in important regimes or populations?
- Is the model stable under reasonable data or parameter perturbations?

## Common Failure Modes

- Random splits on time-dependent data.
- Global preprocessing before splitting.
- Evaluating on a metric unrelated to the decision.
- Ignoring calibration, tails, or ranking quality when they matter.
- Reporting aggregate performance while hiding poor segment performance.
- Missing monitoring plans for drift and degradation.

## Spec-Driven Alignment

This standard backs the Verify step and feeds Maintenance. The validation design
and metric targets become `AC-*`/`NFR-*`; leakage through preprocessing or splits
is a P4 defect (see `instructions/point_in_time.md`); the post-deployment plan
becomes `templates/docs/model_monitoring_plan.md` with drift and decay thresholds.
A model is not done until every `AC-*` has passing, deterministic evidence
(constitution P3) and it can be told whether it is working in production (P6).
