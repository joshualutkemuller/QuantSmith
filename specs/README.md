# Specs

Each unit of work lives in its own directory here, following Spec-Driven
Development (see `instructions/spec_driven_development.md`).

```
specs/
  NNNN-short-slug/
    spec.md    # WHAT and WHY  — requirements, acceptance criteria, non-goals
    plan.md    # HOW           — architecture, data contracts, trade-offs
    tasks.md   # WORK          — ordered, traceable, testable tasks
```

- `NNNN` is a zero-padded sequence number; the slug is short kebab-case.
- Start from `templates/spec/`.
- The `spec-check` hook (`hooks/stages/spec-check.sh`) validates the chain and
  traceability across these directories.

## Index

| ID | Feature | Status |
| --- | --- | --- |
| 0001-daily-momentum-signal | Example: daily cross-sectional momentum signal | Approved (reference) |

`0001-daily-momentum-signal/` is a filled-in reference showing the ID scheme and
traceability end to end. Copy its structure, not its content.
