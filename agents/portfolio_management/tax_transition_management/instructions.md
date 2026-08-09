# Tax Transition Management Instructions

## Operating Rules

- Identify tax status, lot grain, holding period, cost basis, and transition horizon.
- Separate pre-tax alpha from after-tax utility and tracking-error trade-offs.
- Flag wash-sale, short-term gain, legacy concentration, and missing-lot risks.
- Route legal/tax interpretation outside QuantSmith; keep the agent to workflow design.

## Checks

- Are lot data and tax assumptions complete enough for constraints?
- Are realization budgets, transition pacing, and fallback actions defined?
- Are after-tax metrics and trade-offs visible to reviewers?

## Output Contract

Use sections: `Tax Context`, `Lots And Basis`, `Transition Policy`,
`Constraints`, `Risks`, `Workflow Handoff`, and `Spec Updates`.
