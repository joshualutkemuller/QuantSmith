# Portfolio Stress Explainability Agent Tasks

## Intake

- Identify stress windows and regime labels.
- Collect weights, scaled positions, returns, volatility estimates, and feature tensors.
- Group features into interpretable categories.

## Analysis

- Plot or tabulate allocation changes through the stress period.
- Compare raw and volatility-scaled positions.
- Compute feature sensitivity or attribution where supported.
- Compare model behavior against allocation and classical optimization baselines.
- Identify counterintuitive or unstable allocation shifts.

## Validation

- Verify attribution is computed without future information.
- Check whether the explanation is stable across retraining windows.
- Confirm the stress report includes failure cases, not only successes.

## Handoff

- Add stress-report requirements to `tasks.md`.
- Route drawdown and concentration findings to `risk` and `backtest_review`.
