# Deep Portfolio Optimization Agent Instructions

## Operating Rules

- Optimize the portfolio decision directly when the decision is allocation.
- State why a prediction-loss objective is insufficient or acceptable.
- Require time-ordered validation with no shuffled splits for market data.
- Require simple allocation and classical optimizer baselines before neural complexity.
- Encode long-only, leverage, concentration, and turnover constraints explicitly.
- Treat high Sharpe without turnover/cost/drawdown evidence as incomplete.
- Document every objective variant tried to control data-snooping risk.

## Checks

- Is the model output a valid allocation at each decision time?
- Is the objective computed only from information available at that time?
- Are baselines competitive and decision-relevant?
- Does the evaluation include transaction costs and turnover?
- Does the model remain useful under higher cost assumptions?
- Are results stable by regime, asset class, and retraining window?

## Output Contract

Use Markdown sections: `Decision`, `Objective`, `Inputs`, `Allocation Layer`, `Baselines`, `Validation`, `Risk Review`, `Acceptance Criteria`.

## Spec-Driven Role

Translate the portfolio objective, constraint set, baseline suite, and validation protocol into `spec.md` and `plan.md`. Implementation belongs under `src/quantsmith/` only after the acceptance criteria define out-of-sample, after-cost, and regime-specific performance evidence.
