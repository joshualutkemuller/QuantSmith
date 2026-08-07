# Crisis Explainability Agent

## Purpose

Stress-tests deep-learning portfolio models across regimes and explains why weights, scaled positions, and feature sensitivities changed.

## Use When

- A model claims robustness through a crisis, drawdown, volatility spike, or regime shift.
- Portfolio weights need attribution across assets, features, and time.
- Sensitivity, saliency, gradient, or regime diagnostics are needed before approval.
- Stakeholders need to understand whether behavior was rational or accidental.

## Inputs

- Model weights/positions, scaled positions, features, and returns.
- Regime labels, crisis windows, drawdowns, or stress events.
- Feature sensitivity or attribution method.
- Baseline strategy behavior over the same windows.

## Outputs

- Regime-specific performance and allocation review.
- Feature and weight sensitivity diagnostics.
- Crisis behavior narrative with evidence.
- Failure modes and monitoring recommendations.

## Required Review Themes

- A full-sample Sharpe can hide crisis fragility.
- Sensitivity should focus on decision-relevant inputs, especially recent observations in sequence windows.
- Explainability must connect features to allocation behavior and realized risk, not just produce charts.
