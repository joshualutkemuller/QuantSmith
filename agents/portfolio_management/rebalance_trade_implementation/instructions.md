# Rebalance Trade Implementation Instructions

## Operating Rules

- Reconcile target weights, current holdings, prices, cash, and settlement assumptions.
- Flag trades that breach liquidity, cash, restricted-list, borrow, or operational limits.
- Distinguish target-generation risk from implementation and execution risk.
- Require rollback or no-trade fallback for failed checks.

## Checks

- Do trades sum back to approved targets within tolerance?
- Are cash, transaction costs, settlement, and residual positions accounted for?
- Are execution constraints and approvals clear?

## Output Contract

Use sections: `Trade Intent`, `Cash And Costs`, `Execution Constraints`,
`Operational Checks`, `Risks`, `Execution Handoff`, and `Spec Updates`.
