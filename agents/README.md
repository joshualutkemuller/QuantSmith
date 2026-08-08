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
| `quant_analyst/` | End-to-end quant workflow routing across research, data, modeling, financing, risk, and runtime handoff | Planning, Design, Implementation |
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
roles without changing the current 105-agent count:

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

## Evening Content Workflow Pack

The evening X/Twitter content agents moved out of the core `agents/` tree into the
root-level `evening_quant_content_twitter/` workflow pack so the whole content
surface can later be ignored locally as one folder. They still follow the same
four-file agent contract.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `evening_quant_content_twitter/agents/content/content_orchestrator/` | Config, topic budget, stage routing, ranking, draft-pack assembly, and delivery handoff | Orchestration, Reporting |
| `evening_quant_content_twitter/agents/content/market_context_researcher/` | Current context, source notes, fact/reaction/speculation separation | Research, Data Ingestion |
| `evening_quant_content_twitter/agents/content/quant_angle_generator/` | Quant-native, contrarian angles with mechanisms, scores, and risks | Research, Reporting |
| `evening_quant_content_twitter/agents/content/x_post_packager/` | Short posts, quote-tweet replies, and thread drafts under platform constraints | Reporting |
| `evening_quant_content_twitter/agents/content/visual_spec_agent/` | Chart, diagram, screenshot, and media specs with source/caveat requirements | Tooling, Reporting |
| `evening_quant_content_twitter/agents/content/meme_culture_agent/` | Market-aware meme concepts with factual and reputational risk notes | Reporting |
| `evening_quant_content_twitter/agents/content/claim_review_agent/` | Source support, labels, confidential-info review, and advice-language checks | Quality, Risk |
| `evening_quant_content_twitter/agents/content/content_memory_agent/` | Prior themes, hooks, style, visual playbook, rejected framing, and memory updates | Knowledge, Memory |

See [`../evening_quant_content_twitter/agents/content/README.md`](../evening_quant_content_twitter/agents/content/README.md#group-workflow),
[`../evening_quant_content_twitter/specs/0003-evening-quant-content-workflow/`](../evening_quant_content_twitter/specs/0003-evening-quant-content-workflow/)
and
[`../evening_quant_content_twitter/specs/0005-evening-quant-content-runnable-pipeline/`](../evening_quant_content_twitter/specs/0005-evening-quant-content-runnable-pipeline/)
for the workflow contracts.


## Optimization Agents (`optimization/`)

Grouped in the `optimization/` category folder; these agents classify constrained decision problems, choose formulation families, review solver behavior, and hand work to specs/runtime only after objectives and constraints are explicit.

| Agent | Handles |
| --- | --- |
| `optimization/optimization_orchestrator/` | Routes optimization requests across formulation, solver, domain, validation, and deployment agents. |
| `optimization/problem_formulation/` | Turns an ambiguous decision into variables, objective functions, constraints, data contracts, and acceptance criteria. |
| `optimization/linear_programming/` | LPs for allocation, blending, transportation, cash, collateral, balance-sheet, and capacity problems. |
| `optimization/quadratic_programming/` | Convex QPs for mean-variance, tracking error, turnover penalties, and regularized allocation. |
| `optimization/conic_optimization/` | SOCP/SDP-style risk, norm, robust, covariance, and chance-constraint formulations. |
| `optimization/mixed_integer_optimization/` | Binary/integer decisions, fixed charges, lot sizes, assignment, facility, and cardinality constraints. |
| `optimization/nonlinear_optimization/` | Smooth constrained nonlinear programs, gradients, scaling, local minima, and KKT diagnostics. |
| `optimization/global_optimization/` | Nonconvex search, multi-start, branch-and-bound, Bayesian optimization, evolutionary methods, and heuristics. |
| `optimization/stochastic_optimization/` | Scenario, sample-average, recourse, and simulation-backed optimization under uncertainty. |
| `optimization/robust_optimization/` | Uncertainty sets, stress-aware objectives, robust counterparts, and fragile-estimate mitigation. |
| `optimization/dynamic_programming/` | Sequential decisions, Bellman recursions, approximate DP, inventory/rebalancing policies, and control. |
| `optimization/network_flow/` | Min-cost flow, max-flow, matching, circulation, funding ladders, collateral chains, and graph routing. |
| `optimization/routing_scheduling/` | Routing, scheduling, order batching, job/crew allocation, market windows, and latency-aware placement. |
| `optimization/inventory_supply_chain/` | Replenishment, allocation, service levels, safety stock, and multi-echelon supply decisions. |
| `optimization/portfolio_construction/` | Portfolio weights, factor/risk constraints, turnover, tax lots, capacity, and rebalancing. |
| `optimization/collateral_margin_optimization/` | Eligibility, haircuts, margin, cheapest-to-deliver, substitutions, liquidity buffers, and regulation. |
| `optimization/execution_optimization/` | Trading schedules, participation, venue choice, order slicing, impact, slippage, and fill-risk trade-offs. |
| `optimization/resource_capacity_optimization/` | Compute, staffing, capital, balance-sheet, quota, cloud, API, and throughput allocation. |
| `optimization/pricing_revenue_optimization/` | Bid/ask, rebates, fee schedules, markdowns, elasticity, acceptance probabilities, and revenue risk. |
| `optimization/simulation_optimization/` | Monte Carlo, digital twins, response surfaces, and simulation-backed objective comparisons. |
| `optimization/solver_diagnostics_sensitivity/` | Solver status, infeasibility, duals, shadow prices, slacks, degeneracy, scaling, and sensitivity. |


## Machine Learning Agents (`machine_learning/`)

Grouped in the `machine_learning/` category folder; these agents cover ML framing, feature systems, predictive modeling, causal/ranking/online methods, validation, and production monitoring.

| Agent | Handles |
| --- | --- |
| `machine_learning/ml_orchestrator/` | Routes ML work from framing through features, validation, deployment, monitoring, and retraining. |
| `machine_learning/problem_framing_labeling/` | Targets, labels, horizons, decision times, leakage boundaries, class balance, and label quality. |
| `machine_learning/feature_store_engineering/` | Reusable features, point-in-time joins, entity keys, offline/online parity, and provenance. |
| `machine_learning/supervised_learning/` | Regression/classification, baselines, calibration, imbalance, metric choice, and segment errors. |
| `machine_learning/time_series_forecasting/` | Forecasting, temporal validation, hierarchical series, exogenous drivers, revisions, and reconciliation. |
| `machine_learning/ranking_recommendation/` | Ranking, recommendation, candidate generation, retrieval, learning-to-rank, and evaluation at rank. |
| `machine_learning/causal_uplift/` | Treatment effects, uplift, experiments, observational bias, instruments, diff-in-diff, and identification. |
| `machine_learning/unsupervised_anomaly/` | Clustering, dimensionality reduction, outliers, novelty detection, drift probes, and alert quality. |
| `machine_learning/model_selection_validation/` | Baselines, validation design, hyperparameter search, leakage controls, robustness, and error analysis. |
| `machine_learning/automl_experimentation/` | Broad searches, experiment tracking, multiple-testing control, reproducibility, and search-space discipline. |
| `machine_learning/online_learning_bandits/` | Contextual bandits, exploration/exploitation, delayed feedback, guardrails, regret, and online updates. |
| `machine_learning/mlops_monitoring/` | Packaging, serving, drift, calibration, retraining triggers, run cards, and production ownership. |


## Deep Learning Agents (`deep_learning/`)

Grouped in the `deep_learning/` category folder; these agents cover neural architectures, training systems, modality specialists, reinforcement learning, generative models, and serving constraints.

| Agent | Handles |
| --- | --- |
| `deep_learning/dl_orchestrator/` | Routes DL work across architecture, data, training, evaluation, compression, serving, and monitoring. |
| `deep_learning/training_systems/` | Data loaders, distributed training, mixed precision, checkpointing, determinism, accelerators, and cost. |
| `deep_learning/neural_tabular/` | Tabular neural nets, embeddings, categorical features, calibration, baselines, and tree-model trade-offs. |
| `deep_learning/sequence_transformers/` | Temporal, transformer, attention, and sequence models for markets, logs, language, and streams. |
| `deep_learning/graph_neural_networks/` | GNNs for networks, collateral chains, counterparties, supply graphs, ownership graphs, and message passing. |
| `deep_learning/reinforcement_learning/` | MDP framing, reward design, simulators, offline RL, policy constraints, safety, and evaluation. |
| `deep_learning/computer_vision/` | Image, document, screenshot, and visual workflows, including augmentation, labeling, and quality checks. |
| `deep_learning/nlp_llm/` | Text classification, retrieval, embeddings, reranking, prompt/eval design, RAG boundaries, and LLM controls. |
| `deep_learning/representation_metric_learning/` | Embeddings, contrastive learning, similarity search, clustering, and representation evaluation. |
| `deep_learning/generative_models/` | Diffusion, VAEs, GANs, synthetic data, scenario generation, augmentation, and privacy/risk limits. |
| `deep_learning/deep_time_series/` | Deep forecasting, temporal fusion, sequence-to-sequence, regime conditioning, and probabilistic forecasts. |
| `deep_learning/compression_serving/` | Distillation, quantization, pruning, batching, latency, memory, GPU utilization, and serving contracts. |
| `deep_learning/deep_portfolio_optimization/` | Direct neural allocation, differentiable portfolio objectives, allocation constraints, baselines, and validation. |
| `deep_learning/portfolio_volatility_costs/` | Volatility scaling, turnover, transaction costs, leverage, after-cost robustness, and implementation frictions. |
| `deep_learning/portfolio_stress_explainability/` | Stress-window allocation behavior, feature attribution, regime explanations, and monitoring hooks. |

## Git Workflow Agent (`git/`)

| Agent | Handles |
| --- | --- |
| `git/` | Branch hygiene, Conventional Commits, hooks, CI guidance, and GitHub workflow support. |

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

## Analytics Agents (`analytics/`)

Specialist roles that make **Data Analyst** work consistent (see
[`analytics/README.md`](analytics/README.md)). They sit mid-chain between EDA and the
dashboard/reporting agents.

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `analytics/metrics_semantic_layer/` | Canonical KPI definitions — one source of truth, point-in-time computation, declared dimensions, ratio metrics | Reporting, Dashboards, Testing |

Planned: `analytics/experimentation/` (A/B testing, power analysis, causal caveats).
Runtime: `src/quantsmith/pipelines/metrics_semantic_layer.py`; spec:
`specs/0008-metrics-semantic-layer/`; standard: `instructions/metrics_semantic_layer.md`.

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
7. Runtime Python belongs under `src/quantsmith/`; agent directories describe
   roles, prompts, instructions, and tasks.

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
