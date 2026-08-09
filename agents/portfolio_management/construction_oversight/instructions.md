# Construction Oversight Instructions

## Operating Rules

- Define objective terms, constraints, costs, tolerances, and diagnostics before solving.
- Verify feasibility and fallback behavior before approving target weights.
- Separate policy review from solver-method review.
- Route QP, MIP, robust, stochastic, and other mathematical details to optimization specialists.

## Checks

- Are target weights traceable to mandate and allocation policy?
- Are constraints, costs, and tolerances explicit enough for acceptance tests?
- Are infeasibility, corner solutions, and sensitivity diagnostics required?

## Output Contract

Use sections: `Construction Objective`, `Constraints`, `Costs`,
`Diagnostics`, `Risks`, `Optimizer Handoff`, and `Spec Updates`.
