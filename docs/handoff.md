# QuantSmith Handoff

## Snapshot

The SDK has a working v1: a **spec-driven engineering framework** over the six
software-development stages, **131 agents** including the root evening-content
workflow pack, **23 quality gates**, **26 instruction standards**, and CI that
enforces the deterministic gates. It remains primarily a scaffold to be copied
into quant repos, with `evening_quant_content_twitter/` as the first runnable local
workflow pack, `src/quantsmith/pipelines/` holding runnable, dependency-free
reference pipelines for most specs (see `specs/README.md`'s index for the current
list), and `src/quantsmith/quant/agentic_quant/` holding a further runtime (spec
`0023`) with `numpy`/optional-`scipy` dependencies. `adapters/` is a first-class
SDK surface (6 groups) — the provider boundary between agent decisions and
external systems (delivery, scheduling, storage, data access, model runtimes).

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

**Agents (131, verified by the `agent-catalog` gate — treat `agents/README.md`
as the live count, not the number here)** — all on the four-file contract
(`README`/`prompt`/`instructions`/`tasks`) with a `Spec-Driven Role`:

- Orchestrator: `workflow_orchestrator/`.
- Lifecycle (one per stage): `planning_requirements`, `design_architecture`,
  `implementation`, `testing_validation`, `deployment_release`, `maintenance_monitoring`.
- Core domain: `research_analyst`, `data_quality`, `feature_engineering`, `modeling`,
  `backtest_review`, `risk`, `git_release`.
- Groups (largest first): `optimization/`, `deep_learning/`, `machine_learning/`,
  `tooling/`, `data_engineering/`, `trading_strategies/`, `asset_classes/`,
  `secrets_management/`, `securities_financing/`, `knowledge/`, `analytics/`,
  `role_operations/`, `monitoring/`, `alerts/`, `data_ingestion/`,
  `formulaic_alphas/` — see `agents/README.md` for per-group membership and
  counts, which change more often than this file is refreshed.
- Plus the root `evening_quant_content_twitter/` pack (local-only, untracked;
  content agents plus runtime/scheduler).

**Gates (23)** in `hooks/stages/`, driven by `run-stage.sh`; advisory by default,
`QF_STAGE_ENFORCE=1` blocks:

- Cross-cutting: `spec`. Per stage: `planning`, `design`, `implementation`,
  `testing`, `deployment`, `maintenance`.
- Quant/content: `leakage`, `backtest` (incl. a financing theme for shorts),
  `repro`, `data-contract`, `pipeline-contract`, `alert-contract`,
  `monitoring-coverage`, `content-draft-pack`, `data-provenance`.
- Repo: `secret-scan`, `docs-link`, `agent-catalog`, `spec-index`, `knowledge`, `role-context`.

**Instructions (26)** — constitution, SDD method, point-in-time, and the domain
standards; see `README.md`'s "Public Instructions" table for the current list
(this file lists categories, not every filename, to avoid drifting again).

**Templates & prompts** — `templates/spec/`, `templates/docs/` (research memo,
dataset/model card, backtest report, run card, model monitoring plan, incident
postmortem, handoff memo, production readiness, decision log),
`templates/data/data_contract.md`, `templates/knowledge/knowledge_sources.yml`,
and matching prompts.

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
  `backtest`, `secret-scan`, `role-context`, `docs-link`, `agent-catalog`, `spec-index`, and the pytest suite
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
     agents). Live artifact generation is shipped: the `adapters/dashboard_render/` contract
     plus **executable providers** (specs `0017`/`0018`) — `scaffold_react`,
     `write_xlsx` (openpyxl, lazy), and `scaffold_streamlit`, all dry-run-capable with a
     checksum manifest and a no-secrets guard. **Dashboard track complete:** the shared
     `DashboardSpec` now renders to **seven targets** — Power BI, Excel, React
     (`0015`/`0016`) and Streamlit, Looker, Superset, Qlik (`0018`) — each with a
     `tooling/` agent. **Open Data Analyst track:** executable emitters for
     Looker/Superset/Qlik and a `powerbi_publish` provider (payload/agents exist), an
     optional `analytics/data_visualization` agent, and optional continuous-metric /
     sequential experiment designs.
   - **Data Engineer — group fully staffed; two runtime nodes.** The
     `agents/data_engineering/` group now has all six agents: `pipeline_orchestration`
     (DAG runner — spec `0011`, tested runtime) and `pipeline_observability` (freshness/
     downtime/SLA/lineage from the run manifest — spec `0019`, tested runtime), plus
     `data_modeling`, `pipeline_builder`, `pipeline_deployment`, and `data_governance`
     as design/review agents. The Data Engineer chain in `docs/workflows.md` has no
     remaining `(planned)` nodes. Backed by `instructions/pipeline_engineering.md`.
     Follow-ups closed: the **`pipeline-contract-check.sh` gate** (validates a pipeline
     manifest against `templates/data/pipeline_manifest.md`; enforced in CI, skips when
     absent) and **per-step SLA thresholds** in `observe` (`0019`). The four
     design/review nodes (`data_modeling`, `pipeline_builder`, `pipeline_deployment`,
     `data_governance`) get executable runtimes only when a concrete workflow needs
     one. The `src/quantsmith/agentic_code_tools/*` modules (SQL, EDA, prep, BI) remain
     runtime not tied to any spec. Backlog detail in `docs/handoffs/future_features.md`.
4. **Role-operations agent roster (Data Science Lead efficiency plan) — done.**
   All three phases of a 14-agent roster shipped, absorbing a
   quant/data-science lead's operational toil so more time goes to model
   scoping and research. Full roster and rationale: the role-efficiency
   plan this initiative implements (see `agents/role_operations/README.md`
   for the phase breakdown carried in-repo). Backlog detail also tracked
   in `docs/handoffs/future_features.md`.
   - **Phase 1 — done** (spec `0024`): `meeting_to_action`, `status_rollup`,
     `rapid_scaffolder`, `prior_art_scanner` — the lowest-risk,
     highest-frequency slice, deliberately built and used first so trust
     forms before any agent touches a client or governance committee.
     Configurable via a local-only `role_context.yml`, gitignored by
     default and enforced by the `role-context` gate — this repository
     carries no company-specific or personal data. Backed by
     `instructions/role_operations.md`.
   - **Data-provenance guardrail — done** (spec `0025`, prompted directly
     by this initiative's own guardrails): real-data-first priority stack
     and complete synthetic-data disclosure, wired into `rapid_scaffolder`
     specifically since it's the agent most likely to reach for synthetic
     data to make a scaffold runnable.
   - **Phase 2 — done** (spec `0029`): `demo_narrative_packager`,
     `tough_question_rehearsal`, `experiment_ledger` — prototype
     accelerators. `demo_narrative_packager` disclosed synthetic data per
     `instructions/data_provenance.md`; `tough_question_rehearsal` reads
     `role_context.yml`'s stakeholder personas; `experiment_ledger` runs
     alongside `rapid_scaffolder`'s iteration loop.
   - **Phase 3 — done** (spec `0030`): `model_card_drafter`,
     `audit_trail_keeper`, `governance_readiness_checklist`,
     `second_look_backtest_reviewer`, `build_handoff_writer`,
     `alert_triage` — governance-adjacent, deliberately sequenced last
     given the higher stakes. Added `templates/docs/decision_log.md` (no
     template existed yet for `agentic_dictionary.md`'s Decision Log
     term). `second_look_backtest_reviewer` and `alert_triage` are
     explicitly framed as handoff layers, not replacements — the former
     always recommends the full `agents/backtest_review/` agent before a
     production-promotion decision, the latter never suppresses,
     escalates, resolves, or re-routes an alert, deferring all of that to
     `agents/alerts/alert_router/` and
     `agents/alerts/incident_notification/`.
5. **P0 optimizer-agent workflow expansion (continued)** — the solver
   toolkit (`0013`) has no financing-specific application spec yet;
   collateral/margin LP or cardinality-constrained portfolio (MILP) would
   be the first.
6. **Adoption guide** — done. `docs/adoption_guide.md` is a full walkthrough of both
   layers: `pip install quantsmith` + using the runtimes, and copying the scaffold +
   wiring the gates, with per-project-type recipes.
7. **Packaging** — done (package phase active). `docs/packaging.md` records the hybrid
   (versioned `quantsmith` package for the runtimes + template for the scaffold);
   `CHANGELOG.md` and a versioning policy are in place. Remaining optional step: the
   Copier `qf` sync CLI, and an optional PyPI release when there is demand.
8. **More worked examples** — the forecast spec is done
   (`specs/0006-ml-return-forecasting/`); still open: a risk-model spec end to end
   and an ingestion example that emits a data contract (see item 3).
9. **Remaining backing instructions** — risk_management, data_ingestion,
   reproducibility. (`pipeline_engineering`, `metrics_semantic_layer`,
   `data_storytelling`, `monitoring`, `alerting`, `asset_class_mechanics`,
   `role_operations`, and `data_provenance` are shipped.)
10. **`CHANGELOG.md`** — done (Keep a Changelog + a SemVer-style versioning policy).
11. **Optional gates** — `ingestion-snapshot`; a stricter notebook-output gate;
    revisit enforcing `leakage`.
12. **Shipped since this section was last written (specs `0019`–`0028`):**
    - `0019` pipeline observability.
    - `0020`/`0021` the monitoring → alerting chain (`agents/monitoring/`,
      `agents/alerts/`, `adapters/alert_delivery/`).
    - `0022` asset-class mechanics agents, feeding `trading_strategies/` and
      `securities_financing/`.
    - `0023` the securities-lending workflow promoted to a tested runtime,
      with a balance-sheet-cap correctness fix found along the way.
    - `0024`/`0025` role-operations Phase 1 + the data-provenance guardrail
      — see item 4, the dedicated tracking entry for this initiative.
    - `0026` the model plugin adapter — register an already-built internal
      optimization model as a reviewed, contract-bound plugin via a
      local-only `model_plugins.yml`.
    - `0027` the data source catalog (`sources/`) — a centralized,
      per-source registry of APIs/DBs/feeds with quality, point-in-time,
      and credential-pointer metadata, wired into `data_contract.md`,
      `credential_access`, and `data_ingestion`; populated with six public
      sources (FRED, BLS, EIA, BEA, Census, SEC EDGAR), with a matching
      `adapters/data_access/external_apis/eia.md` profile added.
    - `0028` financing cost analysis promoted to a tested, dependency-free
      runtime — cost-of-carry decomposition, financing-aware returns,
      understated-backtest flags, rate-shock sensitivity, and
      classification-keyed capacity findings, reconciling with `0023`'s
      rate/classification vocabulary by value (no `numpy` dependency added).
    - `0029`/`0030` role-operations Phases 2 and 3 — see item 4, the
      dedicated tracking entry for this initiative. The fourteen-agent
      roster is now complete.

    **Recommended next:** promote `repo_financing`/`collateral_management`
    to tested runtimes if a concrete workflow needs to derive their inputs
    (or leave them agent-contract-only — `financing_cost_analysis` doesn't
    require it), an optimizer application spec on the `0013` solver
    toolkit (e.g. collateral/margin LP), an executable dispatcher for
    `0026` once a concrete invocation target exists, and continuing to
    populate `sources/` as real sources come into use.

## Open Questions For The Owner

- Copyable scaffold, Python package, or CLI/copier? (Directionally answered in
  `docs/packaging.md`; revisit its criteria if audience or update cadence changes.)
- Which agent runtime is the primary target (local, general LLM, both)?
- Which gates should graduate from advisory to enforced, and when?
- Should downstream repos pin a version of the SDK, and how are updates delivered?

## Risks

- Breadth: 131 agents is useful only if each stays narrow and inspectable.
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
