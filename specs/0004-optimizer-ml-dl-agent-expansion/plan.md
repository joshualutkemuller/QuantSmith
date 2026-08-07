# Plan: Optimizer, Machine Learning, And Deep Learning Agent Expansion

- **Spec:** 0004-optimizer-ml-dl-agent-expansion (`spec.md`)
- **Status:** Approved
- **Author:** Codex
- **Last updated:** 2026-08-07

## Approach

Create three category folders under `agents/`: `optimization/`, `machine_learning/`, and `deep_learning/`. Each category contains a README group map plus narrow four-file public agents. Add backing instruction standards for each group and update the agent catalog, workflow map, handoff, and future-feature backlog.

## Architecture & Components

```text
workflow_orchestrator
  -> optimization | machine_learning | deep_learning group orchestrator
  -> specialist agent
  -> lifecycle agent: planning_requirements -> design_architecture -> implementation -> testing_validation
  -> spec artifacts under specs/NNNN-slug/
  -> runtime code under src/quantsmith/ when implementation is approved
```

## Interfaces & Data Contracts

The new files are Markdown contracts only. Their inputs and outputs are agent-level control context: problem descriptions, specs, plans, tasks, run cards, data contracts, validation evidence, and handoff notes. No runtime schema or provider API is introduced in this slice.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Specialist contracts require baselines, validation design, and point-in-time review before implementation. |
| P5 Reversibility | yes | Changes are docs/contracts only and isolated on a branch. |
| P6 Observability | yes | Agents require monitoring and run-card fields for production candidates. |
| P9 Security & data | yes | Contracts prohibit credentials, private data, client identifiers, and MNPI. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `agents/optimization/` group and optimization standard | T-001, T-004 |
| REQ-002 | `agents/machine_learning/`, `agents/deep_learning/`, and backing standards | T-002, T-003, T-004 |
| REQ-003 | `agents/README.md`, `docs/workflows.md`, `specs/README.md` updates | T-005 |
| REQ-004 | `docs/handoff.md` and `docs/handoffs/future_features.md` priority updates | T-006 |
| NFR-001 | Four-file generator pattern and agent-catalog check | T-001, T-002, T-003, T-007 |
| NFR-002 | Validation gates | T-007 |
| NFR-003 | Runtime boundary language in prompts/instructions | T-004, T-005 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Agent layout | Grouped families with specialist subagents | One giant optimizer or ML prompt | Grouped routing is more inspectable and avoids prompt sprawl. |
| Runtime scope | Contracts and docs only | Add solver/model runtime now | Runtime needs separate specs, data, dependencies, and tests. |
| Priority marker | P0/highest in handoff backlog | Fit into existing P1/P2/P3 only | User explicitly requested highest priority. |

## Validation Strategy

Run `hooks/stages/run-stage.sh spec agent-catalog docs-link`, `git diff --check`, and file-presence checks for every public agent contract. AC-001 is covered by agent-catalog. AC-002 and AC-003 are covered by docs-link plus direct document inspection. AC-004 is covered by spec/doc checks.

## Rollout, Observability & Rollback

Rollout is a branch and PR. Rollback is reverting the single docs/contracts commit. Future runtime specs should add solver/model tests, sample configs, run cards, and monitoring plans.

## Open Questions

- Which runtime workflow gets built first: optimizer router, collateral optimizer, portfolio optimizer, or ML/DL model factory?
