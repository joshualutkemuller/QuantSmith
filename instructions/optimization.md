# Optimization Instructions

## Purpose

Use this standard when designing, reviewing, or operationalizing optimization systems across finance, operations, and technology. The goal is to turn an ambiguous decision into a documented objective, feasible constraints, a solver plan, validation evidence, and production monitoring.

## Required Inputs

- Decision, action space, objective, constraints, and non-goals.
- Variable definitions, units, domains, bounds, and integrality.
- Data sources, refresh cadence, point-in-time availability, and fallback behavior.
- Costs, risk limits, service-level requirements, and business rules.
- Candidate solver class and required optimality/latency tolerance.

## Standards

- Formulate before solving: variables, objective, constraints, units, and signs must be explicit.
- Baseline first: compare against current policy, greedy heuristic, or simple allocation.
- Feasibility is a product feature: document infeasibility handling, relaxations, slacks, and diagnostics.
- Sensitivity matters: expose duals, shadow prices, binding constraints, scenario deltas, and turnover.
- Match solver to structure: LP/QP/MIP/NLP/conic/stochastic/robust/network/DP/simulation must be justified.
- Preserve reproducibility: pinned input snapshot, config, solver version, tolerances, seed, and run card.
- Monitor drift: input distributions, binding constraints, objective contribution, infeasibility, solve time, and realized outcome.

## Common Failure Modes

- Optimizing the wrong proxy objective.
- Hidden constraints living in notebooks, emails, or operator memory.
- Feasible-looking results caused by stale or unavailable data.
- Overfitting to historical scenarios or hand-picked stress cases.
- Solver status ignored or interpreted as optimal when it is only feasible/time-limited.
- No explanation of trade-offs, shadow prices, or why the recommendation changed.

## Spec-Driven Alignment

Optimization work usually deserves a spec because objectives and constraints encode policy. Objectives and action space become `REQ-*`; solve time, reproducibility, and explainability become `NFR-*`; feasibility, optimality, and backtest/simulation evidence become `AC-*`; infeasibility, estimation error, and constraint conflict become `RISK-*`.
