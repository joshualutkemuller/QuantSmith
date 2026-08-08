# Spec: Optimization solvers by mathematical form

- **ID:** 0013-optimization-solvers
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Turns the `optimization/` group's mathematical-programming agents into a working,
> tested solver library.

## Problem & Context

The `optimization/` group has 21 specialist agents but only two runtime workflows
(`0007-portfolio-construction`, a QP; `0012-execution-scheduling`, a closed-form
control). The fundamental mathematical-programming *forms* the group advertises —
linear, mixed-integer, network-flow, and dynamic programming — had no executable,
tested solver, so the group was a catalog rather than a toolkit. This spec ships a
deterministic reference solver for each of those forms, each routing its specialist
agent, so downstream specs (collateral LPs, cardinality-constrained portfolios,
funding-ladder flows, multi-period rebalancing) have a solver to build on.

## Goals

- A linear-programming solver with explicit optimal / infeasible / unbounded status.
- A mixed-integer solver (branch-and-bound) that returns integral solutions.
- A minimum-cost network-flow solver (min-cost max-flow, or a required flow).
- A finite-horizon dynamic-programming solver (backward induction).
- Deterministic behavior and honest status reporting across all four.

## Non-Goals

- Convex QP (already shipped as `0007`) and conic/SOCP, global, and nonlinear forms
  (need a cone/NLP solver; out of scope for a stdlib reference).
- Large-scale performance; these are correct reference solvers for small problems.
- Automatic model formulation (owned by the `problem_formulation` agent).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall solve a linear program (minimize/maximize, `<=` and `=` constraints, `x >= 0`) and return the optimum. | must |
| REQ-002 | The linear solver shall report infeasibility and unboundedness explicitly rather than returning a wrong number. | must |
| REQ-003 | The system shall solve a mixed-integer LP by branch-and-bound and return integral values for the integer variables. | must |
| REQ-004 | The system shall solve a minimum-cost network-flow problem (max flow at min cost, or a specified required flow) and report infeasibility. | must |
| REQ-005 | The system shall solve a finite-horizon dynamic program by backward induction, returning the optimal value and policy. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | Every solver is deterministic — the same inputs yield the same result. |
| NFR-002 | Termination | The simplex uses Bland's rule (no cycling); branch-and-bound is bounded by a node limit. |
| NFR-003 | Honest reporting | Infeasible and unbounded outcomes are named statuses, never a silent number. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given an LP with a known optimum, when solved, then the reported objective and solution match it. | REQ-001 |
| AC-002 | Given an infeasible LP or an unbounded LP, when solved, then the status is "infeasible" or "unbounded" respectively. | REQ-002, NFR-003 |
| AC-003 | Given a MILP (e.g. a 0/1 knapsack), when solved, then the integer variables are integral and the objective is optimal; a fractional LP optimum is tightened to an integer one. | REQ-003 |
| AC-004 | Given a flow network, when solved, then the min-cost max-flow value and cost match the known answer; a required flow beyond capacity is "infeasible". | REQ-004 |
| AC-005 | Given a finite-horizon DP, when solved, then the stage-0 value and the optimal policy match backward induction. | REQ-005 |
| AC-006 | Given the same inputs, when any solver runs twice, then the results are identical. | NFR-001 |

## Data & Dependencies

- Problem data supplied by the caller (cost vectors, constraint matrices, networks,
  DP transition/reward functions).
- Agents: `linear_programming`, `mixed_integer_optimization`, `network_flow`,
  `dynamic_programming`, with `problem_formulation` upstream and
  `solver_diagnostics_sensitivity` downstream.
- Convex QP is provided separately by `0007-portfolio-construction`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Simplex cycling on degenerate problems. | Non-termination. | Bland's rule for entering/leaving variables (NFR-002). |
| RISK-002 | Branch-and-bound blows up on large problems. | Runaway compute. | A node limit; documented as a small-problem reference (NFR-002). |
| RISK-003 | Infeasible/unbounded returned as a number. | Silent wrong answers. | Explicit status on every solver (NFR-003). |
| RISK-004 | Floating-point tolerance errors near constraints. | Wrong basis / integrality. | Consistent epsilon tolerances; integer rounding after branch-and-bound. |

## Assumptions & Open Questions

- Assumption: variables are non-negative in the LP/MILP standard form; free variables
  are modeled by the caller as a difference of two non-negative variables.
- Assumption: reference-scale problems; performance is not a goal.
- Open question: add conic/SOCP and nonlinear forms when a suitable dependency-free
  approach (or an optional solver dependency) is chosen (tracked, not deferred silently).

## Exceptions

None.
