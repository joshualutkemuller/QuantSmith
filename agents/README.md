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

## How They Fit Together

1. The **orchestrator** determines the lifecycle position and the next gate.
2. It routes to the **lifecycle agent** that owns the current stage.
3. That agent pulls in **domain agents** for the expertise it needs.
4. The **hooks** verify the gate mechanically before the orchestrator advances.
5. The **spec** carries state between stages as the single source of truth.

## Adding An Agent

- Create `agents/<name>/` with all four contract files (the pre-commit, pre-push,
  and CI checks require them).
- Give it a narrow, inspectable responsibility.
- Add a `Spec-Driven Role` section to its `instructions.md`.
- Add a row to the relevant table above.
