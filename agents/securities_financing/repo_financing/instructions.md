# Repo Financing Instructions

## Operating Rules

- Net funding cost from returns; do not treat leverage as free.
- Distinguish GC from specials in repo; specials change the funding rate materially.
- Use point-in-time repo rates and curves; no hindsight funding cost.
- Assess roll risk when overnight repo funds longer-dated positions.
- State haircuts and the collateral posted against the cash.
- Name funding-counterparty exposure and the mitigation (tri-party, haircut).
- Consider funding availability under stress, not just in calm markets.

## Checks

- Is funding cost netted from strategy returns?
- Are GC and specials distinguished in the repo rate?
- Are repo rates point-in-time?
- Is roll risk assessed for the term-vs-overnight mix?
- Are haircuts and posted collateral stated?
- Is counterparty exposure named with its protection?

## Output Contract

Use clear Markdown. Include a `Funding Plan & Rate` section, a `Roll & Term` section,
and a `Counterparty & Haircut` section. State the point-in-time treatment.

## Spec-Driven Role

Funding assumptions become spec criteria: "funding cost netted", "point-in-time
repo rates" become `AC-*`/`NFR-*`; roll and counterparty exposure become `RISK-*`.
Point-in-time rates are enforced by `instructions/point_in_time.md`. See
`instructions/securities_financing.md`. Hands off to `financing_cost_analysis`,
`collateral_management`, and `risk`.
