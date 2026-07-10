# Prompt: Tasks (break a plan into traceable work)

Use with the Coding & Implementation Agent to produce `tasks.md` from an approved
`spec.md` and `plan.md`.

## Inputs

- The approved `spec.md` and `plan.md`.
- Repository conventions and existing interfaces.

## Instructions

Follow `instructions/spec_driven_development.md` and the constitution. Produce a
`tasks.md` from `templates/spec/tasks.md`.

Requirements:

- Assign `T-*` IDs; every task cites the `REQ-*`/`NFR-*` it advances (no orphans).
- Order tasks so each is independently reviewable and testable.
- Fill the **test coverage map**: every `AC-*` is named by at least one planned
  test.
- State the Definition of Done and list any deferred follow-ups explicitly.

## Output

A completed `tasks.md` with a traceable task list and test coverage map, ready to
drive implementation.
