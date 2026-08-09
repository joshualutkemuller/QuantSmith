# Plan: Securities Lending Workflow

- **Spec:** 0023-securities-lending-workflow (`spec.md`)
- **Status:** Approved
- **Author:** Claude
- **Last updated:** 2026-08-09

## Approach

Promote the existing `src/quantsmith/quant/agentic_quant/sec_lending*.py` runtime
in place: fix the greedy-fallback balance-sheet bug, add a dedicated acceptance
test module (`tests/test_sec_lending_workflow.py`), reference the runtime from the
`securities_lending` agent contract, and wire the spec index / agent catalog /
workflow map so the chain is discoverable and traceable — without moving or
rewriting the runtime's architecture.

## Architecture & Components

```text
asset_classes/equities (shorts mechanics)
  -> securities_financing/securities_lending (design/review agent)
       -> src/quantsmith/quant/agentic_quant/sec_lending_workflow.py (runtime)
            SecLendingUniverseAgent (synthetic | SQL)
              -> BorrowRateAnalysisAgent (GC/WARM/HTB, squeeze, spikes)
              -> InventoryOptimizationAgent (LP, balance-sheet + counterparty caps)
              -> SecLendingRiskAgent (concentration, HTB exposure)
              -> BorrowDemandForecastAgent (optional, heuristic)
              -> AnomalyDetectionAgent (optional, z-score)
              -> SecLendingReportAgent (report)
       -> financing_cost_analysis (all-in cost) -> backtest_review -> risk
```

## Interfaces & Data Contracts

- Blackboard keys: `sec_lending_raw` (in) -> `sec_lending_universe` ->
  `borrow_rate_analysis`, `inventory_optimization`, `sec_lending_risk`,
  `borrow_demand_forecast` (optional), `anomaly_flags` (optional) ->
  `sec_lending_report` (out, a formatted string).
- `SecLendingUniverse` dataclass: `securities: List[BorrowSecurity]`,
  `lending_book: List[LendingPosition]`,
  `counterparty_risks: List[CounterpartyRisk]`, `recall_count`,
  `total_book_balance`, `total_daily_fee`.
- `InventoryOptimizationResult`: `allocations`, `total_expected_fee`,
  `utilization_rate`, `solver_status` (`optimal` | `greedy_fallback` |
  `greedy_scipy_missing`).
- CLI: `quantsmith-sec-lending [--db PATH] [--max-book USD]
  [--max-cp-concentration FRAC] [--squeeze-threshold FRAC]
  [--lookback-days N] [--no-ml] [--combined]`.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P3 Point-in-time | n/a here | The runtime classifies a snapshot; point-in-time discipline for signals/backtests using its output remains the `securities_lending` agent's review responsibility (see its `instructions.md`). |
| P4 Correct by construction | yes | Fixes the greedy-fallback cap bug so the balance-sheet constraint holds on every solve path, not only the common one. |
| P5 Reversibility | yes | The fix is a small, isolated function change; the promotion is docs/tests plus one bug fix, on a branch. |
| P6 Observability | yes | `solver_status` on the result already reports which path executed (`optimal`/`greedy_fallback`/`greedy_scipy_missing`); tests assert on it. |
| P9 Security & data | yes | No credentials, PII, or live data introduced; synthetic/seeded data only. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `sec_lending.py` agents (unchanged logic) + `tests/test_sec_lending_workflow.py` | T-002, T-003 |
| REQ-002 | `InventoryOptimizationAgent._greedy` fix in `sec_lending.py` | T-001, T-003 |
| REQ-003 | `sec_lending_workflow.py` (`build_sec_lending_demo_pipeline`, CLI) + AC-005 test | T-003 |
| REQ-004 | `agents/README.md`, `specs/README.md`, `docs/workflows.md`, `securities_lending` agent contract | T-004 |
| NFR-001 | AC-001 determinism test | T-003 |
| NFR-002 | AC-003 balance-sheet-cap test (both solve paths) | T-001, T-003 |
| NFR-003 | Validation gates | T-005 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Runtime location | Keep in `quantsmith.quant.agentic_quant/` | Migrate to `quantsmith.pipelines/` (dependency-free style) | The runtime already depends on `numpy`/optional `scipy`/optional `sklearn` and has working CLI entry points; migrating would be a larger, riskier rewrite with no behavior change and is not what was asked. |
| Greedy-fallback bug | Fix in place (rank by fee density, fill to cap) | Leave as-is and document the limitation | An AC claiming "the cap is respected" would be false on the fallback path used whenever the optional `scipy` dependency is absent; leaving it would ship a known correctness bug under a passing test suite. |
| Test scope | Direct agent/blackboard tests plus one seeded end-to-end run | Only a full-pipeline smoke test | Direct tests pin down each agent's contract (classification, cap, risk flags) independently, so a regression in one agent doesn't hide behind the others; the end-to-end test still proves the pieces compose. |

## Validation Strategy

Run `python -m pytest tests/test_sec_lending_workflow.py tests/
test_packaging_smoke.py -q`, then `hooks/stages/run-stage.sh spec agent-catalog
docs-link spec-index`, then the full suite `python -m pytest tests/ -q`, plus
`git diff --check` for whitespace. AC-001 through AC-005 map directly to the five
tests in `tests/test_sec_lending_workflow.py` (see the Test Coverage Map in
`tasks.md`).

## Rollout, Observability & Rollback

Rollout is a branch commit (and push, if requested). Rollback is reverting the
single commit; the `_greedy` fix is a two-line, isolated change that can be
reverted independently if needed. `solver_status` already gives operational
visibility into which optimization path executed at runtime.

## Open Questions

- Should `financing_cost_analysis` (all-in cost of carry) get the same
  spec/test promotion next, closing out the `securities_financing` group's
  runtime coverage?
