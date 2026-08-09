# Equities Market Mechanics Tasks

## Market-Structure Brief

Input: the instrument(s), venue(s), and date range.

Output: venue/session structure, tick/lot size, and settlement-lag brief.

## Corporate-Action & Adjustment Review

Input: a raw or adjusted price/volume series.

Output: the adjustment method used and its look-ahead risk, with a corrected
series if the adjustment is wrong or unstated.

## Point-in-Time Universe Review

Input: an index or custom universe definition.

Output: a point-in-time membership treatment with reconstitution dates, free of
survivorship.

## Short-Sale Mechanics Scoping

Input: a strategy or backtest that shorts equities.

Output: locate, Reg SHO, and hard-to-borrow flags scoped for handoff to
`securities_financing/securities_lending`.
