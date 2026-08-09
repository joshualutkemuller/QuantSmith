# Allocation Policy Instructions

## Operating Rules

- Define capital budget, risk budget, sizing rule, and rebalance trigger separately.
- Start with a baseline policy and justify any added complexity.
- Include concentration, factor, sector, liquidity, turnover, and capacity limits.
- Define fallback behavior when forecasts, risk inputs, or prices are stale.

## Checks

- Does the policy map evidence to portfolio action without hidden discretion?
- Are drift bands and rebalance triggers measurable?
- Can the policy be converted into construction objectives and constraints?

## Output Contract

Use sections: `Policy`, `Baseline`, `Sizing Rules`, `Risk Budgets`,
`Rebalance Triggers`, `Risks`, `Workflow Handoff`, and `Spec Updates`.
