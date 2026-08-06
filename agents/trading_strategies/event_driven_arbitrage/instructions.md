# Event-Driven & Arbitrage Instructions

## Operating Rules

- Date events point-in-time; use only information public as of the decision.
- Characterize deal/event-failure risk; it is the left tail of the payoff.
- Respect small samples; report how few events drive the result and their dispersion.
- Model fat tails rather than assuming normal event returns.
- Assess crowding in well-known, calendar-driven events (index rebalances, earnings).
- Include borrow, financing, and costs around the event window.
- Watch for survivorship in the event universe (only completed deals, etc.).

## Checks

- Are event dates point-in-time, with no hindsight in the universe?
- Is deal/event-failure (left-tail) risk characterized?
- Is the sample size adequate, and are results robust to a few events?
- Are fat tails modeled rather than assumed away?
- Is crowding in known events considered?
- Are borrow, financing, and costs included around the event?

## Output Contract

Use clear Markdown. Include an `Event Definition & PIT` section, a `Deal/Event Risk`
section, and a `Sample & Crowding` section. Note borrow and cost treatment.

## Spec-Driven Role

Event definitions become `REQ-*`; point-in-time dating and net-edge thresholds
become `AC-*`/`NFR-*`; deal-break, small-sample, and crowding become `RISK-*`.
PIT event dating is enforced by `instructions/point_in_time.md`; sample adequacy by
the `backtest` gate. See `instructions/trading_strategies.md` for the shared
standard. Hands off to `backtest_review` and `risk`.
