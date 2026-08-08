# Tasks: Optimal execution scheduling

- **Spec:** 0012-execution-scheduling (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- The schedule fully liquidates and is monotone/non-negative.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `optimal_schedule` (Almgren-Chriss trajectory, terminal pinning). | REQ-001, REQ-002, NFR-001, NFR-002 | done | `execution_optimization` | Holdings X→0, monotone, non-negative. |
| T-002 | Implement the risk-neutral (TWAP) limit and risk-averse front-loading. | REQ-003 | done | `execution_optimization` | Linear branch at lambda=0. |
| T-003 | Implement `expected_cost` and `cost_variance`. | REQ-004, NFR-003 | done | `solver_diagnostics_sensitivity` | Report both; the trade-off is explicit. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only reference in
`src/quantsmith/pipelines/execution_optimization.py`. A production build may add
nonlinear/transient impact and adaptive schedules; the objective (cost vs variance)
and the full-liquidation guarantee are unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_execution_optimization.py::test_schedule_shape_AC_001` | done |
| AC-002 | `tests/test_execution_optimization.py::test_full_liquidation_AC_002` | done |
| AC-003 | `tests/test_execution_optimization.py::test_twap_vs_frontloaded_AC_003` | done |
| AC-004 | `tests/test_execution_optimization.py::test_cost_variance_tradeoff_AC_004` | done |
| AC-005 | `tests/test_execution_optimization.py::test_holdings_monotone_nonneg_AC_005` | done |
| AC-006 | `tests/test_execution_optimization.py::test_deterministic_AC_006` | done |

## Follow-ups

- Extend to multi-asset joint execution and adaptive (state-dependent) schedules.
- Add nonlinear/transient impact models.
- Wire `0007` target trade → `0012` schedule into a combined execution example.