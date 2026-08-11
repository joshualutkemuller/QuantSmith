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
- **131 agents** in `agents/`, indexed by the catalog `agents/README.md` (the
  live count — this file is a roadmap, not the source of truth): an
  orchestrator, six lifecycle agents (one per SDLC stage), core domain agents, and
  16 grouped categories including `optimization/`, `machine_learning/`,
  `deep_learning/`, `data_ingestion/`, `data_engineering/`, `secrets_management/`,
  `tooling/`, `knowledge/`, `trading_strategies/`, `asset_classes/`,
  `securities_financing/`, `formulaic_alphas/`, `analytics/`, `monitoring/`,
  `alerts/`, and `role_operations/`.
- **23 quality gates** in `hooks/stages/` (SDLC stages, quant gates, and repo
  gates) driven by `run-stage.sh`; advisory by default, blocking under
  `QF_STAGE_ENFORCE=1`.
- **26 instruction standards** and a prompt/template library covering specs, run
  cards, data contracts, monitoring plans, alert policies, synthetic-data
  disclosure, and postmortems.
- **`adapters/`** is a first-class SDK surface (6 groups: `alert_delivery/`,
  `schedulers/`, `artifact_delivery/`, `dashboard_render/`, `data_access/`,
  `llm_runtime/`) — the boundary between agent decisions and external systems.
  See `adapters/README.md`.
- **CI** (`.github/workflows/ci.yml`) enforces required docs, the recursive agent
  contract, shell syntax, spec traceability, backtest integrity, secret-scan,
  role-context, docs-link, agent-catalog, and spec-index; runs leakage,
  pipeline-contract, alert-contract, monitoring-coverage, and data-provenance
  advisorially/conditionally; and runs the pytest suite (`tests/`) in a separate
  job against the package's declared dependencies.
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

The original backlog (domain agents, the hook suite, CI link/contract checks,
the adoption guide, packaging, `CHANGELOG.md`, the monitoring → alerting
production spine) is now built — see `docs/handoff.md`'s "What's Next" for the
live, maintained list. What remains, as of the most recent slice
(specs `0022`–`0025`: asset-class mechanics, securities lending, role
operations, data provenance):

- Close out `agents/securities_financing/`: `repo_financing` and
  `collateral_management` remain agent-contract-only by choice;
  `financing_cost_analysis` shipped as a tested runtime (spec `0028`).
- `role_operations/` — done. Phase 2 (spec `0029`: demo packaging,
  tough-question rehearsal, experiment ledger) and Phase 3 (spec `0030`:
  model-card drafting, audit-trail keeping, governance-readiness
  checklist, a backtest pre-check, build-handoff writing, alert triage —
  sequenced last, higher stakes) both shipped; the fourteen-agent roster
  is complete.
- Optimizer *application* specs on the `0013` solver toolkit — done. Every
  solver now has a shipped application. **Cardinality-constrained portfolio
  construction** (spec `0034`, `cardinality_portfolio.py`): a two-stage
  heuristic composing `0013`'s MILP (selects at most K names) with `0007`'s
  unmodified QP (sizes them), disclosed explicitly as not a joint MIQP solve.
  **Funding ladder** (spec `0035`, `funding_ladder.py`): a bipartite
  tenor-to-obligation network on `0013`'s `min_cost_flow`, matching cash
  obligations to funding tenors at minimum cost — a general treasury/cash
  tool, explicitly not securities-financing. **Multi-period rebalancing**
  (spec `0036`, `multi_period_rebalancing.py`): a discretized single-position
  DP on `0013`'s `solve_dp`, trading transaction cost against tracking-error
  cost over a horizon — unlike `0034`/`0035` it has no "infeasible" outcome,
  since "stay put" is always a valid action. (Securities-financing LP work
  specifically is deliberately out of scope — that domain routes to an
  adopter's own models via `agents/optimization/model_plugin_registration/`,
  spec `0026`, rather than the SDK owning the optimization logic.)
- Remaining backing instructions — done: `risk_management`, `data_ingestion`
  (a shared standard replacing three duplicated copies), `reproducibility`
  (spec `0031`).
- `adapters/alert_delivery/` executable providers — done. Email and
  webhook (spec `0032`), then Slack, Teams, ticketing, PagerDuty/Opsgenie,
  and SMS/push (spec `0037`) — all seven providers now executable,
  completing the adapter's own Recommended Starting Set. Deterministic
  payload/redaction, injectable transport, no network code in the SDK;
  `pagerduty_opsgenie`/`sms_push` structurally enforce their own severity-
  routing rules, `sms_push` also enforces a short-message length cap. The
  `0032` email/webhook wrapper was factored into a shared `deliver_via`
  helper alongside the five new providers, verified behavior-preserving.
- `agents/economists/` — done (spec `0033`). Seven agents giving a
  quant/PM workflow a grounded macro backdrop (indicators → policy →
  regime → cross-asset/scenario → brief/outlook reports), reclaiming a
  stray, unwired placeholder left by the earlier parallel
  `agent/portfolio-management-agents` merge. Backed by
  `instructions/macro_economic_analysis.md`; hands off to
  `trading_strategies/macro_multi_asset`, `portfolio_management/*`, and
  `risk` rather than duplicating them.
- Risk-model worked example — done (spec `0038`, `factor_risk_model.py`).
  A standard Barra-style factor risk decomposition: variance decomposition,
  Euler risk attribution (assets and factors, sums exactly by
  construction), risk concentration (effective number of bets), and a
  linear factor-shock stress loss, explicitly not a full repricing.
  Operationalizes `instructions/risk_management.md` (`0031`) with a tested
  runtime. Remaining worked-example gap: an ingestion example that emits a
  real `data_contract.md`.
- Optional gates: `ingestion-snapshot`, a stricter notebook-output gate; revisit
  enforcing the heuristic `leakage` gate.
- Done: a plugin/adapter contract so an adopter's already-built internal
  optimization model can be registered and routed to by the `optimization/`
  agents without QuantSmith owning its implementation
  (`adapters/model_plugin/`, spec `0026`). Open follow-up: an executable
  dispatcher under `src/quantsmith/adapters/model_plugin/` once a concrete
  invocation target exists to build and test against.

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
