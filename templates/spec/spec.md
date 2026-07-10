# Spec: <feature name>

- **ID:** NNNN-short-slug
- **Status:** Draft | In Review | Approved | Superseded
- **Author:**
- **Approver:**
- **Last updated:** YYYY-MM-DD

> WHAT and WHY only. No implementation detail — that belongs in `plan.md`.

## Problem & Context

What problem is this solving, for whom, and what decision does it support? Link
to the request, thread, or hypothesis that started it.

## Goals

- The outcomes this work must achieve.

## Non-Goals

- Explicitly out of scope. Silence is not a boundary; name what you are not doing.

## Requirements

Functional requirements, each with a stable ID.

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall … | must |
| REQ-002 | The system shall … | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Latency | p99 < … |
| NFR-002 | Cost / capacity / compliance | … |

## Acceptance Criteria

Each criterion is testable and maps to a requirement.

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given …, when …, then … | REQ-001 |
| AC-002 | Given …, when …, then … | NFR-001 |

## Data & Dependencies

Data sources, contracts, lineage, and upstream systems this depends on. Note
access constraints and any private-data handling requirements.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | … | … | … |

## Assumptions & Open Questions

- Assumption: …
- Open question: …

## Exceptions

Record any approved deviation from `instructions/engineering_principles.md`:
principle, reason, risk accepted, approver, expiry. Leave empty if none.
