# Plan: Optimization solvers by mathematical form

- **Spec:** 0013-optimization-solvers (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

One module of small, correct, deterministic solvers — one per mathematical form —
each with an explicit status. Termination and honesty hold *by construction*: the
simplex uses Bland's rule (no cycling), branch-and-bound is node-bounded, and every
solver returns a named status instead of a silent number on infeasible/unbounded
inputs. Pure Python so the reference runs anywhere.

## Agent Routing

The workflow is the optimization group's mathematical-form specialists (see
`docs/workflows.md` → *Optimization Problem Build*):

```text
optimization_orchestrator -> problem_formulation
  -> linear_programming | mixed_integer_optimization | network_flow | dynamic_programming
  -> solver_diagnostics_sensitivity -> (application spec)
```

Convex QP is provided by `portfolio_construction` / `quadratic_programming`
(`0007`). Application specs (collateral LP, cardinality portfolio, funding-ladder
flow, multi-period rebalancing) build on these solvers.

## Architecture & Components

- `solve_lp(c, A_ub, b_ub, A_eq, b_eq, sense)` → `LPResult(status, x, objective)` —
  two-phase simplex over standard form with slacks and artificials.
- `_two_phase_simplex`, `_run_simplex`, `_pivot` — the simplex internals.
- `solve_milp(..., integer_vars, sense, max_nodes)` → `LPResult` — branch-and-bound
  on the LP relaxation with incumbent pruning.
- `min_cost_flow(n, edges, source, sink, required_flow)` → `FlowResult` — successive
  shortest augmenting paths (Bellman-Ford potentials) on the residual graph.
- `DPProblem` / `solve_dp` → `DPResult(values, policy)` — finite-horizon backward
  induction over a deterministic transition.

## Interfaces & Data Contracts

- LP/MILP: `x >= 0`; `A_ub x <= b_ub`, `A_eq x = b_eq`; `sense` in {min, max}.
- Flow: edges as `(u, v, capacity, cost)`; non-negative capacities.
- DP: `states`, `actions(s)`, `step(s, a) -> (next_state, reward)`, horizon, discount.
- Every result exposes an explicit status (LP/flow) or complete value/policy (DP).

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Bland's rule (no cycling), node-bounded B&B, backward induction is exact. |
| P5 Reversibility | yes | Pure computation; nothing to roll back. |
| P6 Observability | yes | Explicit statuses and objective/flow/value reporting. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Infeasible/unbounded are named, never returned as a number. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `solve_lp` + `_two_phase_simplex` | T-001 |
| REQ-002 | infeasible/unbounded status propagation | T-001 |
| REQ-003 | `solve_milp` branch-and-bound | T-002 |
| REQ-004 | `min_cost_flow` | T-003 |
| REQ-005 | `DPProblem` / `solve_dp` | T-004 |
| NFR-001 | deterministic algorithms | T-001..T-004 |
| NFR-002 | Bland's rule + node limit | T-001, T-002 |
| NFR-003 | named statuses on all solvers | T-001, T-003 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| LP algorithm | Two-phase simplex, Bland's rule | Big-M / interior point | Bland's rule guarantees termination; two-phase is robust and dependency-free. |
| MILP | Branch-and-bound + node limit | Cutting planes | B&B is simple, exact for small problems, and easy to bound. |
| Flow | Successive shortest paths (Bellman-Ford) | Network simplex | Handles residual costs simply and correctly for a reference. |
| Scope | LP/MILP/flow/DP | Also conic/global/nonlinear | Those need a cone/NLP dependency; deferred to keep the reference stdlib-only. |

## Validation Strategy

- AC-001/002: LPs with known optima; infeasible and unbounded cases.
- AC-003: a 0/1 knapsack and a fractional-to-integer tightening.
- AC-004: a diamond network with a known min-cost max-flow; an over-capacity required flow.
- AC-005: a small DP with a known optimal value/policy under min and max.
- AC-006: run each solver twice; assert identical results.

## Rollout, Observability & Rollback

A solver library imported by optimization application specs. Nothing to roll back;
callers choose the form that fits their problem, and the explicit statuses make
failures visible.

## Open Questions

- Add conic/SOCP (chance constraints, tracking-error balls) and nonlinear/global
  forms when a dependency-free method or an optional solver dependency is chosen.
