# QuantSmith

> *Build quant models the way you'd defend them — spec-driven, agentic, reproducible.*

QuantSmith is a spec-driven, agentic SDK for quant research and model development — specialist agents, quality gates, standards, and persistent memory that keep every signal and model reproducible, leakage-safe, and traceable to a spec.

The SDK is intentionally practical: it should help teams document assumptions, review data quality, reduce avoidable modeling mistakes, enforce lightweight workflow standards, and produce artifacts that another researcher or engineer can pick up later.

## Spec-Driven Development

The SDK follows a **Spec-Driven Development (SDD)** model with a strong
engineering focus: the specification is the source of truth, and every design
decision, task, test, and release traces back to it.

```
Constitution → Specify → Plan → Tasks → Implement → Verify → Operate
```

- **Constitution** — `instructions/engineering_principles.md`: the non-negotiable
  engineering rules every change is checked against.
- **Method** — `instructions/spec_driven_development.md`: the flow, the ID scheme
  (`REQ`/`NFR`/`AC`/`T`/`RISK`), and the traceability rules.
- **Artifacts** — each feature lives in `specs/NNNN-slug/` with `spec.md` (WHAT/WHY),
  `plan.md` (HOW), and `tasks.md` (traceable work). Templates are in
  `templates/spec/`; a worked example is in `specs/0001-daily-momentum-signal/`.
- **Commands** — `prompts/specify.md`, `prompts/plan.md`, `prompts/tasks.md`.
- **Gate** — `hooks/stages/spec-check.sh` enforces the chain: no plan without a
  spec, no task without a requirement, no acceptance criterion without a test, no
  orphans.

Each SDLC stage owns one spec artifact, so the six stage agents and hooks below
are the SDD flow made operational.

## What This SDK Is For

- Planning quant research from a hypothesis.
- Reviewing data lineage, joins, timestamps, missingness, and leakage risk.
- Documenting features, models, datasets, experiments, and backtests.
- Creating agent roles for common research and data-science workflows.
- Adding hooks that catch avoidable quality issues before commit or push.
- Giving teams a shared vocabulary for agentic quant workflows.

## Current Repository Shape

```text
quantsmith/
  README.md
  agentic_dictionary.md
  setup-hooks.sh
  .agents/
  .githooks/
  .github/
  agents/
  adapters/
  src/
  hooks/
  instructions/
  memory/
  prompts/
  specs/
  templates/
  examples/
  docs/
```

Current state notes:

- `.agents/` contains seed agent examples for general, Git, and design-oriented workflows.
- `.githooks/` contains seed Git hooks.
- `.github/` contains seed GitHub workflow and contribution templates.
- `agents/`, `adapters/`, `hooks/`, `instructions/`, `prompts/`, `templates/`, and `examples/` are the intended public SDK surfaces.
- `src/quantsmith/` contains executable runtime packages. Agent directories are
  role contracts and catalog entries, not long-term homes for Python modules.
- The old app-specific assets have been removed from the working tree; the remaining seed files now describe the SDK workflow.

## Public Agents

See `agents/README.md` for the full catalog (orchestrator, lifecycle, and domain
agents mapped to stages, spec artifacts, and hooks).

Orchestrator:

- `agents/workflow_orchestrator/`: drives a change through the spec-driven flow across all six stages, enforcing the gate between each. Uses the catalog as its routing table.

Ingestion agents (`agents/data_ingestion/`):

- `database_connectivity/`, `file_ingestion/`, `api_ingestion/`: bring external data in from SQL/warehouses, files (CSV, Parquet, Excel, JSON, XML, …), and APIs as typed, validated, reproducible datasets with a data contract.

Secrets management agents (`agents/secrets_management/`):

- `secret_storage/`, `credential_access/`, `secret_rotation/`, `secret_scanning/`: store, read, write/rotate, and scan for secret keys, credentials, and custom key/values — enforcing that secrets never enter the repo (constitution P9).

Technology & tooling agents (`agents/tooling/`):

- `excel/`, `power_bi/`, `tableau/`: bring reproducibility, point-in-time correctness, auditability, and secrets-safe connections to the spreadsheet and BI tools quants use. Built to grow across the quant stack (kdb+/q, MATLAB, R, Jupyter).

Knowledge management agents (`agents/knowledge/`):

- `knowledge_ingestion/`, `knowledge_curation/`, `knowledge_retrieval/`, `institutional_memory/`: absorb, organize, retrieve, and persist a company's institutional knowledge across domains — with grounded, cited answers, access control and information barriers, provenance, and durable memory of what the organization learns.

Trading strategy agents (`agents/trading_strategies/`):

- `momentum_trend/`, `mean_reversion_statarb/`, `carry/`, `value_factor/`, `volatility_options/`, `event_driven_arbitrage/`, `macro_multi_asset/`, `market_making_microstructure/`: design-and-review roles for the strategy archetypes catalogued in *151 Trading Strategies* (Kakushadze & Serur), each applying economic rationale, point-in-time/leakage, cost/capacity, and risk discipline.

Securities financing agents (`agents/securities_financing/`):

- `securities_lending/`, `repo_financing/`, `collateral_management/`, `financing_cost_analysis/`: make financing a first-class part of strategy economics — borrow cost and short rebate, repo/funding, collateral and margin — and make short/long-short backtests financing-aware.

Formulaic alpha agents (`agents/formulaic_alphas/`):

- `alpha_construction/`, `alpha_combination/`, `alpha_evaluation/`: operationalize the formulaic-alpha methodology of *101 Formulaic Alphas* (Kakushadze, 2016) — build tradable signals from an operator library (`rank`, `ts_rank`, `correlation`, `delta`, `decay_linear`, `indneutralize`, …), combine many weakly-correlated alphas, and evaluate holding period, turnover, correlation, and capacity.

Evening content workflow pack (`evening_quant_content_twitter/`):

- `content_orchestrator/`, `market_context_researcher/`, `quant_angle_generator/`, `x_post_packager/`, `visual_spec_agent/`, `meme_culture_agent/`, `claim_review_agent/`, `content_memory_agent/`: produce non-posting evening quant content draft packs with ranked ideas, posts, threads, visual specs, meme concepts, source notes, review findings, and memory updates.
- `runtime/evening_quant_pipeline.py` and `scheduler/cron.md`: run the local
  non-posting pipeline and document the 10:30 PM scheduler profile.

Analytics agents (`agents/analytics/`):

- `metrics_semantic_layer/`: the canonical metrics layer for the Data Analyst workflow — one source-of-truth definition per KPI, computed consistently and point-in-time, with governance and dimension reconciliation. (`experimentation/` planned.)

Domain agents:

- `agents/research_analyst/`: turns hypotheses into research plans, assumptions, validation gates, and handoff-ready next actions.
- `agents/data_quality/`: reviews datasets, joins, timestamps, lineage, missingness, and leakage risks.
- `agents/feature_engineering/`: documents and reviews feature transforms for point-in-time safety, normalization leakage, and stability.
- `agents/modeling/`: model selection, leakage-free validation design, error analysis, and overfitting assessment.
- `agents/backtest_review/`: reviews historical simulations for bias, execution realism, robustness, risk, and production-readiness.
- `agents/risk/`: factor exposure, concentration, drawdown, tail/stress risk, and monitorable risk limits.
- `agents/git_release/`: keeps commits, PRs, changelogs, and release records clean and traceable to the spec.

Development-lifecycle agents (one per SDLC stage):

- `agents/planning_requirements/`: Stage 1 — scopes requests into testable requirements, scope, and acceptance criteria.
- `agents/design_architecture/`: Stage 2 — turns requirements into interfaces, data flow, validation strategy, and trade-offs.
- `agents/implementation/`: Stage 3 — turns a design into reproducible, reviewable code and notebooks.
- `agents/testing_validation/`: Stage 4 — maps acceptance criteria to tests and validates model/backtest results.
- `agents/deployment_release/`: Stage 5 — production-readiness, rollout, rollback, and release handoff.
- `agents/maintenance_monitoring/`: Stage 6 — monitoring, drift/decay triage, incidents, and doc upkeep.

Each public agent follows the same contract:

- `README.md`
- `prompt.md`
- `instructions.md`
- `tasks.md`

## Public Adapters

See `adapters/README.md` for the adapter catalog. Adapters are the provider
boundary for workflows and agents: alert delivery, schedulers, artifact delivery,
data access, and LLM runtimes.

Agents decide what happened and what should be done. Adapters translate approved
payloads into provider-specific actions such as sending email, posting to Slack
or Teams, scheduling a GitHub Actions workflow, writing an artifact, querying a
warehouse, or invoking an approved model runtime.

## Main Concepts

- Agents define durable roles such as Research Analyst, Data Quality Reviewer, Modeling Reviewer, Backtest Reviewer, Risk Reviewer, Documentation Agent, and Git/Release Agent.
- Adapters define stable provider boundaries for delivery, scheduling, storage,
  data access, and model runtime calls.
- Instructions define reusable standards and behavioral rules that agents follow.
- Prompts define task-specific starting points with clear inputs and outputs.
- Hooks define local quality gates for commits, pushes, documentation, notebooks, tests, and sensitive files.
- Templates define repeatable artifacts such as research memos, dataset cards, model cards, experiment reports, and handoff memos.

See `agentic_dictionary.md` for the shared vocabulary.

## Public Instructions

- `instructions/engineering_principles.md` (the constitution)
- `instructions/spec_driven_development.md` (the SDD method)
- `instructions/point_in_time.md` (point-in-time & leakage checklist)
- `instructions/quant_research.md`
- `instructions/data_quality.md`
- `instructions/backtesting.md`
- `instructions/model_validation.md` (how to validate)
- `instructions/model_development.md` (how to build)
- `instructions/trading_strategies.md`
- `instructions/securities_financing.md`
- `instructions/formulaic_alphas.md`
- `instructions/documentation.md`
- `instructions/knowledge_base.md`
- `instructions/metrics_semantic_layer.md`
- `instructions/workflow_memory.md`
- `instructions/git_workflow.md`

## Prompt Library

Spec-driven commands:

- `prompts/specify.md` — author `spec.md`
- `prompts/plan.md` — author `plan.md`
- `prompts/tasks.md` — author `tasks.md`

Artifact prompts:

- `prompts/research_plan.md`
- `prompts/dataset_card.md`
- `prompts/data_contract.md`
- `prompts/model_card.md`
- `prompts/backtest_review.md`
- `prompts/experiment_summary.md`
- `prompts/run_card.md`
- `prompts/model_monitoring.md`
- `prompts/postmortem.md`
- `prompts/handoff_memo.md`
- `prompts/pr_review_checklist.md`

## Templates And Examples

- `templates/spec/`: spec-driven artifact templates — `spec.md`, `plan.md`, `tasks.md`.
- `templates/docs/`: research memo, dataset card, model card, backtest report, experiment summary, run card, model monitoring plan, incident postmortem, handoff memo, and production readiness checklist.
- `templates/data/`: data contract template.
- `specs/0001-daily-momentum-signal/`: a filled-in spec/plan/tasks reference showing the ID scheme and traceability end to end.
- `specs/0006-ml-return-forecasting/`: a worked ML/DL example routing the machine-learning and deep-learning agents from labeling through a monitored, net-of-cost-validated forecast.
- `specs/0007-portfolio-construction/`: a worked optimization example routing the optimization agents to turn the `0006` forecast into a constrained mean-variance portfolio.
- `specs/0008-metrics-semantic-layer/`: a worked Data Analyst example — a governed metrics layer with one canonical, point-in-time definition per KPI.
- `src/quantsmith/pipelines/`: runnable, dependency-free reference pipelines (with tests) that make specs `0006`, `0007`, and `0008` executable.
- `examples/alpha_signal_handoff/`: an end-to-end example showing how the SDK artifacts connect for a hypothetical alpha signal.

## Workflows

See `docs/workflows.md` for the workflow map — the Quant Researcher, Quant Model
Build, Data Analyst, Data Engineer, and Analytics Pipeline workflows as ordered
agent + gate chains, all on the Spec-Driven Development backbone.

## Local Hook Setup

From inside `quantsmith`, run:

```sh
./setup-hooks.sh
```

The current Git hooks are seed examples and should be updated before relying on them for production quant workflows. In particular, the current pre-commit and pre-push hooks still assume an older app layout.

### Development-Stage Hooks

`hooks/stages/` adds one advisory quality gate per SDLC stage, each paired with
its companion agent. They are advisory by default (print findings, exit `0`) and
degrade gracefully when tools or files are missing.

```sh
hooks/stages/run-stage.sh                 # run all six stage checks
hooks/stages/run-stage.sh testing         # run a single stage
```

Set `QF_STAGE_ENFORCE=1` to make findings blocking (for CI or a strict gate),
`QF_RUN_TESTS=1` to let the testing stage run the suite, and `QF_DIFF_BASE=<ref>`
to diff against a base branch. See `hooks/README.md` for wiring into Git and CI.

## Documentation

- `docs/sdk_plan.md`: roadmap and proposed SDK architecture.
- `docs/workflows.md`: the workflow map — role and scenario workflows as agent + gate chains.
- `docs/handoff.md`: continuation guide for the next implementer.
- `docs/handoffs/`: work-stream handoffs, including `future_features.md` (the build backlog).
- `evening_quant_content_twitter/`: self-contained evening quant X/Twitter workflow pack.
- `evening_quant_content_twitter/specs/0003-evening-quant-content-workflow/`: configurable evening quant content workflow spec.
- `evening_quant_content_twitter/specs/0005-evening-quant-content-runnable-pipeline/`: runnable local draft-pack pipeline spec.
- `docs/adoption_guide.md`: how to install the SDK into an existing quant repo.
- `docs/packaging.md`: packaging & distribution decision record.
- `agentic_dictionary.md`: definitions for the SDK vocabulary.

## Recommended Next Steps

- Add Feature Engineering, Modeling, Risk, Documentation, and Git/Release agents.
- Add hook scripts for notebook output, large artifacts, secrets, and stale docs.
- Add an adoption guide for installing the SDK into existing quant repositories.
- Add a lightweight CLI or copier workflow if the SDK should be installed rather than copied manually.

## Design Principles

- Make expert review easier, not optional.
- Keep agent roles narrow and inspectable.
- Surface assumptions, limitations, data lineage, and validation choices.
- Treat leakage, time alignment, survivorship bias, overfitting, and transaction costs as first-class review concerns.
- Prefer reproducible artifacts over conversational memory.
- Let exploratory work stay fast while making handoff work rigorous.
