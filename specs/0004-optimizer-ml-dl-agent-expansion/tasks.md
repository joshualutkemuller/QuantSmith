# Tasks: Optimizer, Machine Learning, And Deep Learning Agent Expansion

- **Spec:** 0004-optimizer-ml-dl-agent-expansion (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

## Definition of Done (applies to every task)

- Agent contracts follow the four-file convention.
- Docs and catalogs are updated alongside new public agents.
- Runtime boundaries remain clear: executable code belongs under `src/quantsmith/`.
- No secrets, credentials, private data, or fabricated capability claims are introduced.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Add optimization group and specialist agents. | REQ-001, NFR-001 | done | Includes orchestrator and solver/domain specialists. |
| T-002 | Add machine-learning group and specialist agents. | REQ-002, NFR-001 | done | Covers framing, features, supervised, forecasting, ranking, causal, anomaly, validation, AutoML, online learning, and MLOps. |
| T-003 | Add deep-learning group and specialist agents. | REQ-002, NFR-001 | done | Covers training systems, neural tabular, transformers, GNNs, RL, vision, NLP/LLM, representations, generative models, time series, and serving. |
| T-004 | Add backing instruction standards. | REQ-001, REQ-002, NFR-003 | done | Adds optimization, machine-learning, and deep-learning standards. |
| T-005 | Update catalogs and workflow map. | REQ-003, NFR-002, NFR-003 | done | Adds routing documentation and spec index. |
| T-006 | Update handoff/backlog with highest-priority optimizer expansion. | REQ-004 | done | Adds P0 priority handoff. |
| T-007 | Run validation gates. | NFR-001, NFR-002 | done | `spec`, `agent-catalog`, `docs-link`, shell syntax, contract presence, and `git diff --check` passed. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `hooks/stages/run-stage.sh agent-catalog` | done |
| AC-002 | `hooks/stages/run-stage.sh docs-link`; inspect `docs/workflows.md` | done |
| AC-003 | `hooks/stages/run-stage.sh docs-link`; inspect `docs/handoff.md` and `docs/handoffs/future_features.md` | done |
| AC-004 | `hooks/stages/run-stage.sh spec docs-link`; `git diff --check` | done |

## Follow-ups

- The first runtime ML/DL workflow is promoted to `specs/0006-ml-return-forecasting/`
  — a cross-sectional return forecast routing the `machine_learning/` and
  `deep_learning/` groups from labeling through monitored serving.
- Promote the first runtime *optimization* workflow into a new spec (next free number
  is `0007-*`).
- Add solver/runtime adapters only after a concrete workflow chooses data, solver, and acceptance criteria.
