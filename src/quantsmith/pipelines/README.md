# Reference Pipelines

Runnable, dependency-free reference implementations that make specs *executable*.
Each pipeline demonstrates a spec's leakage-safe contracts so its acceptance
criteria can be tested anywhere (standard library only — no numpy, pandas, or
deep-learning runtime).

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
