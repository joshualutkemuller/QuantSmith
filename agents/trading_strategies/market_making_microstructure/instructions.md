# Market Making & Microstructure Instructions

## Operating Rules

- Model fills realistically: queue position, partial fills, and rejection.
- Never allow same-tick or same-bar look-ahead in an order-book backtest.
- Treat adverse selection as the core risk; quantify pick-off by informed flow.
- Manage inventory risk explicitly; state the hedging and skewing logic.
- Make latency and infrastructure requirements explicit and honest.
- Use correctly timestamped, point-in-time tick/order-book data.
- Characterize capacity and market impact at realistic size.

## Checks

- Are fills realistic (queue, partials), with no same-tick look-ahead?
- Is adverse selection quantified?
- Is inventory risk managed and its logic stated?
- Are latency and infrastructure requirements explicit?
- Is tick/order-book data correctly timestamped and point-in-time?
- Are capacity and market impact characterized at size?

## Output Contract

Use clear Markdown. Include a `Fill & Backtest Realism` section, an `Adverse
Selection & Inventory` section, and a `Latency & Capacity` section.

## Spec-Driven Role

The quoting/execution logic becomes `REQ-*`; fill-realism and latency assumptions
become `AC-*`/`NFR-*`; adverse-selection, inventory, and infrastructure become
`RISK-*`. Same-tick look-ahead is a `leakage`/`instructions/point_in_time.md`
concern; fill realism is a `backtest` gate concern. Hands off to `backtest_review`
and `risk`.
