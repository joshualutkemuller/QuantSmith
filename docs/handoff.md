# QuantSmith Handoff

## Snapshot

The SDK has a working v1: a **spec-driven engineering framework** over the six
software-development stages, **43 agents**, **15 quality gates**, **13 instruction
standards**, and CI that enforces the deterministic gates. It remains a scaffold to
be copied into quant repos, not a runnable app.

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

**Agents (43)** — all on the four-file contract (`README`/`prompt`/`instructions`/
`tasks`) with a `Spec-Driven Role`:

- Orchestrator: `workflow_orchestrator/`.
- Lifecycle (one per stage): `planning_requirements`, `design_architecture`,
  `implementation`, `testing_validation`, `deployment_release`, `maintenance_monitoring`.
- Core domain: `research_analyst`, `data_quality`, `feature_engineering`, `modeling`,
  `backtest_review`, `risk`, `git_release`.
- Groups: `data_ingestion/` (3), `secrets_management/` (4), `tooling/` (3 — Excel,
  Power BI, Tableau), `knowledge/` (4), `trading_strategies/` (8 archetypes from
  *151 Trading Strategies*), `securities_financing/` (4), `formulaic_alphas/` (3 —
  from *101 Formulaic Alphas*).

**Gates (15)** in `hooks/stages/`, driven by `run-stage.sh`; advisory by default,
`QF_STAGE_ENFORCE=1` blocks:

- Cross-cutting: `spec`. Per stage: `planning`, `design`, `implementation`,
  `testing`, `deployment`, `maintenance`.
- Quant: `leakage`, `backtest` (incl. a financing theme for shorts), `repro`,
  `data-contract`.
- Repo: `secret-scan`, `docs-link`, `agent-catalog`, `knowledge`.

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
  `backtest`, `secret-scan`, `docs-link`, `agent-catalog`.
- **Advisory:** `leakage` (heuristic by design) and the per-stage/quant gates not
  listed above. Graduate a gate to enforced per repo as discipline matures.

## What's Next (prioritized)

1. **Adoption guide** (`docs/adoption_guide.md`) — expand into a full walkthrough of
   installing the SDK into an existing quant repo.
2. **Packaging** — execute the decision in `docs/packaging.md` (template now, sync
   CLI later, package only with real code).
3. **More worked examples** — a risk/forecast spec end to end; an ingestion example
   that emits a data contract.
4. **Remaining backing instructions** — risk_management, data_ingestion,
   reproducibility, monitoring.
5. **`CHANGELOG.md`** and a versioning policy once the SDK is consumed elsewhere.
6. **Optional gates** — `ingestion-snapshot`; a stricter notebook-output gate;
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
- Docs can drift from the code; the `docs-link` and `agent-catalog` gates help, but
  narrative docs (this file, `sdk_plan.md`, `agentic_dictionary.md`) need periodic
  manual refresh.
- Copied gates assume conventional artifact names; adopters must tune the patterns.

## Definition Of Done For The Next Slice

- `docs/adoption_guide.md` is complete enough that a fresh repo can install the SDK.
- The packaging decision has a chosen path with first steps taken.
- A second end-to-end worked example exists beyond the momentum signal.
