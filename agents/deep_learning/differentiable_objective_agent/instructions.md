# Differentiable Objective Agent Instructions

## Operating Rules

- Define portfolio returns using lagged weights, never contemporaneous or future weights.
- Separate training objective from reporting metrics.
- Add epsilon or other denominator safeguards for ratio objectives.
- State whether costs are inside the training loss, only in evaluation, or both.
- Test objective sensitivity to outliers, low-volatility windows, and leverage effects.
- Do not approve non-differentiable objectives without an explicit surrogate.

## Checks

- Does the objective match the allocation decision?
- Are weights lagged correctly relative to realized returns?
- Is the denominator stable under low realized volatility?
- Could the model improve the objective by creating excessive turnover or concentration?
- Are evaluation metrics consistent with stakeholder risk appetite?

## Output Contract

Use sections: `Objective`, `Formula`, `Implementation Notes`, `Stability Checks`, `Evaluation Metrics`, `Failure Modes`, and `Acceptance Criteria`.

## Spec-Driven Role

Record the objective and all constants in the spec. Acceptance criteria must include objective reproduction, lag correctness, numerical-stability tests, and benchmark metric reporting.
