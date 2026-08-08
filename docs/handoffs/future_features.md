# Future Features

The running backlog of features to build. Add new ideas as rows; promote one to a
full `specs/NNNN-slug/` when work starts (see `docs/handoffs/README.md`).

**Status:** `proposed` → `in-progress` → `done`.
**Priority:** P0 (highest) · P1 (high) · P2 (medium) · P3 (nice-to-have).

## Agents

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `agents/optimization/*`, `agents/machine_learning/*`, `agents/deep_learning/*` | Highest-priority optimizer-agent expansion plus ML/DL specialist surfaces for stringing finance, operations, and technology workflows into specs and runtime handoffs. First runtime workflows shipped: `specs/0006-ml-return-forecasting/` (ML/DL) and `specs/0007-portfolio-construction/` (optimization), both with runnable reference pipelines and tests. Remaining: more runtime workflows across operations/technology optimization and additional ML/DL examples | P0 | in-progress |
| `agents/data_engineering/data_modeling/` | Dimensional/warehouse modeling: star/snowflake schemas, slowly-changing dimensions, grain | P1 | proposed |
| `agents/data_engineering/pipeline_orchestration/` | dbt-style models, DAGs, scheduling, incremental loads, backfills, idempotency. Shipped: agent + `instructions/pipeline_engineering.md` + spec `specs/0011-data-pipeline-orchestration/` + tested runtime `src/quantsmith/pipelines/data_pipeline.py` (DAG, contracts, idempotency, retries, backfill, run manifest) | P1 | done |
| `agents/data_engineering/pipeline_observability/` | Data freshness, SLAs, lineage, data-downtime detection | P2 | proposed |
| `agents/data_engineering/data_governance/` | Catalog, lineage, access policy, ownership | P3 | proposed |
| `agents/data_engineering/pipeline_builder/` | Compile a source/transform/sink intent into a reviewable DAG, data contracts, schedules, retries, backfills, tests, ownership, and deployment plan | P1 | proposed |
| `agents/data_engineering/pipeline_deployment/` | Environment promotion, dry runs, canaries, rollback, state migration, and scheduler-specific deployment adapters | P1 | proposed |
| `agents/analytics/metrics_semantic_layer/` | Canonical KPI/metric definitions (semantic layer) — the biggest data-analyst consistency win. Shipped: agent + `instructions/metrics_semantic_layer.md` + spec `specs/0008-metrics-semantic-layer/` + tested runtime `src/quantsmith/pipelines/metrics_semantic_layer.py` | P1 | done |
| `agents/analytics/experimentation/` | A/B testing, power analysis, causal caveats. Shipped: agent + spec `specs/0009-experimentation/` + tested runtime `src/quantsmith/pipelines/experimentation.py` (power/sample-size, SRM guard, p-value/CI consistency, power-gated verdict). Follow-ups: continuous-metric (t-test), sequential/Bayesian, CUPED | P2 | done |
| `agents/analytics/data_storytelling/` + `dashboard_design/` | Data Analyst communication layer — narrative (situation → insight → action) and tool-agnostic dashboard spec. Shipped: two agents + `instructions/data_storytelling.md` + spec `specs/0014-data-analyst-storytelling/`; reuse `0008`/`0009`/`0010`, hand off to `reporting-agent` and tool dashboard agents | P1 | done |
| BI-tool profiles: `tooling/looker`, `tooling/qlik`, `tooling/superset`, `tooling/streamlit_dash` | Thin profiles that render the shared dashboard spec from `dashboard_design`. Shipped so far: Power BI (`specs/0015-powerbi-dashboard-profile/`), Excel and React (`specs/0016-excel-react-dashboard-profiles/`, added `tooling/react`). These four follow the same `render_<tool>(DashboardSpec)` pattern | P2 | in-progress |
| `agents/analytics/data_visualization/` | Single-chart encoding/color/accessibility, split from `dashboard_design` if it grows too broad (spec `0014` track) | P3 | proposed |
| `agents/alerts/alert_policy/` | Threshold, anomaly, composite, and missing-event policies with severity, suppression, cooldown, and market-calendar rules | P1 | proposed |
| `agents/alerts/alert_router/` | Ownership, deduplication, grouping, rate limits, escalation, and channel selection | P1 | proposed |
| `agents/alerts/incident_notification/` | Actionable notifications, acknowledgement/recovery lifecycle, evidence and runbook links | P1 | proposed |
| Provider implementations for `adapters/alert_delivery/` | Executable email, Slack, Teams, PagerDuty/Opsgenie, SMS/push, webhook, Jira/ServiceNow/Linear integrations behind the adapter contract | P1 | proposed |
| `agents/monitoring/pipeline_monitoring/` | DAG status, dependencies, freshness, latency, backlogs, retries, partial writes, idempotency, and SLOs | P1 | proposed |
| `agents/monitoring/model_signal_monitoring/` | Quality, calibration, feature drift, alpha decay, turnover/capacity, and regime change | P1 | proposed |
| `agents/monitoring/infrastructure_cost_monitoring/` | Compute, memory, storage, API quota, market-data spend, and cost-per-run guardrails | P2 | proposed |
| `evening_quant_content_twitter/` evening content workflow pack | Configurable 10:30 PM ET quant content workflow that produces ranked X/Twitter ideas, threads, visual specs, meme concepts, source notes, claim review, local draft artifacts, and a cron profile without automatic posting; see `evening_quant_content_twitter/docs/handoff.md`, `evening_quant_content_twitter/specs/0003-evening-quant-content-workflow/`, and `evening_quant_content_twitter/specs/0005-evening-quant-content-runnable-pipeline/` | P1 | done |
| Normalize `agents/quant_analyst/` | Keep `agents/quant_analyst/` as a four-file agent contract and promote runtime Python into `src/quantsmith/` | P2 | shipped |

## Technology & Tooling

Tooling agents are grouped by distinct risk and review contracts. Vendor variants
belong under profiles/adapters unless they require materially different behavior.

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `agents/tooling/python/` | Packaging, typing, vectorization, numerical stability, testing, environments, profiling | P1 | proposed |
| `agents/tooling/sql/` | Dialect-aware query design, temporal joins, plans, parameterization, transactions, warehouse cost | P1 | proposed |
| `agents/tooling/cpp/` | C/C++ numerical correctness, memory/undefined behavior, concurrency, profiling, Python bindings | P1 | proposed |
| `agents/tooling/r/` | Reproducible environments, statistical workflows, packages, testing, R/Python interoperability | P1 | proposed |
| `agents/tooling/jupyter/` | Execution order, hidden state, parameterized runs, environment capture, notebook graduation | P1 | proposed |
| `agents/tooling/kdb_q/` | Tick/time-series storage, temporal joins, partitioning, symbology, query performance | P1 | proposed |
| `agents/tooling/dbt/` | Model contracts, tests, incremental models, snapshots, lineage, semantic definitions | P1 | proposed |
| `agents/tooling/dag_orchestration/` | Airflow/Dagster/Prefect/cloud scheduler profiles; DAGs, retries, backfills, idempotency | P1 | proposed |
| `agents/tooling/julia/`, `matlab/`, `java_jvm/`, `dotnet_csharp/` | Additional research, numerical, and enterprise-runtime coverage | P2 | proposed |
| `agents/tooling/looker/`, `qlik/`, `superset/`, `streamlit_dash/` | Remaining common governed BI and Python-native analytics surfaces | P2 | proposed |
| `agents/tooling/warehouse_lakehouse/` | Snowflake, Databricks, BigQuery, Redshift profiles with PIT, partition, cost, and governance review | P1 | proposed |
| `agents/tooling/columnar_data/` | Parquet/Arrow/Polars/DuckDB profiles; schema, partitioning, lazy execution, interoperability | P2 | proposed |
| `agents/tooling/spark/`, `ray_dask/` | Distributed compute plans, skew/shuffle diagnostics, determinism, memory and cost | P2 | proposed |
| `agents/tooling/git_ci/`, `containers/`, `cloud_quant_platform/` | CI/CD, containers/Kubernetes, and AWS/Azure/GCP deployment profiles | P2 | proposed |
| `agents/tooling/optimization_solvers/`, `gpu_compute/` | Solver diagnostics and accelerated numerical-compute rigor | P2 | proposed |
| `agents/tooling/market_data_execution/` | FIX/vendor feeds, timestamps, calendars, throttling, replay, order safety, audit | P1 | proposed |

## Instructions (backing standards)

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `instructions/risk_management.md` | Standard behind the `risk` agent (exposure, tail, limits) | P2 | proposed |
| `instructions/data_ingestion.md` | Standard behind `data_ingestion/*` (PIT capture, snapshots, schema validation) | P2 | proposed |
| `instructions/reproducibility.md` | Operationalize P4 for the `repro` gate and run card | P2 | proposed |
| `instructions/monitoring.md` | Standard behind `maintenance_monitoring` and the monitoring plan | P3 | proposed |
| `instructions/pipeline_engineering.md` | DAG, idempotency, retry/backfill, environment, data-contract, lineage, and deployment standard | P1 | proposed |
| `instructions/alerting.md` | Channel-neutral alert schema, severity, routing, suppression, acknowledgement, escalation, and privacy | P1 | proposed |

## Gates

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `hooks/stages/ingestion-snapshot-check.sh` | Verify ingestion captures a snapshot/checksum | P3 | proposed |
| `hooks/stages/pipeline-contract-check.sh` | Verify DAG ownership, inputs/outputs, schedule, retry/backfill, idempotency, and runbook metadata | P2 | proposed |
| `hooks/stages/alert-contract-check.sh` | Verify event schema, owner, severity, deduplication, runbook, redaction, and test route | P2 | proposed |
| `hooks/stages/monitoring-coverage-check.sh` | Verify each production risk has a metric, threshold/baseline, owner, alert, runbook, and review cadence | P2 | proposed |
| Stricter notebook-output gate | Beyond the current `implementation` check | P3 | proposed |
| Enforce `leakage` in CI | Currently advisory (heuristic); revisit once patterns are tuned | P3 | proposed |

## Docs & Packaging

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| Expand `docs/adoption_guide.md` | Full walkthrough with per-project-type recipes | P1 | proposed |
| Copier-style sync CLI | Selective install + update per `docs/packaging.md` | P2 | proposed |
| More worked examples | Forecast spec shipped (`specs/0006-ml-return-forecasting/`); still open: a risk-model spec end to end and an ingestion example that emits a data contract | P2 | in-progress |
| `CHANGELOG.md` + versioning policy | Once the SDK is consumed by other repos | P2 | proposed |
| Visual workflow diagram | A rendered diagram of `docs/workflows.md` | P3 | proposed |

## Recently Shipped (for reference)

- **Data Analyst role complete**: `analytics/metrics_semantic_layer` (spec `0008`),
  `analytics/experimentation` (spec `0009`), and the end-to-end capstone
  `specs/0010-analytics-pipeline/` — all with dependency-free, tested reference
  runtimes under `src/quantsmith/pipelines/`.
- ML/DL and optimization runtime workflows: `specs/0006-ml-return-forecasting/`,
  `specs/0007-portfolio-construction/` (QP), `specs/0012-execution-scheduling/`
  (Almgren-Chriss), and `specs/0013-optimization-solvers/` (LP, MILP, min-cost flow,
  dynamic programming), with tested reference pipelines. The quant chain runs
  signal → forecast → portfolio → execution.
- Data Engineer first slice: `specs/0011-data-pipeline-orchestration/` — a DAG runner
  with contracts, idempotency, retries, backfill, and a run manifest.
- Adapter catalog contracts (`adapters/`) for alert delivery, schedulers, artifact
  delivery, data access, and LLM runtimes.
- Persistent workflow memory (`memory/`, `instructions/workflow_memory.md`,
  `memory-check` gate) — spec `specs/0002-workflow-memory/`.
- Model-development standard (`instructions/model_development.md`) and the
  consolidated workflow map (`docs/workflows.md`).
- Securities financing, formulaic alphas, trading strategies, tooling, knowledge,
  and secrets agent groups.
- The consolidation pass (refreshed `sdk_plan`, `handoff`, `agentic_dictionary`;
  added the adoption guide).
