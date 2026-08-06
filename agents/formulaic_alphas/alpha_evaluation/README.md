# Alpha Evaluation Agent

## Purpose

The Alpha Evaluation Agent assesses a formulaic alpha's real characteristics:
holding period, turnover, volatility dependence, correlation to known alphas,
capacity, and decay/crowding. It separates a genuine, tradable edge from an
in-sample artifact.

## Use When

- A formulaic alpha needs its holding period, turnover, and capacity characterized.
- An alpha's dependence on volatility or other factors needs assessment.
- Correlation to known/common alphas needs checking before adding it.
- Decay and crowding of an alpha over time need evaluation.

## Inputs

- The alpha's signal and return series, point-in-time.
- Turnover, transaction-cost (cents-per-share), and capacity assumptions.
- Reference alphas/factors to correlate against.
- The evaluation window and out-of-sample period.

## Outputs

- Holding period and turnover characterization.
- A net-of-cost performance view (transaction costs dominate short-horizon alphas).
- Volatility and factor-dependence analysis.
- Correlation to known alphas and crowding assessment.
- Capacity and decay estimates.

## Example Requests

- "Characterize this alpha's holding period, turnover, and capacity."
- "Is this alpha's return just volatility exposure? Test its dependence."
- "Assess this alpha's correlation to common factors and its decay over time."

## Required Review Themes

- Holding period and turnover, and whether the edge survives cost at that turnover.
- Net-of-cost performance using realistic transaction costs.
- Volatility and factor dependence; an alpha may be a risk premium in disguise.
- Correlation to known alphas; incremental, not redundant.
- Capacity and decay/crowding; the edge at deployable size, over time.
