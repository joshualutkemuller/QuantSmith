# Trading Strategies Instructions

## Purpose

Use this instruction set when designing or reviewing a trading strategy of any
archetype. It is the shared standard behind the `agents/trading_strategies/` group,
which operationalizes the strategy families in *151 Trading Strategies*
(Kakushadze & Serur). The goal is a strategy whose edge is economically grounded,
leakage-free, cost-aware, and robust — before any capital is at risk.

## Required Inputs

- The strategy archetype and its economic rationale.
- Universe and asset class, with point-in-time membership.
- Signal definition, decision frequency, and holding logic.
- Cost, borrow/financing, turnover, and capacity constraints.
- Risk, leverage, and drawdown limits.

## Expected Output

- A strategy specification with a stated edge.
- A leakage and point-in-time review.
- A cost-, capacity-, and turnover-aware net-edge view.
- A robustness and overfitting assessment.
- A risk characterization (exposures, tails, crowding, regime dependence).

## Standards

- **Rationale before backtest.** State why the edge should exist and persist; a
  pattern without a mechanism is a coincidence until proven otherwise.
- **Point-in-time and leakage-free.** Signals use only information available at the
  decision time; universes and fundamentals are point-in-time. See
  `instructions/point_in_time.md`.
- **Net of costs.** Include transaction costs, slippage, borrow/financing, and
  turnover; report the edge after them, not before.
- **Capacity-aware.** State the size at which the edge decays; capacity is part of
  the result, not a footnote.
- **Overfitting discipline.** Record the number of configurations tried and correct
  for multiple testing; prefer robustness across parameters to a single tuned point.
- **Risk-characterized.** Examine exposures, tail behavior, crowding, and regime
  dependence for every strategy. See `instructions/backtesting.md`.

## Checks

- Is there an economic rationale, not just a fitted pattern?
- Is the strategy point-in-time and free of look-ahead/leakage?
- Does a real edge survive realistic costs, borrow, and turnover?
- Is capacity stated, with the size at which the edge decays?
- Is performance robust across parameters, and is multiple testing controlled?
- Are exposures, tails, crowding, and regime dependence characterized?

## Common Failure Modes

- A backtested pattern with no economic mechanism behind it.
- Look-ahead through restated data, universe survivorship, or signal timing.
- Reporting gross returns while costs, borrow, or turnover erase the edge.
- Ignoring capacity; an edge that vanishes at deployable size.
- Overfitting via undocumented parameter search and no multiple-testing control.
- Presenting a smooth average that hides a short-volatility or event tail.

## Spec-Driven Alignment

This standard backs the `agents/trading_strategies/` group across the Research and
Testing stages. The strategy definition becomes `REQ-*`; economic-rationale,
net-of-cost, capacity, and robustness thresholds become `AC-*`/`NFR-*`; tail,
crowding, and regime risks become `RISK-*`. Point-in-time and leakage are enforced
by `instructions/point_in_time.md` and the `leakage` gate; cost, out-of-sample, and
multiple-testing by the `backtest` gate (constitution P3, P4). Strategy agents hand
off to `research_analyst`, `feature_engineering`, `modeling`, `backtest_review`, and
`risk`.
