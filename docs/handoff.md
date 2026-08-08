# QuantSmith Handoff

## Snapshot

The SDK has a working v1: a **spec-driven engineering framework** over the six
software-development stages, **105 agents** including the root evening-content
workflow pack, **15 quality gates**, **13 instruction standards**, and CI that
enforces the deterministic gates. It remains primarily a scaffold to be copied
into quant repos, with `evening_quant_content_twitter/` as the first runnable local
workflow pack and `src/quantsmith/pipelines/` holding runnable, dependency-free
reference pipelines that make specs `0006` and `0007` executable and tested.

- Build-out branch: `claude/dev-stages-hooks-agents-co1sjj` (open as PR #4 into `main`).
- Root `CLAUDE.md` activates the framework by default for any agent in the repo.
- `agents/README.md` is the agent catalog and the orchestrator's routing table.

## Architecture

**Spec-Driven Development** — the spec is the source of truth; everything traces to
it via stable IDs (`REQ`/`NFR`/`AC`/`RISK`/`T`).

- `instructions/engineering_principles.md` — the constitution (P1–P10).
- `instructions/spec_driven_development.md` — flow, ID scheme, gates.
- `specs/NNNN-slug/{spec,plan,tasks}.md` from `templates/spec/`; worked example at
  `specs/0001-daily-momentum-signal/`.

**Agents (105)** — all on the four-file contract (`README`/`prompt`/`instructions`/
`tasks`) with a `Spec-Driven Role`:

- Orchestrator: `workflow_orchestrator/`.
- Lifecycle (one per stage): `planning_requirements`, `design_architecture`,
  `implementation`, `testing_validation`, `deployment_release`, `maintenance_monitoring`.
- Core domain: `research_analyst`, `data_quality`, `feature_engineering`, `modeling`,
  `backtest_review`, `risk`, `git_release`.
- Groups: `optimization/` (21), `machine_learning/` (12), `deep_learning/` (12), `data_ingestion/` (3), `secrets_management/` (4), `tooling/` (3 — Excel,
  Power BI, Tableau), `knowledge/` (4), `trading_strategies/` (8 archetypes from
  *151 Trading Strategies*), `securities_financing/` (4), `formulaic_alphas/` (3 —
  from *101 Formulaic Alphas*), and the root `evening_quant_content_twitter/`
  pack (8 content agents plus runtime/scheduler).

**Gates (15)** in `hooks/stages/`, driven by `run-stage.sh`; advisory by default,
`QF_STAGE_ENFORCE=1` blocks:

- Cross-cutting: `spec`. Per stage: `planning`, `design`, `implementation`,
  `testing`, `deployment`, `maintenance`.
- Quant/content: `leakage`, `backtest` (incl. a financing theme for shorts),
  `repro`, `data-contract`, `content-draft-pack`.
- Repo: `secret-scan`, `docs-link`, `agent-catalog`, `spec-index`, `knowledge`.

**Instructions (13)** — constitution, SDD method, point-in-time, and the domain
standards (quant_research, data_quality, backtesting, model_validation, documentation,
git_workflow, knowledge_base, trading_strategies, securities_financing, formulaic_alphas).

**Templates & prompts** — `templates/spec/`, `templates/docs/` (research memo,
dataset/model card, backtest report, run card, model monitoring plan, incident
postmortem, handoff memo, production readiness), `templates/data/data_contract.md`,
`templates/knowledge/knowledge_sources.yml`, and matching prompts.

**Configurable knowledge sources** — the knowledge agents plug into external
repositories declared in `knowledge_sources.yml` (subfolders as domains), validated
by the `knowledge` gate.

## Conventions To Preserve

- A public agent is any directory containing `prompt.md` (any depth under `agents/`)
  with all four contract files plus a `Spec-Driven Role`; group related agents in a
  category folder (its own `README.md`, no `prompt.md`). Add a catalog row.
- A domain gets a backing `instructions/*.md` standard when multiple agents/gates
  share it.
- Specs are the source of truth; assign stable IDs and keep traceability intact.
- Conventional Commits; work on the feature branch; a merged PR is finished (start
  follow-ups fresh from `main`, rebasing unmerged commits).
- Gates degrade gracefully when optional tools are missing.

## Quality Gates — Enforced vs Advisory

- **Enforced in CI:** required docs, agent contract, shell syntax, `spec`,
  `backtest`, `secret-scan`, `docs-link`, `agent-catalog`, `spec-index`, and the pytest suite
  (`tests/`, run against the package's declared dependencies).
- **Advisory:** `leakage` (heuristic by design) and the per-stage/quant gates not
  listed above. Graduate a gate to enforced per repo as discipline matures.

## What's Next (prioritized)

1. **P0 optimizer-agent workflow expansion** — the optimization group now has runtimes
   for the core mathematical forms plus two applications: convex QP
   (`specs/0007-portfolio-construction/`), a closed-form control
   (`specs/0012-execution-scheduling/`), and the solver toolkit
   (`specs/0013-optimization-solvers/`: LP, MILP, min-cost flow, dynamic programming).
   The quant chain runs signal → forecast → portfolio → execution. Next: build
   *application* specs on the new solvers — collateral/margin LP, cardinality-
   constrained portfolio (MILP), funding-ladder min-cost flow, multi-period
   rebalancing DP — and add conic/global/nonlinear forms when a dependency-free method
   or an optional solver dependency is chosen.
2. **Machine-learning and deep-learning workflow expansion** — the first runtime
   workflow is shipped as `specs/0006-ml-return-forecasting/` (ML build chain end to
   end with a DL challenger, plus a runnable reference pipeline and tests). Next: add
   more ML/DL worked examples (ranking, RL, forecasting variants) as the desk needs
   them.
3. **Data-engineering & data-analyst spec + runtime coverage** — closing the biggest
   structural gap, role by role.
   - **Data Analyst — analysis + communication layers shipped.** Governed analysis:
     `metrics_semantic_layer/` (spec `0008`), `experimentation/` (spec `0009`), and the
     end-to-end capstone `specs/0010-analytics-pipeline/` (tested runtime that reuses
     the `0008` layer). Communication layer (spec `0014-data-analyst-storytelling`):
     `data_storytelling/` (governed `Report` → narrative) and `dashboard_design/`
     (tool-agnostic dashboard spec), backed by `instructions/data_storytelling.md` —
     both **reuse** `0008`/`0009`/`0010` and hand off to `reporting-agent` and the
     tool-specific dashboard agents (no duplication). No `(planned)` nodes remain in
     the core Data Analyst or Analytics Pipeline chains. **Dashboard profiles shipped:**
     a tool-agnostic `DashboardSpec` contract plus renderers for **Power BI**
     (`specs/0015-powerbi-dashboard-profile/`), **Excel**, and **React**
     (`specs/0016-excel-react-dashboard-profiles/`), each mapping the *same* spec to a
     validated payload; `tooling/react` was added (Excel/Power BI reuse existing
     agents). **Open Data Analyst track:** the remaining BI-tool profiles (Looker,
     Qlik, Superset, Streamlit) on the same `DashboardSpec`, optional live `.xlsx`/React
     scaffolding behind the adapter contract, an optional `analytics/data_visualization`
     agent, and optional continuous-metric / sequential experiment designs.
   - **Data Engineer — first slice shipped.** The flagship node is built:
     `agents/data_engineering/pipeline_orchestration/` (a DAG runner with data
     contracts, idempotency, retries, backfill, and a run manifest), backed by
     `instructions/pipeline_engineering.md`, the worked spec
     `specs/0011-data-pipeline-orchestration/`, and a runnable, tested runtime
     (`src/quantsmith/pipelines/data_pipeline.py`). Its Data Engineer chain in
     `docs/workflows.md` no longer marks the orchestration node `(planned)`. Remaining
     Data Engineer nodes (still `(planned)`): `data_modeling`, `pipeline_observability`
     (consumes the run manifest — a natural next slice), `pipeline_builder`,
     `pipeline_deployment`, `data_governance`; plus a `pipeline-contract-check.sh` gate.
     The `src/quantsmith/agentic_code_tools/*` modules (SQL, EDA, prep, BI) remain
     runtime not tied to any spec. Backlog detail in `docs/handoffs/future_features.md`.
4. **Adoption guide** (`docs/adoption_guide.md`) — expand into a full walkthrough of
   installing the SDK into an existing quant repo.
5. **Packaging** — execute the decision in `docs/packaging.md` (template now, sync
   CLI later, package only with real code).
6. **More worked examples** — the forecast spec is done
   (`specs/0006-ml-return-forecasting/`); still open: a risk-model spec end to end
   and an ingestion example that emits a data contract (see item 3).
7. **Remaining backing instructions** — risk_management, data_ingestion,
   reproducibility, monitoring, pipeline_engineering.
8. **`CHANGELOG.md`** and a versioning policy once the SDK is consumed elsewhere.
9. **Optional gates** — `ingestion-snapshot`; a stricter notebook-output gate;
   revisit enforcing `leakage`.

## Open Questions For The Owner

- Copyable scaffold, Python package, or CLI/copier? (Directionally answered in
  `docs/packaging.md`; revisit its criteria if audience or update cadence changes.)
- Which agent runtime is the primary target (local, general LLM, both)?
- Which gates should graduate from advisory to enforced, and when?
- Should downstream repos pin a version of the SDK, and how are updates delivered?

## Risks

- Breadth: 43 agents is useful only if each stays narrow and inspectable.
- Heuristic gates (`leakage`, `backtest`, `secret-scan` fallback) can false-positive
  or miss; keep them advisory unless a repo's layout makes them reliable.
- Docs can drift from the code; the `docs-link`, `agent-catalog`, and `spec-index` gates help, but
  narrative docs (this file, `sdk_plan.md`, `agentic_dictionary.md`) need periodic
  manual refresh.
- Copied gates assume conventional artifact names; adopters must tune the patterns.

## Definition Of Done For The Next Slice

- `docs/adoption_guide.md` is complete enough that a fresh repo can install the SDK.
- The packaging decision has a chosen path with first steps taken.
- A second end-to-end worked example exists beyond the momentum signal.
