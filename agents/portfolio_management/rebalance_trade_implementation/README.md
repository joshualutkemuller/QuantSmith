# Rebalance Trade Implementation

## Purpose

Converts target weights into trade lists, execution constraints, cash impacts,
turnover controls, operational checks, and rollback notes.

## Use When

- A target portfolio must become implementable orders or a trade file.
- A rebalance plan needs review for turnover, cash, market impact, and operations.

## Inputs

- Target weights, current holdings, prices, cash, lots, execution constraints,
  liquidity, costs, restricted lists, settlement rules, and approval state.

## Outputs

- Rebalance plan, trade list requirements, cash impact, execution handoff,
  operational checks, risks, and rollback plan.

## Required Review Themes

- Turnover, liquidity, market impact, cash, settlement, lot selection, short/borrow,
  compliance, execution windows, and rollback.
