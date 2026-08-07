# Tasks: Constrained portfolio construction from a return forecast

- **Spec:** 0007-portfolio-construction (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Returned weights are feasible (budget, box, gross) within tolerance.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `solve_portfolio` (mean-variance objective, projected gradient descent). | REQ-001, NFR-001, NFR-003 | done | `portfolio_construction` / `quadratic_programming` | Deterministic; consumes as-of alpha/cov. |
| T-002 | Implement `ConstraintSet` and `_project` (budget, box, gross cap). | REQ-002, NFR-002 | done | `problem_formulation` | Feasible by construction. |
| T-003 | Add the turnover penalty term and `turnover` helper. | REQ-003 | done | `portfolio_construction` | Penalize deviation from the prior portfolio. |
| T-004 | Implement `diagnostics` (objective, max violation, risk-aversion sensitivity). | REQ-004, NFR-002 | done | `solver_diagnostics_sensitivity` | Sensitivity curve over a gamma grid. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_portfolio_construction.py::test_risk_aversion_reduces_variance_AC_001` | done |
| AC-002 | `tests/test_portfolio_construction.py::test_constraints_satisfied_AC_002` | done |
| AC-003 | `tests/test_portfolio_construction.py::test_turnover_penalty_reduces_turnover_AC_003` | done |
| AC-004 | `tests/test_portfolio_construction.py::test_diagnostics_emitted_AC_004` | done |
| AC-005 | `tests/test_portfolio_construction.py::test_solver_reproducible_AC_005` | done |

## Follow-ups

- Calibrate `gamma` and `lambda_to` against the desk's risk budget and cost model;
  update the plan if the defaults change (tracked, not silently deferred).
- Add a long-short mandate and a robust/shrinkage covariance variant.
- Wire `0006` forecast → `0007` allocation into a combined worked example once both
  are calibrated.