# Spec: Securities Lending Workflow

- **ID:** 0023-securities-lending-workflow
- **Status:** Approved
- **Author:** Claude
- **Approver:** Josh
- **Last updated:** 2026-08-09

## Problem & Context

`agents/securities_financing/securities_lending/` is an agent contract only — a
design-and-review role with no traceable, tested runtime, unlike most other groups
in the SDK (e.g. `0006` forecasting, `0011` pipeline orchestration). A working
agentic pipeline already exists at
`src/quantsmith/quant/agentic_quant/sec_lending_workflow.py` (and its
`sec_lending.py`/`ml_agents.py` dependencies): synthetic or SQL-backed universe
construction, GC/WARM/HTB borrow-rate classification, LP-based inventory
optimization, counterparty/single-name concentration risk, optional ML demand
forecasting and anomaly detection, and report synthesis. It predates the
spec-driven pattern, has only an import smoke test
(`tests/test_packaging_smoke.py`), and is not traced to any `REQ-*`/`AC-*`.

While promoting this runtime to a proper spec, a correctness bug surfaced: the
inventory optimizer's greedy fallback path (used when the optional `scipy`
dependency is unavailable, or the LP solve fails) allocated 100% of every
security's availability regardless of the balance-sheet cap
(`max_book_size`) — the cap was silently ignored on that path. This spec fixes it
as part of making "the optimizer respects the balance-sheet cap" a true, tested
acceptance criterion.

## Goals

- Promote the existing securities-lending pipeline to a numbered spec with
  `REQ-*`/`NFR-*`/`AC-*` traceability and a dedicated test module.
- Fix the greedy-fallback balance-sheet-cap bug so the optimizer's constraint
  holds regardless of which solve path executes.
- Reference the runtime from the `securities_lending` agent contract so the
  agent and the runtime are connected (mirroring the `quant_analyst` pattern).
- Add a Role & Scenario workflow entry to `docs/workflows.md` so the chain from
  asset-class mechanics through securities financing to backtest/risk review is
  discoverable, alongside the existing `securities_financing` group workflow.

## Non-Goals

- No rewrite of the runtime into the dependency-free `src/quantsmith/pipelines/`
  style; it stays in `src/quantsmith/quant/agentic_quant/` where it already lives
  and is exercised (it depends on `numpy`, a base package dependency, and
  optionally `scipy`).
- No change to the ML demand-forecast/anomaly-detection heuristics beyond what is
  needed to test them; they remain heuristic-mode by design when `sklearn` is
  absent.
- No live SQL/vendor integration testing; the SQL path (`SQLSecLendingDataAgent`,
  `SQLiteDataSource`) is exercised only through its deterministic seeded demo.
- No change to `financing_cost_analysis`, `repo_financing`, or
  `collateral_management`; they remain agent-contract-only in this slice.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall provide a deterministic securities-lending pipeline that classifies borrow rates (GC/WARM/HTB), analyzes rate-spike and supply-squeeze signals, optimizes lending inventory under a balance-sheet cap, and evaluates counterparty/single-name concentration risk. | must |
| REQ-002 | The inventory optimizer shall respect the configured balance-sheet cap on every solve path, including the fallback used when the optional solver dependency is unavailable. | must |
| REQ-003 | The pipeline shall support synthetic (no external dependency) and SQL-backed data ingestion, runnable via a documented CLI entry point (`quantsmith-sec-lending`). | must |
| REQ-004 | The agent catalog, spec index, and workflow map shall document the runtime and its route from asset-class mechanics through securities-financing review to backtest/risk. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Determinism | The same seed produces identical classification, book balance, and fee totals across runs. |
| NFR-002 | Balance-sheet safety | Allocated notional from the inventory optimizer never exceeds `max_book_size`, on the LP path and the greedy-fallback path alike. |
| NFR-003 | Repository hygiene | `spec`, `agent-catalog`, `docs-link`, `spec-index` gates and the full pytest suite pass. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given the same seed, when the universe agent runs twice, then classification, book balance, and fee totals are identical; given a different seed, the result differs. | REQ-001, NFR-001 |
| AC-002 | Given a synthetic universe, when borrow-rate analysis runs, then securities at/above the utilization threshold appear in `squeeze_candidates` and securities at/above the rate-spike factor appear in `rate_spike_securities`, matching a direct recomputation from the universe. | REQ-001 |
| AC-003 | Given a balance-sheet cap below total available notional, when inventory optimization runs (LP path) and when the greedy fallback runs directly, then allocated notional does not exceed the cap in either case. | REQ-002, NFR-002 |
| AC-004 | Given tight concentration thresholds, when the risk agent runs, then it flags counterparty and single-name breaches; given loose thresholds on the same book, then it flags none. | REQ-001 |
| AC-005 | Given the seeded demo pipeline, when it runs end to end, then it produces a report containing the book balance, borrow classification breakdown, and a risk-flags section, with `inventory_optimization` and `sec_lending_risk` present on the blackboard. | REQ-001, REQ-003 |

## Data & Dependencies

- `numpy` (base package dependency) for the classification, analysis, and risk
  math.
- `scipy` (optional, `quant` extra) for the LP inventory solve; a greedy
  fallback (fixed by this spec, see Problem & Context) is used when absent.
- `sklearn` (optional) for ML demand forecast/anomaly detection; both agents
  operate in heuristic mode when absent (no new dependency introduced).
- No external network or live data access; the SQL path uses a local SQLite
  file or a fully synthetic in-memory seed.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | The greedy-fallback fix changes allocation output for anyone already depending on the old (buggy) all-ones behavior. | Silent behavior change for downstream callers. | The old behavior violated the documented balance-sheet constraint; fixing it is a correctness fix, not a new feature. No known caller depends on the unconstrained fallback (no prior tests covered it). |
| RISK-002 | Synthetic-data tests could mask real SQL-path bugs. | A SQL-ingestion defect ships untested. | AC-005 exercises the SQL-backed path via the deterministic seeded SQLite demo (`SQLSecLendingDataAgent` + `SQLiteDataSource.seed_demo_data`), not only the pure-synthetic path. |
| RISK-003 | The pipeline's ML forecast/anomaly agents are heuristic, not validated models; a user could mistake them for production-grade forecasts. | Overstated confidence in `borrow_demand_forecast`. | `securities_lending` agent contract and this spec's Non-Goals state the heuristic-mode design explicitly; no accuracy claim is made. |

## Assumptions & Open Questions

- Assumption: keeping the runtime in `quantsmith.quant.agentic_quant/` (rather
  than migrating it to `quantsmith.pipelines/`) is correct because it already
  depends on `numpy`/`scipy` and is exercised via CLI entry points; migrating
  would be a larger, separately-scoped refactor with no behavior change.
- Assumption: the greedy-fallback fix (rank by fee density, fill to cap) is the
  intended behavior, matching the LP objective it approximates.
- Open question: should `financing_cost_analysis` get the same runtime
  promotion next, so the securities-financing group's "all-in cost of carry"
  step is also tested?

## Exceptions

None.
