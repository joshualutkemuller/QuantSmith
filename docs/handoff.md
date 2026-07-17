# QF Workflow SDK Handoff

## Snapshot

The SDK now has a working v1: a **spec-driven engineering framework** layered over
the **six software-development stages**, a catalog of **21 agents**, **14 quality
gates**, and CI that enforces the deterministic ones. It remains a scaffold to be
copied into quant repos, not a runnable app.

- Branch of record for this build-out: `claude/dev-stages-hooks-agents-co1sjj`
  (open as PR #4 into `main`). Earlier slices landed via PRs #2 and #3.
- Root `CLAUDE.md` activates the framework by default for any agent in the repo.

## What This Session Added

**Spec-Driven Development (the operating model)**

- `instructions/engineering_principles.md` — the constitution (10 non-negotiable rules + exceptions).
- `instructions/spec_driven_development.md` — flow, ID scheme (`REQ`/`NFR`/`AC`/`T`/`RISK`), gates.
- `instructions/point_in_time.md` — point-in-time & leakage checklist.
- `templates/spec/{spec,plan,tasks}.md` + `prompts/{specify,plan,tasks}.md`.
- `specs/0001-daily-momentum-signal/` — a fully worked, traceable reference spec.

**Agents (21 total, all on the four-file contract)**

- Orchestrator: `workflow_orchestrator/` — drives the flow and enforces stage gates.
- Six lifecycle agents (one per stage): `planning_requirements`, `design_architecture`,
  `implementation`, `testing_validation`, `deployment_release`, `maintenance_monitoring`.
- Domain agents: `research_analyst`, `data_quality`, `feature_engineering`, `modeling`,
  `backtest_review`, `risk`, `git_release`.
- `data_ingestion/` group: `database_connectivity`, `file_ingestion`, `api_ingestion`.
- `secrets_management/` group: `secret_storage`, `credential_access`, `secret_rotation`, `secret_scanning`.
- `agents/README.md` — the agent catalog and the orchestrator's routing table.

**Quality gates (`hooks/stages/`, advisory by default, enforce with `QF_STAGE_ENFORCE=1`)**

- Cross-cutting: `spec-check` (traceability chain).
- Per stage: `planning`, `design`, `implementation`, `testing`, `deployment`, `maintenance`.
- Quant gates: `leakage`, `backtest`, `repro`, `data-contract`.
- Repo gates: `secret-scan`, `docs-link`, `agent-catalog`.
- Driver `run-stage.sh`, shared `common.sh`, and `hooks/README.md`.

**Templates & prompts**

- `templates/docs/{run_card,model_monitoring_plan,incident_postmortem}.md`,
  `templates/data/data_contract.md`, and matching prompts.

**Enforcement plumbing**

- `.githooks/pre-commit` and `pre-push` validate the agent contract recursively
  (any directory containing `prompt.md`, so category folders work).
- `.github/workflows/ci.yml` enforces required docs, the agent contract, shell
  syntax, spec traceability, backtest integrity, secret-scan, docs-link, and
  agent-catalog; runs leakage advisory. Uses `actions/checkout@v7` + `fetch-depth: 0`.

## Current Surfaces

```text
qf_workflow_sdk/
  CLAUDE.md                # repo guide; activates the framework by default
  agents/                  # 21 agents + README.md catalog (some grouped in folders)
  hooks/stages/            # 14 gates + run-stage.sh + common.sh
  instructions/            # constitution, SDD method, point-in-time, quant standards
  prompts/                 # spec commands + artifact prompts
  specs/                   # per-feature spec dirs; 0001 is a worked example
  templates/               # spec/, docs/, data/ artifact templates
  examples/                # alpha_signal_handoff end-to-end example
  docs/                    # sdk_plan, handoff, (architecture/adoption still TODO)
```

## What's Next (prioritized)

1. **Adoption guide** (`docs/adoption_guide.md`): how to copy the SDK into an
   existing quant repo — which folders to take, how to wire `setup-hooks.sh` and
   the CI gates, and how to tune the heuristic gates' patterns to a repo's layout.
2. **Packaging decision**: stays a copyable scaffold, or grows a CLI/copier that
   installs selected agents, prompts, hooks, and templates. Open question below.
3. **More worked examples**: only a momentum-signal spec and the alpha-signal
   handoff exist. Add a risk-model or forecast-model spec end to end, and an
   ingestion example that produces a data contract.
4. **Refresh the roadmap and vocabulary**: `docs/sdk_plan.md` backlog still lists
   agents/hooks that now exist; `agentic_dictionary.md` predates spec-driven terms
   (constitution, gate, orchestrator, run card, data contract). Bring both current.
5. **Optional gates** (deferred by design): an `ingestion-snapshot` gate (verify a
   pull captures a snapshot/checksum) and a stricter notebook-output gate.
   `leakage` is intentionally advisory (heuristic); revisit before enforcing it.
6. **`CHANGELOG.md`**: the deployment gate flags its absence; add one and a
   versioning policy if the SDK starts being consumed by other repos.

## Quality Gates — Enforced vs Advisory

- **Enforced in CI:** required docs, agent contract, shell syntax, `spec`,
  `backtest`, `secret-scan`, `docs-link`, `agent-catalog`.
- **Advisory (run locally or wire in later):** `leakage` (heuristic by design) and
  the per-stage/quant gates not listed above. `QF_STAGE_ENFORCE=1` makes any gate
  blocking; do this per gate as a repo's discipline matures.

## Conventions To Preserve

- Every agent: `README.md`, `prompt.md`, `instructions.md`, `tasks.md`, plus a
  `Spec-Driven Role` section and a catalog row. Group related agents in a category
  folder (its own `README.md`, no `prompt.md`).
- Specs are the source of truth; assign stable IDs and keep traceability intact.
- Conventional Commits; do all work on the feature branch; a merged PR is finished
  (start follow-ups fresh from `main`, rebasing any unmerged commits).
- Gates degrade gracefully when optional tools are missing.

## Open Questions For The Owner

- Copyable scaffold, Python package, or CLI/copier?
- Which agent runtime is the primary target (local Codex-style, general LLM, both)?
- Which gates should graduate from advisory to enforced, and when?
- Which quant artifact is the next complete example: risk model, forecast, optimizer?
- Should downstream repos pin a version of the SDK, and how are updates delivered?

## Risks

- Breadth: 21 agents is useful only if each stays narrow and inspectable.
- Heuristic gates (`leakage`, `backtest`, `secret-scan` fallback) can false-positive
  or miss; keep them advisory unless a repo's layout makes them reliable.
- Docs can drift from the code they describe; the `docs-link` and `agent-catalog`
  gates help, but `sdk_plan.md`/`agentic_dictionary.md` still need a manual refresh.
- Copied gates assume conventional artifact names; adopters must tune the patterns.

## Definition Of Done For The Next Slice

- `docs/adoption_guide.md` exists and a fresh repo can install the SDK from it.
- `docs/sdk_plan.md` backlog and `agentic_dictionary.md` reflect the current build.
- A second end-to-end worked example (beyond the momentum signal) exists.
- The packaging decision is recorded, with a path (scaffold vs CLI) chosen.
