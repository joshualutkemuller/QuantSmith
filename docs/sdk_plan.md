# QuantSmith Plan

## Vision

QuantSmith is a practical agentic workflow kit for quants, researchers, data scientists, and portfolio teams. Its job is to turn repeated research and model-development work into reliable, inspectable workflows made from agents, hooks, instructions, prompts, templates, and validation gates.

The SDK should help a team move from idea to documented, reviewed, reproducible quant artifact with less manual coordination and fewer hidden assumptions.

## Current State

The SDK now has a working v1 built on a spec-driven engineering framework:

- **Spec-Driven Development** is the operating model: a constitution
  (`instructions/engineering_principles.md`), the SDD method
  (`instructions/spec_driven_development.md`), per-feature specs under `specs/`, and
  a worked example (`specs/0001-daily-momentum-signal/`).
- **43 agents** in `agents/`, indexed by the catalog `agents/README.md`: an
  orchestrator, six lifecycle agents (one per SDLC stage), core domain agents, and
  grouped categories — `data_ingestion/`, `secrets_management/`, `tooling/`,
  `knowledge/`, `trading_strategies/`, `securities_financing/`, `formulaic_alphas/`.
- **15 quality gates** in `hooks/stages/` (SDLC stages, quant gates, and repo
  gates) driven by `run-stage.sh`; advisory by default, blocking under
  `QF_STAGE_ENFORCE=1`.
- **13 instruction standards** and a prompt/template library covering specs, run
  cards, data contracts, monitoring plans, and postmortems.
- **CI** (`.github/workflows/ci.yml`) enforces required docs, the recursive agent
  contract, shell syntax, spec traceability, backtest integrity, secret-scan,
  docs-link, and agent-catalog; runs leakage advisory.
- Root `CLAUDE.md` activates the framework by default for any agent in the repo.
- `setup-hooks.sh` wires local Git hooks; `.githooks/` holds commit/pre-commit/pre-push.

The `hooks/` surface, once a placeholder, is now the public gate suite.

## Target Users

- Quant researchers building alpha signals, backtests, risk models, optimizers, and execution logic.
- Data scientists developing features, forecasts, experiments, and model documentation.
- Research leads who need reviewable assumptions, experiment traceability, and handoff quality.
- Platform engineers who want agentic workflow conventions without forcing every team into one monolithic tool.

## Core SDK Surfaces

### Agents

Agents should be focused role definitions that can be used by humans or automation systems. Recommended initial agents:

- Research Analyst Agent: turns a hypothesis into a research plan, assumptions, data needs, and acceptance criteria.
- Data Quality Agent: checks data contracts, missingness, survivorship risk, leakage risk, joins, and timestamp alignment.
- Feature Engineering Agent: proposes, documents, and reviews feature transformations.
- Modeling Agent: assists with model selection, validation plans, experiment tracking, and error analysis.
- Backtest Review Agent: reviews simulation assumptions, transaction costs, lookahead bias, benchmark choice, and fragility.
- Risk Agent: reviews factor exposure, concentration, drawdown, stress, and scenario behavior.
- Documentation Agent: creates model cards, research memos, dataset cards, runbooks, and decision logs.
- Git and Release Agent: keeps commits, branches, PRs, changelogs, and validation gates clean.

### Hooks

Hooks should enforce lightweight quality gates before work leaves a machine or branch:

- Commit message validation using Conventional Commits.
- Notebook output and large artifact checks.
- Python formatting and lint checks when Python code is present.
- Unit, smoke, or regression test selection based on changed files.
- Documentation freshness checks for changed models, datasets, and experiments.
- Secrets, credentials, and private data path checks.

### Instructions

Instructions should define stable behavior that agents reuse:

- Quant research review protocol.
- Backtest integrity checklist.
- Dataset and feature documentation standards.
- Model validation and monitoring standards.
- Reproducibility expectations for notebooks, scripts, configs, and outputs.
- Git, PR, and release expectations.

### Prompts

Prompts should be task-ready, composable starting points:

- Draft a research plan from a hypothesis.
- Convert notebook exploration into a reproducible script plan.
- Review a backtest for lookahead bias and overfitting risk.
- Generate a model card.
- Generate a dataset card.
- Write an experiment summary.
- Create a PR review checklist for a quant change.
- Produce a handoff memo for a model or signal.

### Templates

The SDK should include document and code templates:

- Research memo.
- Model card.
- Dataset card.
- Experiment report.
- Backtest report.
- Risk review.
- Production readiness checklist.
- Incident/postmortem template for data or model issues.

## Proposed Directory Structure

```text
quantsmith/
  README.md
  agentic_dictionary.md
  setup-hooks.sh
  agents/
    research_analyst/
    data_quality/
    feature_engineering/
    modeling/
    backtest_review/
    risk/
    documentation/
    git_release/
  hooks/
    git/
    quality/
    data/
    docs/
  instructions/
    quant_research.md
    data_quality.md
    model_validation.md
    backtesting.md
    documentation.md
    git_workflow.md
  prompts/
    research_plan.md
    dataset_card.md
    model_card.md
    backtest_review.md
    experiment_summary.md
    handoff_memo.md
  templates/
    docs/
    notebooks/
    python/
  docs/
    sdk_plan.md
    handoff.md
    architecture.md
    adoption_guide.md
```

The hidden `.agents/` folder can remain as adapter-specific or internal agent metadata, while the public `agents/` folder becomes the SDK-facing catalog.

## Development Phases

### Phase 1: Documentation and Taxonomy

- Add a top-level README that explains the SDK purpose and current state.
- Add an agentic dictionary that defines the vocabulary used across the SDK.
- Add this plan and a handoff document under `docs/`.
- Identify and document any remaining seed content that must be promoted into public SDK surfaces.

### Phase 2: Public Agent Catalog

- Create public agent folders under `agents/`.
- Give each agent a `README.md`, `prompt.md`, `instructions.md`, and `tasks.md`.
- Keep agent responsibilities narrow enough that they can be selected automatically.
- Add examples of when to invoke each agent.

### Phase 3: Quant Workflow Instructions and Prompts

- Add reusable instructions for research, data quality, modeling, backtesting, documentation, and Git workflow.
- Add prompt templates for high-frequency quant tasks.
- Add model and dataset documentation templates.
- Make every prompt specify inputs, outputs, assumptions, and validation checks.

### Phase 4: Hooks and Quality Gates

- Keep hook language aligned with quant workflow and SDK validation needs.
- Add checks for notebook output, large binary artifacts, secrets, stale docs, and changed model files.
- Make hooks degrade gracefully when optional tools are missing.
- Document local setup and bypass policy.

### Phase 5: Examples and Reference Workflows

- Add example workflows for alpha research, model documentation, backtest review, and production handoff.
- Include sample folder layouts for Python projects, notebook-heavy research, and mixed data/model repositories.
- Add one complete end-to-end example from hypothesis to handoff memo.

### Phase 6: Packaging and Adoption

- Decide whether this remains a copyable repo scaffold, a Python package, a CLI, or a hybrid.
- Add installation and upgrade guidance.
- Add versioning, changelog, and compatibility policy.
- Add contribution guidelines that reflect quant workflow review needs.

## Design Principles

- Make expert review easier, not optional.
- Prefer narrow agents with clear responsibilities over broad assistants.
- Keep every generated artifact auditable and source-linked.
- Treat data lineage, time alignment, and leakage risk as first-class concerns.
- Encourage reproducibility without blocking exploratory research.
- Use hooks as guardrails, not traps.
- Make documentation part of the workflow, not an after-the-fact chore.

## Near-Term Backlog

Much of the original backlog is now built (the domain agents, the hook suite, CI
link/contract checks). What remains:

- Write and expand `docs/adoption_guide.md` (how to install the SDK into a repo).
- Decide packaging (recorded in `docs/packaging.md`): formalize the template now,
  add a Copier-style sync CLI when update pain is real, a package only with real code.
- Add more worked examples: a risk-model or forecast spec end to end, and an
  ingestion example that emits a data contract.
- Add remaining backing instructions where a domain lacks one (e.g. risk_management,
  data_ingestion, reproducibility, monitoring).
- Add a `CHANGELOG.md` and a versioning policy once downstream repos consume the SDK.
- Optional gates: `ingestion-snapshot`, a stricter notebook-output gate; revisit
  enforcing the heuristic `leakage` gate.
- Build the production workflow spine in priority order: pipeline builder and
  deployment, pipeline/model monitoring, then channel-neutral alert policy,
  routing, and delivery adapters.
- Extend quant tooling coverage first through Python, SQL, C/C++, R, Jupyter,
  kdb+/q, dbt, and DAG orchestration; add vendors as profiles unless their review
  contract is materially different.

## Open Decisions

- Should the SDK target one primary runtime such as Python, or remain language-agnostic?
- Should notebook handling be advisory only, or enforced through hooks?
- Should agents be optimized for Codex-style local workflows, general LLM systems, or both?
- Should the SDK ship with a CLI for copying agents, prompts, hooks, and templates into downstream repos?
- What minimum documentation should be required before a model or strategy can be considered handoff-ready?

## Success Criteria

- A new quant repo can install or copy the SDK and immediately get useful agents, hooks, prompts, and documentation templates.
- A researcher can start from a hypothesis and produce a reviewed research memo, reproducible experiment summary, and handoff document.
- A reviewer can quickly see assumptions, data lineage, model choices, validation results, and known limitations.
- The SDK reduces repeated setup work without hiding important judgment calls.
