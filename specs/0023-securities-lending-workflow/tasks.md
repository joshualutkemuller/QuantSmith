# Tasks: Securities Lending Workflow

- **Spec:** 0023-securities-lending-workflow (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-09

## Definition of Done (applies to every task)

- Every `AC-*` has a passing, named test in `tests/test_sec_lending_workflow.py`.
- The runtime stays dependency-honest: `numpy` required (already a base
  dependency), `scipy`/`sklearn` remain optional with graceful fallback.
- No secrets, credentials, or live data; synthetic/seeded data only.
- Docs and catalogs updated alongside the promotion.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Fix the inventory optimizer's greedy-fallback balance-sheet-cap bug. | REQ-002, NFR-002 | done | `InventoryOptimizationAgent._greedy` now ranks by fee density and fills to `max_book`, in `src/quantsmith/quant/agentic_quant/sec_lending.py`. |
| T-002 | Confirm the existing runtime's behavior (classification, analysis, risk) matches the spec's requirements. | REQ-001 | done | Verified directly against `sec_lending.py`/`sec_lending_workflow.py`; no logic changes needed beyond T-001. |
| T-003 | Add the acceptance test module. | REQ-001, REQ-002, REQ-003, NFR-001, NFR-002 | done | `tests/test_sec_lending_workflow.py`, 5 tests (AC-001..005). |
| T-004 | Wire the spec into catalogs, the agent contract, and the workflow map. | REQ-004 | done | `agents/securities_financing/securities_lending/{README,instructions}.md`, `agents/README.md`, `specs/README.md`, `docs/workflows.md`. |
| T-005 | Run validation gates. | NFR-003 | done | `spec`, `agent-catalog`, `docs-link`, `spec-index`; full `pytest tests/ -q`; `git diff --check`. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `test_universe_construction_is_deterministic_AC_001` | done |
| AC-002 | `test_borrow_rate_analysis_flags_squeeze_and_spikes_AC_002` | done |
| AC-003 | `test_inventory_optimization_respects_balance_sheet_cap_AC_003` | done |
| AC-004 | `test_risk_agent_flags_concentration_breaches_AC_004` | done |
| AC-005 | `test_demo_pipeline_runs_end_to_end_AC_005` | done |

## Follow-ups

- Promote `financing_cost_analysis` (all-in cost of carry, financing-aware
  backtesting) to a tested runtime under a future spec, closing out the
  `securities_financing` group's remaining agent-contract-only members
  (`repo_financing`, `collateral_management`).
- Consider a `sklearn`-backed (non-heuristic) variant of
  `BorrowDemandForecastAgent` if a concrete workflow needs calibrated demand
  forecasts rather than a rate/utilization heuristic.
