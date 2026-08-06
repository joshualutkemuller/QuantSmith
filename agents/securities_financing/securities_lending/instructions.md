# Securities Lending Instructions

## Operating Rules

- Net the borrow fee and short rebate from short returns; never assume a free short.
- Distinguish general collateral from specials; specials can dwarf the alpha.
- Use point-in-time borrow rates and hard-to-borrow status, not today's values.
- Treat recall risk as a constraint: a recalled borrow can force a buy-in.
- Handle corporate actions on loaned stock: manufactured dividends and lost votes.
- Respect locate/close-out rules (e.g. Reg SHO) where they apply.
- Reflect availability in capacity; hard-to-borrow names cap short size.

## Checks

- Is the borrow fee/rebate netted from short returns?
- Are GC and specials distinguished, with specials costed correctly?
- Are borrow rates and HTB status point-in-time, not hindsight?
- Are recall and buy-in risks characterized?
- Are corporate actions on loaned stock handled?
- Is short capacity limited by borrow availability?

## Output Contract

Use clear Markdown. Include a `Borrow Cost & Availability` section and a `Recall &
Buy-In Risk` section. State the point-in-time treatment of borrow data.

## Spec-Driven Role

Borrow assumptions become spec criteria: "borrow cost netted", "point-in-time borrow
rates", and "capacity reflects availability" become `AC-*`/`NFR-*`; recall, buy-in,
and specials risk become `RISK-*`. Point-in-time borrow data is enforced by
`instructions/point_in_time.md`; short-cost realism by the `backtest` gate's
financing theme. See `instructions/securities_financing.md`. Hands off to
`financing_cost_analysis`, `backtest_review`, and `risk`.
