# Agent Catalog

The SDK's agents fall into three groups: the **orchestrator** that drives the
whole spec-driven flow, the **lifecycle agents** that own one SDLC stage each, and
the **domain agents** that supply quant expertise the lifecycle agents draw on.

Every agent follows the same contract: `README.md`, `prompt.md`, `instructions.md`,
`tasks.md`. See `instructions/spec_driven_development.md` for the flow and
`instructions/engineering_principles.md` for the constitution every agent upholds.

## Orchestrator

| Agent | Role |
| --- | --- |
| `workflow_orchestrator/` | Routes a change through `Specify → Plan → Tasks → Implement → Verify → Operate`, enforcing the gate between stages. Uses this catalog as its routing table. |

## Lifecycle Agents (one per SDLC stage)

| Stage | Agent | Spec artifact owned | Companion hook |
| --- | --- | --- | --- |
| 1. Planning / Requirements | `planning_requirements/` | `spec.md` | `planning-check` |
| 2. Design | `design_architecture/` | `plan.md` | `design-check` |
| 3. Coding / Implementation | `implementation/` | `tasks.md` + code | `implementation-check` |
| 4. Testing | `testing_validation/` | AC evidence | `testing-check` |
| 5. Deployment | `deployment_release/` | release record | `deployment-check` |
| 6. Maintenance | `maintenance_monitoring/` | living spec | `maintenance-check` |

Cross-cutting: the `spec-check` hook enforces the traceability chain across all
stages.

## Domain Agents (quant expertise)

| Agent | Supplies | Feeds mainly |
| --- | --- | --- |
| `research_analyst/` | Hypothesis → research plan, assumptions, go/no-go | Planning |
| `data_quality/` | Lineage, joins, timestamps, missingness, leakage review | Planning, Design |
| `feature_engineering/` | Point-in-time features, normalization-leakage review, stability | Design, Implementation |
| `modeling/` | Model selection, leakage-free validation, error analysis | Design, Testing |
| `backtest_review/` | Bias, costs, robustness, production-readiness of simulations | Testing |
| `risk/` | Exposure, concentration, drawdown, tail/stress, risk limits | Testing, Deployment |
| `git_release/` | Conventional commits, spec-traceable PRs, changelogs | Deployment |

## Ingestion Agents (`data_ingestion/`)

Grouped in the `data_ingestion/` category folder; they bring external data into a
workflow as typed, validated, reproducible datasets with a data contract.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `data_ingestion/database_connectivity/` | SQL databases & warehouses: connections, safe queries, point-in-time pulls, snapshots | Planning, Design |
| `data_ingestion/file_ingestion/` | Files (CSV, Parquet, Excel, JSON, XML, fixed-width, …): typed loading, validation | Planning, Design |
| `data_ingestion/api_ingestion/` | REST / streaming / vendor APIs: auth, pagination, retries, as-of capture | Planning, Design |

## Secrets Management Agents (`secrets_management/`)

Grouped in the `secrets_management/` category folder; they handle secret keys,
credentials, and custom key/values safely across their lifecycle, enforcing
constitution P9 (secrets never enter the repo).

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `secrets_management/secret_storage/` | Choosing/provisioning a secret store: naming, structure, access policy, encryption | Design, Deployment |
| `secrets_management/credential_access/` | Reading secrets at runtime safely: least privilege, no logging, safe caching | Implementation |
| `secrets_management/secret_rotation/` | Writing/updating/rotating and revoking credentials and custom keys | Deployment, Maintenance |
| `secrets_management/secret_scanning/` | Detecting leaked secrets in code/history/logs; remediation and prevention | Implementation, Maintenance |

## Technology & Tooling Agents (`tooling/`)

Grouped in the `tooling/` category folder; they bring the SDK's discipline to the
platforms quants work in (spreadsheets, BI/reporting, and growing to compute/data
stores).

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `tooling/excel/` | Excel models: structure, formula audit, reproducibility, model-risk, VBA safety | Implementation, Testing |
| `tooling/power_bi/` | Power BI datasets/reports: data model, DAX, refresh, RLS, performance | Implementation, Maintenance |
| `tooling/tableau/` | Tableau workbooks/data sources: LOD/table calcs, extracts, honest visuals, publishing | Implementation, Maintenance |

The planned technology matrix is maintained in
[`tooling/README.md`](tooling/README.md#planned-coverage). It prioritizes Python,
SQL, C/C++, R, Jupyter, kdb+/q, dbt, and DAG orchestration, then expands through
additional languages, BI tools, data platforms, distributed compute, production
engineering, optimization/GPU, and market connectivity.

## Planned Pipeline, Monitoring & Alerting Agents

These roadmap capabilities extend the existing data-engineering and maintenance
roles without changing the current 43-agent count:

| Capability | Planned roles | Design rule |
| --- | --- | --- |
| Pipeline building | `pipeline_builder`, `pipeline_orchestration`, `pipeline_deployment` | Emit a reviewable DAG, contracts, tests, ownership, deployment and rollback plan. |
| Monitoring | `pipeline_monitoring`, `model_signal_monitoring`, `infrastructure_cost_monitoring` | Cover data, model/signal, pipeline/service, and business/risk planes. |
| Alerting | `alerts/alert_policy`, `alerts/alert_router`, `alerts/incident_notification` | Separate detection and policy from vendor-neutral delivery adapters. |

See [`alerts/README.md`](alerts/README.md#group-workflow) for the internal alert
flow, [`../adapters/alert_delivery/README.md`](../adapters/alert_delivery/README.md)
for channel adapters, and
[`docs/handoffs/future_features.md`](../docs/handoffs/future_features.md) for
priorities and status.

## Knowledge Management Agents (`knowledge/`)

Grouped in the `knowledge/` category folder; they absorb, organize, retrieve, and
persist a company's unstructured institutional knowledge across domains — with
grounding, citations, access control, and provenance.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `knowledge/knowledge_ingestion/` | Absorbing internal sources (wiki, docs, tickets, chat, code) with provenance, access, and PII/secret/MNPI flagging | Planning, cross-cutting |
| `knowledge/knowledge_curation/` | Taxonomy, tagging, deduplication, canonical sources, conflict resolution, staleness/gap detection | Cross-cutting |
| `knowledge/knowledge_retrieval/` | Grounded, cited answers respecting the asker's access level and information barriers | Cross-cutting |
| `knowledge/institutional_memory/` | Persisting decisions, lessons, glossary, and FAQs as durable, referenceable artifacts | Maintenance, cross-cutting |

## Trading Strategy Agents (`trading_strategies/`)

Grouped in the `trading_strategies/` category folder; they operationalize the
strategy archetypes catalogued in *151 Trading Strategies* (Kakushadze & Serur) as
design-and-review roles, each with its own economic rationale, leakage, cost, and
risk concerns.

| Agent | Archetype |
| --- | --- |
| `trading_strategies/momentum_trend/` | Cross-sectional & time-series momentum, trend-following |
| `trading_strategies/mean_reversion_statarb/` | Mean reversion, pairs/stat-arb, index & ETF arbitrage |
| `trading_strategies/carry/` | Carry and roll-down (FX, rates, commodity, dividend) |
| `trading_strategies/value_factor/` | Value, quality, size, low-vol and other factor styles |
| `trading_strategies/volatility_options/` | Variance risk premium, vol arbitrage, options overlays |
| `trading_strategies/event_driven_arbitrage/` | Merger/risk arb, index rebalancing, earnings, convertibles |
| `trading_strategies/macro_multi_asset/` | Global macro, allocation, risk parity, tactical tilts |
| `trading_strategies/market_making_microstructure/` | Liquidity provision, execution alpha, order-book strategies |

## Securities Financing Agents (`securities_financing/`)

Grouped in the `securities_financing/` category folder; they make financing a
first-class part of a strategy's economics — borrow, funding, collateral, and their
costs and risks.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `securities_financing/securities_lending/` | Stock loan/borrow: locates, GC vs specials, rebate, recalls, buy-ins, corporate actions | Testing |
| `securities_financing/repo_financing/` | Repo/reverse repo funding, rates, term, haircuts, roll and counterparty risk | Testing |
| `securities_financing/collateral_management/` | Eligibility, haircuts, margin, collateral optimization, rehypothecation, regulatory impact | Deployment |
| `securities_financing/financing_cost_analysis/` | All-in cost of carry, borrow/rebate/funding netting, financing-aware backtesting | Testing |

## Formulaic Alpha Agents (`formulaic_alphas/`)

Grouped in the `formulaic_alphas/` category folder; they operationalize the
formulaic-alpha methodology of *101 Formulaic Alphas* (Kakushadze, 2016) — building
tradable signals as formulas from an operator library, combining them, and evaluating
them.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `formulaic_alphas/alpha_construction/` | Building alphas from the operator library, neutralization, point-in-time correctness | Research, Testing |
| `formulaic_alphas/alpha_combination/` | Combining alphas: correlation, spanning, weighting, diversification | Research, Testing |
| `formulaic_alphas/alpha_evaluation/` | Holding period, turnover, volatility dependence, correlation, capacity, decay | Testing |

## Analytics Pipeline Agents

A runtime multi-agent analytics/dashboard pipeline (consolidated from other
projects and normalized to the four-file contract). Each also keeps its original
`SKILL.md`. They form a chain: orchestrate → query → prep → explore → visualize →
guard → report.

| Agent | Handles |
| --- | --- |
| `orchestrator-agent/` | Routes a natural-language analytics request across the pipeline agents |
| `sql-integration-agent/` | Safe, parameterized SQL querying and schema discovery |
| `data-prep-agent/` | Cleaning, profiling, transformation, and lineage |
| `eda-specialist-agent/` | Exploratory data analysis and hypothesis generation |
| `tableau-dashboard-agent/` | Schema-validated Tableau dashboard payloads |
| `powerbi-dashboard-agent/` | Schema-validated Power BI report payloads with governance |
| `quality-guard-agent/` | Contract, schema, and policy quality gates before release |
| `reporting-agent/` | Stakeholder-ready report artifacts with provenance |

These overlap conceptually with SDK agents (`workflow_orchestrator`,
`data_ingestion/`, `tooling/`, `testing_validation`) but are a distinct runtime
pipeline; the SDK agents are design-and-review roles.

## How They Fit Together

1. The **orchestrator** determines the lifecycle position and the next gate.
2. It routes to the **lifecycle agent** that owns the current stage.
3. That agent pulls in **domain agents** for the expertise it needs.
4. The **hooks** verify the gate mechanically before the orchestrator advances.
5. The **spec** carries state between stages as the single source of truth.
6. The **adapters** connect approved payloads to providers without changing agent
   logic.

## Adding An Agent

- Create the agent directory with all four contract files (the pre-commit,
  pre-push, and CI checks require them). A public agent is any directory
  containing `prompt.md`, at any depth under `agents/`.
- Related agents may be grouped in a **category folder** (e.g.
  `agents/data_ingestion/`) with its own `README.md` describing the group; the
  category folder itself is not an agent (it has no `prompt.md`).
- Give each agent a narrow, inspectable responsibility.
- Add a `Spec-Driven Role` section to its `instructions.md`.
- Add a row to the relevant table above.