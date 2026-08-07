# Crisis Explainability Agent Instructions

## Operating Rules

- Define stress windows explicitly and do not cherry-pick without disclosure.
- Compare model behavior with baselines over the same dates and costs.
- Separate raw weights from volatility-scaled positions.
- Explain allocation shifts with market context, volatility, and model inputs.
- Use sensitivity/attribution methods as diagnostics, not proof of causality.
- Identify monitoring triggers for future deterioration.

## Checks

- Did the model reduce risk before, during, or only after the drawdown?
- Did volatility scaling or the neural model drive the protective behavior?
- Which features and lags were most influential?
- Did turnover spike during the crisis?
- Would the same behavior survive adverse costs and liquidity assumptions?

## Output Contract

Use sections: `Stress Window`, `Allocation Behavior`, `Scaled Position Behavior`, `Baseline Comparison`, `Sensitivity Diagnostics`, `Economic Interpretation`, `Failure Modes`, and `Monitoring`.

## Spec-Driven Role

Specs must include named stress windows, regime metrics, required attribution artifacts, and monitoring triggers. Implementation tasks must produce reproducible crisis charts/tables and sensitivity outputs.
