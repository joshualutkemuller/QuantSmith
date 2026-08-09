# Allocation Policy

## Purpose

Designs capital allocation rules, risk budgets, sizing logic, factor tilts,
rebalancing bands, and fallback baselines before construction.

## Use When

- A portfolio needs policy-level sizing logic before optimization.
- Research signals must be translated into risk budgets or sleeve allocations.

## Inputs

- Mandate, universe, forecasts, risk model, benchmark, current holdings, cash,
  liquidity, costs, risk budgets, and constraints.

## Outputs

- Allocation policy, baseline, sizing rules, risk budgets, rebalance triggers,
  assumptions, risks, and construction handoff.

## Required Review Themes

- Objective alignment, risk budget, capacity, concentration, factor exposure,
  turnover, drift bands, and fallback behavior.
