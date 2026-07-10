# Prompt: Specify (author a spec)

Use with the Planning & Requirements Analysis Agent to produce `spec.md`.

## Inputs

- The request, hypothesis, or problem statement.
- Intended decision or use case.
- Known constraints (data, latency, cost, capacity, compliance).
- Existing systems, datasets, or prior work touched.

## Instructions

Follow `instructions/spec_driven_development.md` and the constitution in
`instructions/engineering_principles.md`. Produce a `spec.md` from
`templates/spec/spec.md` that captures WHAT and WHY only — no implementation.

Requirements:

- Assign stable IDs: `REQ-*`, `NFR-*`, `AC-*`, `RISK-*`.
- Every acceptance criterion is testable and maps to a requirement.
- Include an explicit Non-Goals section.
- Record assumptions and open questions instead of inventing facts.

## Output

A completed `spec.md` under `specs/NNNN-slug/`, ready for review, plus a short
list of the open questions that block approval.
