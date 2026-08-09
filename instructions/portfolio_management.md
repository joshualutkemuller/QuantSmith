# Portfolio Management Instructions

Use this instruction set when a workflow governs the full portfolio lifecycle:
mandate definition, universe selection, signal intake, allocation policy,
construction, implementation, risk, compliance, attribution, liquidity, tax,
monitoring, and governance.

## Operating Principles

- Start with the mandate, benchmark, investment horizon, decision owner, and
  permitted action space before discussing models or trades.
- Separate investment belief, forecast evidence, portfolio decision, execution
  decision, and monitoring evidence.
- Preserve point-in-time data availability for holdings, benchmarks, corporate
  actions, signals, prices, risk models, constraints, tax lots, and cash.
- State risk budgets, concentration limits, liquidity limits, turnover limits,
  leverage rules, benchmark tolerances, and compliance constraints explicitly.
- Compare proposed portfolio actions against a baseline such as current weights,
  benchmark weights, equal risk contribution, or a simple rebalance rule.
- Treat costs, liquidity, taxes, borrow/financing, capacity, and operational
  constraints as first-class inputs, not after-the-fact commentary.
- Route mathematical optimization to `agents/optimization/portfolio_construction/`
  and execution scheduling to `agents/optimization/execution_optimization/`.
- Keep private positions, client identifiers, MNPI, restricted lists, account
  numbers, and credentials out of prompts, examples, and repository artifacts.

## Lifecycle Checks

| Stage | Required checks |
| --- | --- |
| Mandate | Objective, benchmark, horizon, constraints, governance, and non-goals are explicit. |
| Universe | Eligibility, survivorship, corporate actions, liquidity, and coverage gaps are documented. |
| Signal intake | Forecast horizon, as-of timestamp, leakage controls, decay, calibration, and confidence are known. |
| Allocation | Risk budget, factor exposure, capital budget, sizing logic, and fallback baseline are defined. |
| Construction | Objective, constraints, costs, feasibility, diagnostics, and handoffs are reviewable. |
| Implementation | Trade list, turnover, execution constraints, cash effects, and rollback plan are clear. |
| Risk/compliance | Exposures, limits, scenario losses, restricted assets, and approvals are checked before action. |
| Attribution | Return, risk, cost, timing, sizing, and selection effects are decomposed honestly. |
| Monitoring | Drift, breaches, model decay, stale data, capacity, and governance review cadence are defined. |

## Output Contract

Use clear Markdown sections: `Portfolio Stage`, `Decision Context`, `Inputs`,
`Recommendation`, `Risks And Constraints`, `Validation`, `Workflow Handoff`, and
`Spec Updates`.

When proposing implementation work, include spec-ready `REQ-*`, `NFR-*`, `AC-*`,
and `RISK-*` entries and name the next lifecycle or specialist agent.
