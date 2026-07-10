# Plan: <feature name>

- **Spec:** NNNN-short-slug (`spec.md`)
- **Status:** Draft | In Review | Approved
- **Author:**
- **Last updated:** YYYY-MM-DD

> HOW. This plan requires an approved `spec.md`. Every requirement in the spec
> must appear in the traceability matrix below.

## Approach

The chosen design in a few paragraphs. How it satisfies the goals in the spec.

## Architecture & Components

Components, their responsibilities, and how they interact. A text diagram is fine.

## Interfaces & Data Contracts

Inputs, outputs, schemas, and — for data/feature work — time-alignment and
leakage controls that make the design correct by construction.

## Constitution Check

Confirm the design upholds `instructions/engineering_principles.md`. Call out P4
(correct by construction), P5 (reversibility), P6 (observability), and P9
(security/data) explicitly.

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes/no | … |
| P5 Reversibility | yes/no | … |
| P6 Observability | yes/no | … |
| P9 Security & data | yes/no | … |

## Traceability Matrix

Every `REQ-*`/`NFR-*` from the spec maps to a design element and the tasks that
deliver it.

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | … | T-001, T-002 |
| NFR-001 | … | T-003 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| … | … | … | … |

## Validation Strategy

How each `AC-*` will be proven. Test types, data, and — for models/backtests —
the validation scheme (splits, leakage controls, significance).

## Rollout, Observability & Rollback

Rollout strategy scaled to blast radius; monitoring and alert thresholds; the
rollback path and, where relevant, the kill switch.

## Open Questions

- …
