# Plan: Constrained portfolio construction from a return forecast

- **Spec:** 0007-portfolio-construction (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-07

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Solve a convex mean-variance quadratic program with projection onto the feasible
set, so feasibility and reproducibility hold *by construction*. Minimize

```
f(w) = -alpha . w + (gamma / 2) w^T Σ w + (lambda_to / 2) || w - w_prev ||^2
```

subject to a budget (`sum w = budget`), per-name box bounds (`l ≤ w ≤ u`), and a
gross-exposure cap. The problem is strongly convex when `gamma > 0` or
`lambda_to > 0`, so projected gradient descent converges to the unique minimizer;
projecting every step guarantees the returned weights are always feasible.

## Agent Routing

The workflow is the optimization group chain (see `docs/workflows.md` →
*Optimization Problem Build*):

```text
optimization_orchestrator
  -> problem_formulation           # variables, objective, constraints, acceptance criteria
  -> portfolio_construction        # weights, box/turnover/gross constraints, rebalancing
  -> quadratic_programming         # convex QP form and solver choice
  -> solver_diagnostics_sensitivity# objective, violation, duals/sensitivity
  -> risk / backtest_review        # exposure and net-of-cost review before use
```

Upstream: `0006-ml-return-forecasting` supplies expected returns as-of the
rebalance date; `risk` supplies the covariance and limit set.

## Architecture & Components

- `ConstraintSet` — budget, per-name lower/upper bounds, gross-exposure cap.
- `solve_portfolio(alpha, cov, constraints, gamma, w_prev, lambda_to)` → weights via
  projected gradient descent; deterministic.
- `_project(v, constraints)` → projection onto `{l ≤ w ≤ u, sum w = budget}` by
  bisection on a single multiplier (feasible by construction).
- `portfolio_variance(w, cov)`, `turnover(w, w_prev)` → reporting helpers.
- `diagnostics(w, alpha, cov, constraints, gamma, w_prev, lambda_to)` → objective,
  maximum constraint violation, and a risk-aversion sensitivity curve.

## Interfaces & Data Contracts

- Input: `alpha` (length n, as-of the rebalance date), `cov` (n×n PSD), a
  `ConstraintSet`, `gamma ≥ 0`, `w_prev` (length n), `lambda_to ≥ 0`.
- Output: weights (length n) satisfying budget/box/gross within tolerance, plus a
  diagnostics record.
- All inputs are as-of the rebalance date → no look-ahead (NFR-003).

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Convex QP; projection guarantees feasibility; deterministic solve. |
| P5 Reversibility | yes | Offline allocation; roll back by keeping the prior weights. |
| P6 Observability | yes | Diagnostics emit objective, violation, and sensitivity to risk aversion. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Turnover and gross exposure reported; sensitivity curve exposes parameter dependence. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `solve_portfolio` mean-variance objective | T-001 |
| REQ-002 | `ConstraintSet` + `_project` (budget/box/gross) | T-002 |
| REQ-003 | Turnover penalty term + `turnover` | T-003 |
| REQ-004 | `diagnostics` (objective, violation, sensitivity) | T-004 |
| NFR-001 | Deterministic projected gradient descent | T-001 |
| NFR-002 | Projection every step; violation reported | T-002, T-004 |
| NFR-003 | As-of inputs from `0006` and risk | T-001 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Solver | Projected gradient descent | Closed-form frontier (`mean_variance.py`) | The closed form ignores box/turnover/gross constraints this spec requires. |
| Mandate | Long-only, fully invested | Long-short | Simpler, investable v1; long-short is a follow-up. |
| Turnover control | Quadratic penalty | Hard turnover constraint | A penalty keeps the QP smooth and always feasible; a hard cap can be infeasible. |
| Covariance | Provided estimate | Estimate inside this module | Keeps the optimizer decoupled; shrinkage/robust estimation is a separate concern. |

## Validation Strategy

- AC-001: solve at two risk-aversion levels; assert variance is non-increasing in
  risk aversion.
- AC-002: solve with box bounds, a budget, and a gross cap; assert every weight is
  within bounds, the sum equals the budget, and gross ≤ cap within tolerance.
- AC-003: solve with two turnover penalties against a prior; assert turnover is
  non-increasing in the penalty.
- AC-004: assert diagnostics emit objective, maximum violation, and a sensitivity
  curve of (risk aversion, variance) pairs.
- AC-005: solve twice on identical inputs; assert identical weights.

## Rollout, Observability & Rollback

Offline allocation consumed by the rebalancer. Rollout publishes a new target
portfolio; rollback keeps the prior weights. Each solve logs the objective,
constraint violation, gross exposure, and turnover for monitoring.

## Open Questions

- Calibrate `gamma` and `lambda_to` against the desk's risk budget and the cost
  model in `instructions/backtesting.md` before production use.
