# QF Workflow SDK

QF Workflow SDK is an agentic workflow kit for quants, researchers, and data scientists. It is designed to organize agents, prompts, instructions, hooks, and documentation templates that make quantitative research and model development more reproducible, reviewable, and easier to hand off.

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
qf_workflow_sdk/
  README.md
  agentic_dictionary.md
  setup-hooks.sh
  .agents/
  .githooks/
  .github/
  agents/
  hooks/
  instructions/
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
- `agents/`, `hooks/`, `instructions/`, `prompts/`, `templates/`, and `examples/` are the intended public SDK surfaces.
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

## Main Concepts

- Agents define durable roles such as Research Analyst, Data Quality Reviewer, Modeling Reviewer, Backtest Reviewer, Risk Reviewer, Documentation Agent, and Git/Release Agent.
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
- `instructions/model_validation.md`
- `instructions/documentation.md`
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
- `examples/alpha_signal_handoff/`: an end-to-end example showing how the SDK artifacts connect for a hypothetical alpha signal.

## Suggested Quant Workflow

1. Start with a hypothesis and use a Research Analyst Agent to draft the research plan.
2. Use a Data Quality Agent to inspect source data, joins, timestamp alignment, coverage, and leakage risk.
3. Use a Feature Engineering or Modeling Agent to document transformations, model choices, validation design, and assumptions.
4. Use a Backtest Review Agent to inspect bias, costs, benchmarks, fragility, and robustness.
5. Use a Risk Agent to summarize exposures, concentration, drawdowns, stress behavior, and monitoring needs.
6. Use a Documentation Agent to produce a research memo, model card, dataset card, experiment summary, and handoff memo.
7. Use Git hooks and PR templates to keep changes reviewable and reproducible.

## Local Hook Setup

From inside `qf_workflow_sdk`, run:

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
- `docs/handoff.md`: continuation guide for the next implementer.
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
