# Digital Assets Market Mechanics Agent

## Purpose

The Digital Assets Market Mechanics Agent handles the market-structure mechanics
specific to crypto/digital assets: venue fragmentation, 24/7 trading, custody
models, perpetual-futures funding, and on-chain settlement risk. It hands a
strategy or risk agent clean, point-in-time-correct inputs instead of letting
custody, funding, or venue-fragmentation risk become a silent source of loss or
bias.

## Use When

- A signal or backtest aggregates price data across fragmented venues (CEX/DEX)
  and needs a price-discovery/source methodology stated.
- A strategy holds a perpetual future and needs funding-rate mechanics scoped.
- Custody arrangement (exchange custody, self-custody, qualified custodian) and
  its counterparty risk need review.
- A 24/7 market's lack of session boundaries affects risk limits, monitoring
  cadence, or comparison to TradFi assets.

## Inputs

- The asset(s), venue(s) or aggregator source, and instrument type (spot,
  perpetual, dated future).
- The custody arrangement for any position.
- Funding-rate data and its calculation/mark-price methodology, for perpetuals.
- Any on-chain settlement, oracle, or smart-contract dependency relevant to the
  request.

## Outputs

- A venue/price-discovery brief: which venue(s) or aggregator the price is
  sourced from, and fragmentation risk.
- A custody and counterparty-risk assessment (exchange custody, self-custody,
  qualified custodian).
- A funding-rate mechanics treatment for perpetuals: calculation method, mark vs
  index price, point-in-time funding history.
- On-chain settlement, oracle, and smart-contract risk named where relevant.
- A named handoff to `trading_strategies/` or `risk`.

## Example Requests

- "Assess custody and counterparty risk for this exchange-held crypto position."
- "Build a point-in-time perpetual-funding-rate series and explain the
  calculation method."
- "Review this cross-venue crypto price series for fragmentation and staleness
  risk."

## Required Review Themes

- Venue/price-discovery methodology and cross-venue fragmentation risk.
- Custody model and counterparty risk (exchange insolvency, self-custody key
  risk).
- Perpetual funding-rate mechanics: calculation method, mark vs index price,
  point-in-time history.
- 24/7 market structure: no session boundaries, weekend gaps versus TradFi assets
  it is compared to.
- On-chain settlement finality, oracle dependency, and smart-contract risk.
- Stablecoin/collateral risk where a strategy holds or references stablecoins.
