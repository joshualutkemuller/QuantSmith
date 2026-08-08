# Plan: Optimal execution scheduling

- **Spec:** 0012-execution-scheduling (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Implement the closed-form Almgren-Chriss optimal liquidation trajectory. Feasibility
holds *by construction*: the trajectory is pinned to the full size at the start and
zero at the end, so it always fully liquidates, and for a pure liquidation the
holdings are monotone and non-negative. The cost/risk trade-off is a single
parameter (risk aversion), and both expected cost and variance are reported so the
trade-off is explicit. Pure Python (`math.sinh`/`math.acosh`) so the reference runs
anywhere.

## Agent Routing

The workflow is the optimization group's execution branch (see `docs/workflows.md`
→ *Optimization Problem Build*):

```text
optimization_orchestrator
  -> problem_formulation             # objective: cost + lambda * variance, constraints
  -> execution_optimization          # Almgren-Chriss schedule
  -> solver_diagnostics_sensitivity  # sensitivity to risk aversion and impact
  -> backtest_review / risk          # net-of-cost impact on the strategy
```

Upstream: `0007-portfolio-construction` supplies the target trade to execute.

## Architecture & Components

- `ExecutionSchedule` — holdings (N+1) and trades (N), plus `expected_cost()` and
  `cost_variance()`.
- `optimal_schedule(total, n_periods, eta, gamma, sigma, risk_aversion, tau)` —
  the Almgren-Chriss trajectory; risk-neutral limit is the linear (TWAP) path.
- Cost model: permanent `0.5*gamma*X^2` + temporary `eta*sum(n_k^2)/tau`; variance
  `sigma^2*tau*sum(x_k^2)`.

## Interfaces & Data Contracts

- Input: total size, N periods, `eta`, `gamma`, `sigma`, `risk_aversion`, `tau`,
  as-of the execution window; requires `eta - 0.5*gamma*tau > 0`.
- Output: an `ExecutionSchedule` with holdings, trades, and cost/variance methods.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Trajectory pinned to X→0; monotone, non-negative liquidation; deterministic. |
| P5 Reversibility | yes | A schedule is a plan; recompute with new parameters, nothing to roll back. |
| P6 Observability | yes | Reports expected cost and cost variance per schedule. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Both cost and variance reported; the risk taken is never hidden. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `optimal_schedule` trajectory | T-001 |
| REQ-002 | terminal pinning + trade differencing | T-001 |
| REQ-003 | risk-neutral linear limit vs sinh trajectory | T-002 |
| REQ-004 | `expected_cost` / `cost_variance` | T-003 |
| NFR-001 | closed-form deterministic math | T-001 |
| NFR-002 | monotone non-negative liquidation | T-001 |
| NFR-003 | report both cost and variance | T-003 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Model | Almgren-Chriss closed form | Numerical dynamic program | Closed form is exact, fast, and deterministic for the linear-impact case. |
| Impact | Linear temporary + permanent | Nonlinear / transient | Linear is the standard first model; nonlinear impact is a follow-up. |
| Risk-neutral limit | Explicit linear (TWAP) branch | Let kappa→0 numerically | Avoids a 0/0 limit; the TWAP path is exact and clean. |
| Objective | Cost + lambda*variance | Cost only | Cost-only ignores the price risk of working the order (P10). |

## Validation Strategy

- AC-001/002: assert shape and full liquidation (trades sum to total, terminal zero).
- AC-003: assert TWAP at lambda=0 and front-loading at lambda>0.
- AC-004: assert the more risk-averse schedule has lower variance and higher cost.
- AC-005: assert monotone non-increasing, non-negative holdings and non-negative trades.
- AC-006: assert two runs are identical.

## Rollout, Observability & Rollback

A library consumed by execution and backtest review. There is nothing to roll back;
a changed impact/volatility estimate or risk aversion simply changes the schedule, and
both cost and variance travel with it for review.

## Open Questions

- Extend to multi-asset joint execution, adaptive (state-dependent) schedules, and
  nonlinear/transient impact.
