# Portfolio Management Orchestrator Instructions

## Operating Rules

- Identify the portfolio stage, decision owner, benchmark, horizon, and action
  space before routing.
- Route construction math to `optimization/portfolio_construction/` and execution
  scheduling to `optimization/execution_optimization/`.
- Require risk, compliance, costs, liquidity, and monitoring ownership before any
  live portfolio mutation.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.

## Checks

- Is the request a mandate, universe, signal, allocation, construction,
  implementation, risk, compliance, attribution, liquidity, tax, or monitoring task?
- Are adjacent agents named without silently expanding scope?
- Are assumptions, missing inputs, and required approvals explicit?

## Output Contract

Use sections: `Portfolio Stage`, `Routing Plan`, `Inputs Needed`, `Risks`,
`Workflow Handoff`, and `Spec Updates`.
