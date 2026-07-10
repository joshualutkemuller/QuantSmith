# Design & Architecture Instructions

## Operating Rules

- Trace every design element back to a specific requirement.
- Define interfaces and data contracts before internal logic.
- Design for reproducibility, time alignment, and leakage safety by default.
- Prefer the simplest design that meets the requirements and non-functionals.
- Record at least one rejected alternative and why it lost.
- Include how the design will be tested, observed, and rolled back.
- Do not hide a hard trade-off; name it and pick a side.

## Checks

- Does the design satisfy every must-have requirement?
- Are interfaces, inputs, outputs, and data contracts explicit?
- Are failure modes and their handling described?
- Is there a validation strategy tied to acceptance criteria?
- Are observability and rollback considered before launch?
- Are the non-functional constraints (latency, cost, capacity) addressed?

## Output Contract

Use clear Markdown sections. Always include a `Trade-offs` section and an
`Open Questions` section. When the design affects production trading, data
lineage, or compliance, include a `Failure Modes & Rollback` section.
