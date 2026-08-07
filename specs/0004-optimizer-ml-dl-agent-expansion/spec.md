# Spec: Optimizer, Machine Learning, And Deep Learning Agent Expansion

- **ID:** 0004-optimizer-ml-dl-agent-expansion
- **Status:** Approved
- **Author:** Codex
- **Approver:** Josh
- **Last updated:** 2026-08-07

## Problem & Context

QuantSmith needs a routable agent surface for optimization, machine-learning, and deep-learning work that spans finance, operations, and technology. The current optimizer placeholder does not give the workflow orchestrator enough structure to classify problem types, choose specialist reviewers, promote ideas into specs, or string workflows together.

## Goals

- Add comprehensive specialist agent groups for optimization, machine learning, and deep learning.
- Make optimizer coverage the highest-priority handoff because optimization is the bridge from decision intent to executable specs and workflows.
- Keep each specialist as a four-file agent contract and keep executable code under `src/quantsmith/`.
- Update catalogs and workflow docs so orchestrators can route work deterministically.

## Non-Goals

- No solver, ML, or deep-learning runtime implementation in this slice.
- No external provider integrations, data pulls, or model training jobs.
- No automatic workflow execution beyond documented contracts and routing guidance.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall provide a grouped optimization agent family covering finance, operations, and technology optimization problem types. | must |
| REQ-002 | The system shall provide grouped machine-learning and deep-learning agent families with specialist roles for modeling workflows. | must |
| REQ-003 | The agent catalog and workflow documentation shall describe how optimization, ML, and DL agents compose with specs and lifecycle agents. | must |
| REQ-004 | The handoff backlog shall mark the optimizer-agent expansion as the highest-priority workflow handoff. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Agent contract consistency | Every public agent has `README.md`, `prompt.md`, `instructions.md`, and `tasks.md`. |
| NFR-002 | Repository hygiene | `agent-catalog`, `docs-link`, `spec`, and formatting checks pass. |
| NFR-003 | Runtime boundary | Agent docs do not introduce executable runtime code outside `src/quantsmith/`. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given the repo agents directory, when the catalog check runs, then every new public agent is listed in `agents/README.md`. | REQ-001, REQ-002, NFR-001 |
| AC-002 | Given a workflow request involving optimization, ML, or DL, when the workflow map is read, then it names a route from orchestrator to specialist to lifecycle/spec artifacts. | REQ-003 |
| AC-003 | Given the handoff backlog, when priorities are reviewed, then the optimizer-agent expansion is listed as the highest-priority handoff. | REQ-004 |
| AC-004 | Given the documentation set, when doc-link and spec checks run, then the new spec and docs pass. | NFR-002, NFR-003 |

## Data & Dependencies

No data dependencies. This slice creates agent contracts and documentation only. Future implementation specs may depend on solver libraries, model frameworks, data adapters, and runtime packages.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | The agent set becomes too broad to route clearly. | Orchestrator confusion and duplicated responsibilities. | Use grouped README maps, narrow specialist names, and explicit handoff rules. |
| RISK-002 | Docs imply executable capabilities that do not exist yet. | Users may expect live solvers/models. | State runtime implementation is out of scope and belongs in future specs under `src/quantsmith/`. |
| RISK-003 | Optimization, ML, and DL concerns overlap. | Redundant reviews or inconsistent recommendations. | Use orchestrators to classify the primary method and call adjacent agents only for named handoffs. |

## Assumptions & Open Questions

- Assumption: Specialist agent contracts are the right next layer before implementing runtime workflows.
- Assumption: Optimization gets highest priority because many finance, ops, and tech workflows are constrained decision problems.
- Open question: Which optimization runtime spec should be implemented first: collateral, portfolio, execution, capacity, or solver diagnostics?

## Exceptions

None.
