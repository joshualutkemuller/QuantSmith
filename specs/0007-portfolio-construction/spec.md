# Spec: Constrained portfolio construction from a return forecast

- **ID:** 0007-portfolio-construction
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-07

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> First runtime workflow promoted from the `agents/optimization/` group (spec
> `0004`). Consumes the `0006-ml-return-forecasting` forecast as expected returns.

## Problem & Context

The desk now has a learned return forecast (`specs/0006-ml-return-forecasting`) but
no disciplined way to turn it into a portfolio. Turning scores into weights ad hoc
ignores risk, position limits, and rebalancing cost, and cannot be reviewed. This
spec defines constrained portfolio construction as a first-class artifact: a
mean-variance allocation over the forecast that respects box bounds, a budget, a
gross-exposure cap, and a turnover penalty, with solver diagnostics a reviewer can
trust. It is the first runtime workflow that routes the optimization specialist
agents from formulation through solver diagnostics.

## Goals

- Turn a point-in-time return forecast and covariance into portfolio weights that
  trade expected alpha against risk.
- Enforce position, budget, gross-exposure, and turnover constraints so the result
  is investable and its rebalancing cost is controlled.
- Emit solver diagnostics — objective, constraint satisfaction, and sensitivity to
  the risk-aversion parameter — so the allocation is inspectable.

## Non-Goals

- Producing the forecast itself (owned by `0006`) or trading/execution (a later
  execution-optimization spec).
- A general-purpose QP solver library; this slice ships a focused, deterministic
  reference solver for the mean-variance form.
- Transaction-cost *modelling* beyond a turnover penalty proxy.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall construct portfolio weights that maximize forecast alpha minus a risk penalty (mean-variance objective) using the `0006` forecast as expected returns. | must |
| REQ-002 | The system shall enforce constraints: a full-investment budget, per-name box bounds, and a gross-exposure cap. | must |
| REQ-003 | The system shall penalize turnover against a prior portfolio so rebalancing cost is controlled. | must |
| REQ-004 | The system shall emit solver diagnostics: objective value, maximum constraint violation, and a risk-aversion sensitivity curve. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same inputs yield identical weights on every solve. |
| NFR-002 | Feasibility by construction | Returned weights satisfy the budget, box, and gross-exposure constraints within a documented tolerance. |
| NFR-003 | No look-ahead | Expected returns and covariance are consumed as-of the rebalance date; no future information enters the allocation. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a forecast and covariance, when the risk-aversion parameter is increased, then the solved portfolio's variance does not increase. | REQ-001 |
| AC-002 | Given box bounds, a budget, and a gross cap, when weights are returned, then each weight is within its bounds, the weights sum to the budget, and gross exposure is at most the cap. | REQ-002, NFR-002 |
| AC-003 | Given a prior portfolio and a turnover penalty, when the penalty is increased, then realized turnover against the prior does not increase. | REQ-003 |
| AC-004 | Given a solve, when diagnostics are produced, then the objective value, the maximum constraint violation, and a risk-aversion sensitivity curve are emitted. | REQ-004 |
| AC-005 | Given identical inputs, when the solver runs twice, then the returned weights are identical. | NFR-001 |

## Data & Dependencies

- Expected returns: the `0006` forecast (prediction panel), as-of the rebalance date.
- Covariance: a point-in-time estimate from trailing returns over the reference
  universe.
- A prior portfolio (previous weights) for the turnover penalty; the zero portfolio
  on the first rebalance.
- Standards: `instructions/model_development.md`, `instructions/backtesting.md`
  (cost/turnover assumptions), and the `optimization` agent group.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Infeasible or corner solutions from tight constraints. | Unusable or degenerate portfolios. | Projection onto the feasible set every step; diagnostics report the maximum violation (AC-002, AC-004). |
| RISK-002 | Estimation error in expected returns/covariance amplifies concentration. | Fragile, over-fit allocations. | Box bounds, a gross cap, and a risk penalty; a robust/shrinkage variant is a follow-up. |
| RISK-003 | Turnover ignored, so paper alpha is lost to trading cost. | Overstated live performance. | Turnover penalty against the prior portfolio (REQ-003, AC-003). |
| RISK-004 | Look-ahead from using non-point-in-time inputs. | Inflated backtests. | Consume `0006` outputs and covariance as-of the rebalance date (NFR-003). |

## Assumptions & Open Questions

- Assumption: a long-only, fully-invested mandate for v1 (budget = 1, weights ≥ 0);
  long-short is a follow-up.
- Assumption: the covariance estimate is provided; shrinkage/robust estimation is
  out of scope here.
- Open question: calibrate the risk-aversion and turnover-penalty parameters against
  the desk's cost model and risk budget (tracked, not silently deferred).

## Exceptions

None.
