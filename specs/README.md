# Specs

Each unit of work lives in its own directory here, following Spec-Driven
Development (see `instructions/spec_driven_development.md`).

```
specs/
  NNNN-short-slug/
    spec.md    # WHAT and WHY  — requirements, acceptance criteria, non-goals
    plan.md    # HOW           — architecture, data contracts, trade-offs
    tasks.md   # WORK          — ordered, traceable, testable tasks
```

- `NNNN` is a zero-padded sequence number; the slug is short kebab-case.
- Start from `templates/spec/`.
- The `spec-check` hook (`hooks/stages/spec-check.sh`) validates the chain and
  traceability across these directories.

## Index

Specs `0001`, `0006`–`0013`, `0015`, `0016`, `0018`–`0021`, and `0028` have dependency-free reference runtimes under
`src/quantsmith/pipelines/` (catalogued in
[`../src/quantsmith/pipelines/README.md`](../src/quantsmith/pipelines/README.md)),
each with a matching test module under `tests/`.

| ID | Feature | Runtime (`src/quantsmith/pipelines/`) | Tests (`tests/`) | Status |
| --- | --- | --- | --- | --- |
| [0001-daily-momentum-signal](0001-daily-momentum-signal/) | Daily cross-sectional momentum signal | `momentum_signal.py` | `test_momentum_signal.py` | Approved (reference) |
| [0002-workflow-memory](0002-workflow-memory/) | Persistent workflow memory scaffold | `memory/` scaffold | `memory` gate | Approved |
| [0004-optimizer-ml-dl-agent-expansion](0004-optimizer-ml-dl-agent-expansion/) | Optimizer, ML, and DL agent expansion | — (agent contracts) | catalog/docs gates | Approved |
| [0006-ml-return-forecasting](0006-ml-return-forecasting/) | Cross-sectional short-horizon return forecasting | `return_forecasting.py` | `test_return_forecasting.py` | Approved |
| [0007-portfolio-construction](0007-portfolio-construction/) | Constrained portfolio construction (QP) | `portfolio_construction.py` | `test_portfolio_construction.py` | Approved |
| [0008-metrics-semantic-layer](0008-metrics-semantic-layer/) | Metrics semantic layer | `metrics_semantic_layer.py` | `test_metrics_semantic_layer.py` | Approved |
| [0009-experimentation](0009-experimentation/) | Experiment (A/B test) analysis | `experimentation.py` | `test_experimentation.py` | Approved |
| [0010-analytics-pipeline](0010-analytics-pipeline/) | End-to-end analytics pipeline | `analytics_pipeline.py` | `test_analytics_pipeline.py` | Approved |
| [0011-data-pipeline-orchestration](0011-data-pipeline-orchestration/) | Data-pipeline orchestration (DAG runner) | `data_pipeline.py` | `test_data_pipeline.py` | Approved |
| [0012-execution-scheduling](0012-execution-scheduling/) | Optimal execution scheduling (Almgren-Chriss) | `execution_optimization.py` | `test_execution_optimization.py` | Approved |
| [0013-optimization-solvers](0013-optimization-solvers/) | Optimization solvers (LP/MILP/flow/DP) | `optimization_solvers.py` | `test_optimization_solvers.py` | Approved |
| [0014-data-analyst-storytelling](0014-data-analyst-storytelling/) | Data Analyst storytelling & dashboard expansion | — (agents; reuses `0010` Report) | catalog/docs gates | Approved |
| [0015-powerbi-dashboard-profile](0015-powerbi-dashboard-profile/) | Power BI dashboard profile (renders the shared dashboard spec) | `dashboard_spec.py`, `powerbi_profile.py` | `test_powerbi_profile.py` | Approved |
| [0016-excel-react-dashboard-profiles](0016-excel-react-dashboard-profiles/) | Excel and React dashboard profiles (render the shared dashboard spec) | `excel_profile.py`, `react_profile.py` | `test_excel_react_profiles.py` | Approved |
| [0017-dashboard-render-adapters](0017-dashboard-render-adapters/) | Executable render adapters — React scaffold + `.xlsx` writer | `adapters/dashboard_render/` (not `pipelines/`) | `test_dashboard_render_adapters.py` | Approved |
| [0018-remaining-dashboard-profiles](0018-remaining-dashboard-profiles/) | Streamlit/Looker/Superset/Qlik renderers + Streamlit scaffolder | `bi_profiles.py`, `adapters/dashboard_render/streamlit_scaffold.py` | `test_bi_profiles.py` | Approved |
| [0019-pipeline-observability](0019-pipeline-observability/) | Data-pipeline observability — freshness, downtime, SLA, lineage | `pipeline_observability.py` | `test_pipeline_observability.py` | Approved |
| [0020-alerting](0020-alerting/) | Alerting — policy evaluation + routing (dedup, suppress, escalate) | `alerting.py` | `test_alerting.py` | Approved |
| [0021-signal-monitoring](0021-signal-monitoring/) | Model/signal monitoring — drift, calibration, decay, regime | `signal_monitoring.py` | `test_signal_monitoring.py` | Approved |
| [0022-asset-class-mechanics-agents](0022-asset-class-mechanics-agents/) | Asset class mechanics agent expansion (equities, fixed income/rates/credit, FX, commodities, digital assets) | — (agent contracts) | catalog/docs gates | Approved |
| [0023-securities-lending-workflow](0023-securities-lending-workflow/) | Securities lending workflow — borrow classification, LP inventory optimization, concentration risk | `quantsmith/quant/agentic_quant/sec_lending_workflow.py` (not `pipelines/`) | `test_sec_lending_workflow.py` | Approved |
| [0024-role-operations-agents](0024-role-operations-agents/) | Role operations agent expansion, Phase 1 (meeting/status/scaffolding/research-scan toil, configurable, no company data) | — (agent contracts) | catalog/docs gates, `role-context` gate | Approved |
| [0025-data-provenance-guardrail](0025-data-provenance-guardrail/) | Data provenance guardrail — real-data-first priority stack + synthetic-data disclosure | — (standard/template/gate) | `data-provenance` gate | Approved |
| [0026-model-plugin-adapter](0026-model-plugin-adapter/) | Model plugin adapter — register a prebuilt internal optimization model as a reviewed, contract-bound plugin | `adapters/model_plugin/` (contract only, not `pipelines/`) | `model-plugin` gate | Approved |
| [0027-source-catalog](0027-source-catalog/) | Data source catalog — centralized, per-source registry of APIs/DBs/feeds with quality, point-in-time, and credential-pointer metadata | `sources/` (catalog only, not `pipelines/`) | `source-catalog` gate | Approved |
| [0028-financing-cost-analysis](0028-financing-cost-analysis/) | Financing cost analysis — cost-of-carry decomposition, financing-aware returns, rate-shock sensitivity, capacity | `financing_cost_analysis.py` | `test_financing_cost_analysis.py` | Approved |

`0001-daily-momentum-signal/` is a filled-in reference showing the ID scheme and
traceability end to end. Copy its structure, not its content.

### Chains & themes

- **Quant research:** `0001` signal → `0006` forecast → `0007` portfolio → `0012` execution.
- **Optimization toolkit:** `0007` (QP), `0013` (LP/MILP/flow/DP), `0012` (control), `0026` (plugin contract for prebuilt internal models).
- **Data foundations:** `0027` source catalog (registry) → `data_contract.md` (per-dataset) → `agents/data_ingestion/` (ingestion) → `data_quality`/`point_in_time` (review).
- **Data Analyst:** `0008` metrics → `0009` experimentation → `0010` end-to-end
  pipeline → `0014` storytelling & dashboards → `0015`/`0016` dashboard profiles (Power BI, Excel, React) → `0017` executable render adapters → `0018` remaining BI profiles (communication layer).
- **Data Engineer:** `0011` pipeline orchestration → `0019` pipeline observability.
- **Monitoring & alerting:** `0021` signal monitoring → `0020` alerting → `adapters/alert_delivery/`.
- **Securities financing:** `0022` asset-class mechanics (equities shorts) → `0023` securities lending workflow → `0028` financing cost analysis (`repo_financing`/`collateral_management` remain agent-contract only) → `backtest_review`/`risk`.
- **Cross-cutting:** `0002` workflow memory; `0004` agent expansion; `0022` asset-class mechanics agents (feed `trading_strategies/` and `securities_financing/`); `0024` role-operations agents (feed `research_analyst`/`implementation`, configurable via a local-only `role_context.yml`) → `0025` data-provenance guardrail (real-data-first + synthetic-data disclosure, backing `0024` and cross-referenced by `dashboard_design`/`data_storytelling`).

### Local-only specs

The evening content pack (`evening_quant_content_twitter/`) is untracked (local-only)
and carries its own `0003-evening-quant-content-workflow` and
`0005-evening-quant-content-runnable-pipeline`, validated by the `spec` gate when the
pack is present on disk.

**Next free spec number: `0029`** (`0003`/`0005` belong to the local-only pack).
