# Differentiable Objective Agent Tasks

## Standard Tasks

1. Translate the investment goal into a differentiable objective.
2. Define portfolio-return calculation using lagged weights.
3. Document mean, volatility, downside-risk, or diversification terms.
4. Decide whether costs and turnover are inside the objective.
5. Specify stability protections and unit tests.
6. Map training objective to evaluation metrics and acceptance criteria.

## Evidence to Collect

- Objective formula.
- Lag-alignment test.
- Denominator-stability test.
- Cost inclusion/exclusion rationale.
- Metric reporting template.

## Red Flags

- Optimizing prediction error when the decision is allocation.
- Objective uses future information.
- Ratio objective without stability safeguards.
- Cost-free objective with high-turnover output.
- Single metric reported as proof of success.
