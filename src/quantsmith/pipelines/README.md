# Reference Pipelines

Runnable, dependency-free reference implementations that make specs *executable*.
Each pipeline demonstrates a spec's leakage-safe contracts so its acceptance
criteria can be tested anywhere (standard library only — no numpy, pandas, or
deep-learning runtime).

## `momentum_signal` — spec `0001-daily-momentum-signal`

The original reference, now executable: a daily cross-sectional momentum signal
(12-1 window → liquidity filter → per-date z-score) — the first link in the quant
chain (signal → forecast → portfolio → execution).

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `raw_momentum` | REQ-001 / AC-001 | 12-1 window uses only data on/before D minus the skip — no look-ahead. |
| `liquidity_filter` | REQ-003 | Names below the per-date liquidity percentile are excluded. |
| `normalize` / `build_signal` | REQ-002 / NFR-001 / AC-002, AC-003 | Per-date cross-sectional z-score; deterministic. |

Tests: `tests/test_momentum_signal.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_momentum_signal.py -q
```

## `return_forecasting` — spec `0006-ml-return-forecasting`

A cross-sectional short-horizon return forecast that routes the ML build chain with
a deep-learning challenger. It implements the spec's contracts:

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `build_labels` | REQ-001 / AC-001 | Forward excess-return labels use only returns realized strictly after the decision day. |
| `FeatureStore` | REQ-002 / AC-002 | One as-of code path for offline and online reads — parity by construction. |
| `make_folds` | REQ-003 / AC-003 | Purged + embargoed walk-forward; no train label reaches a test decision day. |
| `train_baseline` | REQ-004 | Closed-form ridge model — reference stand-in for gradient-boosted trees. |
| `train_challenger` | REQ-005 | Seeded gradient-descent model — reference stand-in for the deep temporal model. |
| `evaluate` | NFR-003 / AC-004 | Rank IC plus a net-of-cost score with turnover, on identical test rows. |
| `monitor` | REQ-006 / AC-005 | Drift, calibration, decay, and a retraining trigger with explicit thresholds. |
| `run_forecast` | — | Composes the whole walk-forward run over a price panel. |

The two model functions are deliberately simple stand-ins; a production build swaps
them for real models (gradient-boosted trees, a deep temporal network) while keeping
the surrounding labels/features/folds/evaluation/monitoring contracts intact.

Tests: `tests/test_return_forecasting.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_return_forecasting.py -q
```

## `portfolio_construction` — spec `0007-portfolio-construction`

Turns the `0006` forecast into portfolio weights by solving a constrained
mean-variance QP with projection onto the feasible set (budget, per-name box bounds,
gross-exposure cap, turnover penalty). Deterministic and dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `solve_portfolio` | REQ-001 / NFR-001 | Deterministic projected-gradient solve of the mean-variance objective. |
| `ConstraintSet` + `_project` | REQ-002 / NFR-002 / AC-002 | Weights stay feasible (budget, box, gross) by construction. |
| turnover penalty | REQ-003 / AC-003 | Rebalancing cost controlled against a prior portfolio. |
| `diagnostics` | REQ-004 / AC-004 | Objective, max constraint violation, and a risk-aversion sensitivity curve. |

The solver is a focused reference for the mean-variance form; the closed-form
frontier in `quant/mean_variance.py` remains the unconstrained counterpart.

Tests: `tests/test_portfolio_construction.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_portfolio_construction.py -q
```

## `metrics_semantic_layer` — spec `0008-metrics-semantic-layer`

A governed metrics layer for the Data Analyst workflow: each KPI is defined once and
computed consistently, so every dashboard and report returns the same number.
Deterministic and dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `SemanticLayer.register` | REQ-001 / AC-001 | One definition per metric; conflicting re-definitions rejected. |
| `SemanticLayer.compute` | REQ-002 / NFR-002 / AC-002 / AC-003 | Point-in-time period filter and declared-dimension slices that reconcile. |
| ratio metrics | REQ-003 / AC-004 | Numerator/denominator divided over the same governed rows. |
| `GovernanceError` paths | REQ-004 / AC-005 | Undefined metric, undeclared dimension, missing owner/grain fail loudly. |

Standard: `instructions/metrics_semantic_layer.md`. A production build may load
definitions from a versioned registry and connect to a warehouse; the governance
contract is unchanged.

Tests: `tests/test_metrics_semantic_layer.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_metrics_semantic_layer.py -q
```

## `experimentation` — spec `0009-experimentation`

Disciplined A/B test design and readout for the Data Analyst workflow: size before
you run, validate the allocation, and refuse to call a winner that is underpowered or
invalid. Deterministic and dependency-free (normal CDF via `math.erf`, inverse normal
via Acklam's approximation).

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `required_sample_size` | REQ-001 / AC-001 | Per-arm power analysis; grows as the MDE shrinks. |
| `analyze_proportions` | REQ-002 / NFR-002 / AC-002, AC-005 | One shared Wald SE — CI excludes 0 exactly when p < alpha. |
| `sample_ratio_mismatch` | REQ-003 / AC-003 | Detects broken allocation and invalidates the readout. |
| `analyze_experiment` | REQ-004 / NFR-003 / AC-004 | Verdict is "inconclusive" unless powered and valid (peeking guard). |

Tests: `tests/test_experimentation.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_experimentation.py -q
```

## `analytics_pipeline` — spec `0010-analytics-pipeline`

The Data Analyst capstone: runs the whole chain end to end — query → prepare →
profile → metrics → quality guard → report — and reuses the `0008` semantic layer so
the report's numbers come from one source of truth. Deterministic and dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `run_pipeline` | REQ-001 / NFR-001 | One deterministic call from source to report. |
| `run_query` + `prepare` + `profile_facts` | REQ-002 | Dedup, typing, missingness profile, and an EDA summary. |
| `SemanticLayer.compute` (from `0008`) | REQ-003 / NFR-002/003 | Metrics only through the governed layer. |
| quality guard + `QualityResult` | REQ-004 | Blocks empty results, ungoverned metrics, and failed reconciliation. |
| `Report.provenance` | REQ-005 | Source, period, row counts, and metric definition travel with the answer. |

Tests: `tests/test_analytics_pipeline.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_analytics_pipeline.py -q
```

## `data_pipeline` — spec `0011-data-pipeline-orchestration`

The first Data Engineer runtime: a deterministic DAG runner with the core
data-engineering guarantees. Dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `Pipeline` (toposort) | REQ-001 / NFR-002 / AC-001 | Dependency-ordered execution; cycles and missing deps rejected at construction. |
| `DataContract.validate` | REQ-002 / AC-002 | Each step's output is validated (columns, types, required); violations fail the step. |
| `run` (idempotent + retries) | REQ-003, REQ-004 / AC-003, AC-004 | Completed partitions skipped; bounded retries; deterministic recompute. |
| `backfill` + `RunManifest` | REQ-005 / NFR-003 / AC-005 | Only missing partitions run; per-(step, partition) status for observability. |

A production build wraps a real scheduler (Airflow/Dagster/Prefect) and a durable
state store behind the same contract.

Tests: `tests/test_data_pipeline.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_data_pipeline.py -q
```

## `signal_monitoring` + `alerting` — specs `0021` / `0020`

The monitoring→alerting chain. `signal_monitoring.monitor_signal` computes model/signal
health (drift, calibration, alpha decay, regime shift) from a reference vs live sample
and emits `Observation`s; `alerting.evaluate_policies` turns those into alerts, and
`alerting.route` deduplicates, suppresses, assigns owner/channel, and escalates.
Detection and delivery stay separate — delivery is the `adapters/alert_delivery/`
contract, with `deliver_email`/`deliver_webhook` as its first executable providers
(`0032`, `src/quantsmith/adapters/alert_delivery/`). Dependency-free and
deterministic.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `monitor_signal` → `SignalHealth` | REQ-001/002 / NFR-002 | Drift/calibration/decay/regime vs a reference; degraded on any breach. |
| `SignalHealth.observations` | REQ-003 | Measured values as observations the alerting engine evaluates. |
| `evaluate_policies` | 0020 REQ-001 / NFR-002 | A breach always fires (threshold/missing); severity + dedup key. |
| `route` | 0020 REQ-002 | Dedup + count, suppression, owner/channel, escalation. |

Tests: `tests/test_signal_monitoring.py`, `tests/test_alerting.py`.

```sh
PYTHONPATH=src python3 -m pytest tests/test_signal_monitoring.py tests/test_alerting.py -q
```

## `pipeline_observability` — spec `0019-pipeline-observability`

Reads the `RunManifest` the DAG runner (`0011`) emits and turns it into a health read:
per-step status, freshness against a watermark, data-downtime detection, an SLA verdict,
and a lineage view. Reuses `0011`; it observes, it does not re-orchestrate.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `observe` → `ObservabilityReport` | REQ-001/004 / NFR-002 | Per-step health, SLA verdict, and lineage; degraded on any breach. |
| freshness / downtime | REQ-002/003 | Stale steps (behind the watermark) and failed-partition downtime flagged. |

Tests: `tests/test_pipeline_observability.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_pipeline_observability.py -q
```

## `execution_optimization` — spec `0012-execution-scheduling`

Almgren-Chriss optimal execution: schedule a liquidation over a horizon, trading
expected cost against cost variance. Continues the quant chain (signal → forecast →
portfolio → execution). Dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `optimal_schedule` | REQ-001/002 / NFR-002 / AC-001, AC-002, AC-005 | Full-liquidation trajectory (X→0), monotone and non-negative. |
| risk-neutral / risk-averse branches | REQ-003 / AC-003 | TWAP at zero risk aversion; front-loaded when positive. |
| `expected_cost` / `cost_variance` | REQ-004 / NFR-003 / AC-004 | Both reported; risk aversion trades cost against variance. |

Tests: `tests/test_execution_optimization.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_execution_optimization.py -q
```

## `optimization_solvers` — spec `0013-optimization-solvers`

The core mathematical-programming toolkit: one deterministic solver per form, each
with an explicit status. Convex QP ships separately as `0007`. Dependency-free.

| Solver | Form / spec | Agent |
| --- | --- | --- |
| `solve_lp` | Linear programming (two-phase simplex, Bland's rule) — REQ-001/002 | `linear_programming` |
| `solve_milp` | Mixed-integer (branch-and-bound) — REQ-003 | `mixed_integer_optimization` |
| `min_cost_flow` | Min-cost (max-)flow — REQ-004 | `network_flow` |
| `solve_dp` | Finite-horizon dynamic programming — REQ-005 | `dynamic_programming` |

Infeasible and unbounded are named statuses, never a silent number. A production build
may swap in HiGHS/OR-Tools behind the same interfaces.

Tests: `tests/test_optimization_solvers.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_optimization_solvers.py -q
```

## `cardinality_portfolio` — spec `0034-cardinality-constrained-portfolio`

The first application built on the `0013` solver toolkit since `0007`/`0012`: a
cardinality constraint (hold at most K names) that `0007`'s continuous QP can't
express on its own. Composes two already-shipped solvers rather than inventing a
third — `select_cardinality_support` (`solve_milp`, `0013`) picks *which* names,
`cardinality_constrained_portfolio` sizes them via `solve_portfolio` (`0007`,
unmodified) on the reduced dimension. **A documented two-stage heuristic, not a
joint MIQP solve** — stated explicitly, not oversold. Long-only. Dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `select_cardinality_support` | REQ-001, REQ-003, REQ-004, REQ-005 | At most `max_names` names selected by linear expected-return maximization; infeasibility reported explicitly; negative `lower` raises. |
| `cardinality_constrained_portfolio` | REQ-002, REQ-003, REQ-004, REQ-005 | Reduced-dimension QP sizing with an exact zero at every unselected name; `min_weight_selected` enforced end to end. |

Tests: `tests/test_cardinality_portfolio.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_cardinality_portfolio.py -q
```

## `funding_ladder` — spec `0035-funding-ladder`

The first application built on `0013`'s `min_cost_flow`: a bipartite `SOURCE ->
tenor -> obligation -> SINK` network that matches future cash obligations to
available funding tenors (overnight, 1-week, 1-month, …) at minimum total cost. A
tenor may only fund an obligation it can actually cover — the tenor's length must
be at least the obligation's horizon — enforced by edge existence, not a post-hoc
filter. Every obligation is fully funded or the result is `"infeasible"`; never a
partial allocation presented as success. **General treasury/cash tool, not
securities-financing** — no repo, securities-lending, or collateral mechanics (that
stays agent-contract-only, routing to `model_plugin_registration`, `0026`). A
static single-snapshot decision, not a rolling re-solve. Dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `solve_funding_ladder` | REQ-001 – REQ-005 | Full funding per obligation, eligibility via edge existence, tenor capacity respected, minimum total cost, explicit infeasibility. |

Tests: `tests/test_funding_ladder.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_funding_ladder.py -q
```

## `multi_period_rebalancing` — spec `0036-multi-period-rebalancing`

The third application built on `0013`'s toolkit, and the last solver in it to get
one: a discretized single-position dynamic program on `solve_dp`. Trades off a
transaction cost (per unit traded) against a tracking-error cost (per unit away
from target) over a finite horizon, capped by a per-period `max_trade`. **A single
discretized position dimension, not a general multi-asset problem** — `solve_dp`
needs an enumerable state space, which a continuous multi-asset weight vector
isn't. Unlike `0034`/`0035`, there is no infeasible outcome: "stay put" is always a
valid action, so a well-formed problem always has a defined optimal policy.
Dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `solve_multi_period_rebalancing` | REQ-001 – REQ-004 | `max_trade` enforced by action-set construction; full position path, per-period trades, and total cost reported; cost trade-off driven by caller-supplied rates. |

Tests: `tests/test_multi_period_rebalancing.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_multi_period_rebalancing.py -q
```

## `dashboard_spec` + `powerbi_profile` — spec `0015-powerbi-dashboard-profile`

The first BI-tool renderer from the `0014` expansion track. `dashboard_spec.py` is the
tool-agnostic `DashboardSpec` contract (the output of `analytics/dashboard_design`);
`powerbi_profile.py` renders it into a Power BI payload, reusing the existing
`PowerBIPayload` and `PowerBIPayloadValidator`. Dependency-free and deterministic.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `DashboardSpec` / `Panel` | REQ-001 / NFR-003 | Governed metric per panel; chart types from a fixed vocabulary; rejects empty/ungoverned specs. |
| `render_powerbi` | REQ-002 / NFR-002 | Maps panels→visuals and metrics→measures (de-duplicated, ordered); carries dataset/page/filters. |
| reuse of `PowerBIPayloadValidator` | REQ-003/004 / NFR-001 | Validates via the existing (now repaired) Power BI contract. |

Tests: `tests/test_powerbi_profile.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_powerbi_profile.py -q
```

## `excel_profile` + `react_profile` — spec `0016-excel-react-dashboard-profiles`

Two more renderers of the shared `DashboardSpec`, on the `0015` pattern. Dependency-free
and deterministic.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `render_excel` → `ExcelWorkbookPayload` | REQ-001 | Data sheet + dashboard sheet; a chart per panel with mapped Excel chart types and governed measures. |
| `render_react` → `ReactDashboardPayload` | REQ-002 | A component per panel (mapped) with the governed metric in props and a deterministic grid layout. |
| shared `DashboardSpec` | REQ-003 / NFR-002/003 | Dataset/page/filters/order carried; governed metrics only. |

One design (`dashboard_design`), **seven render targets** — Power BI, Excel, React
(`0015`/`0016`) and Streamlit, Looker, Superset, Qlik (`0018`,
`src/quantsmith/pipelines/bi_profiles.py`) — rendered by their `tooling/` agents.
Turning a rendered payload into a **live artifact** (`.xlsx` file, scaffolded React or
Streamlit app, published report) is defined behind the adapter contract in
`adapters/dashboard_render/`; `write_xlsx`, `scaffold_react`, and `scaffold_streamlit`
are executable (`0017`/`0018`).

Tests: `tests/test_excel_react_profiles.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_excel_react_profiles.py -q
```

## `financing_cost_analysis` — spec `0028-financing-cost-analysis`

Closes out the `securities_financing` group's quant bridge. Given a book of
`FinancedPosition`s (each carrying borrow-fee, rebate, funding, and margin
legs), `decompose` computes the all-in cost of carry per leg on an explicit
ACT/360 basis; `financing_aware_returns` restates a gross return net of that
cost with the drag reported; `flag_understated_backtest` catches a backtest
that under-reports financing; `spread_sensitivity` re-decomposes under a
uniform rate shock; `capacity_limit` flags where requested short notional
exceeds availability by borrow classification (GC/WARM/HTB);
`check_point_in_time` flags a leg whose rate was "known" after its
position's period ended. `position_from_borrow_rate` reconciles with
`securities_lending`'s (`0023`) rate/classification vocabulary by value —
this module never imports that runtime's `numpy` dependency. Dependency-free
and deterministic.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `decompose` → `CostDecomposition` | REQ-001 | Per-leg cost on an explicit day-count basis; invalid inputs rejected at construction. |
| `financing_aware_returns` | REQ-002 | `net_return = gross_return - financing_cost`, with `drag` reported. |
| `flag_understated_backtest` | REQ-003 | Fires when reported cost is below the computed all-in cost beyond tolerance. |
| `spread_sensitivity` | REQ-004 | Net cost under a rate shock, monotonic, borrow leg clamped at zero. |
| `capacity_limit` → `CapacityFinding` | REQ-005 | Keyed by GC/WARM/HTB; a long position never contributes to short-borrow capacity. |
| `check_point_in_time` | NFR-001 | Flags a leg whose rate was known after its position's period end. |

Tests: `tests/test_financing_cost_analysis.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_financing_cost_analysis.py -q
```
