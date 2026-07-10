# Prompt: Plan (author a technical plan)

Use with the Design & Architecture Agent to produce `plan.md` from an approved
`spec.md`.

## Inputs

- The approved `spec.md` (with `REQ-*`, `NFR-*`, `AC-*`).
- Existing architecture, datasets, and interfaces.
- Constraints and known risks.

## Instructions

Follow `instructions/spec_driven_development.md` and the constitution. Produce a
`plan.md` from `templates/spec/plan.md` that defines HOW.

Requirements:

- The plan requires an approved spec; refuse to plan without one.
- Fill the **traceability matrix**: every `REQ-*`/`NFR-*` maps to a design element
  and the tasks that will deliver it.
- Complete the **constitution check** (P4, P5, P6, P9 at minimum).
- Record trade-offs with the rejected alternative and why.
- Define the validation strategy for every `AC-*` and the rollback/observability
  plan.

## Output

A completed `plan.md` with a full traceability matrix and constitution check, plus
any open design questions.
