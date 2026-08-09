# Portfolio Management Agents

The Portfolio Management group covers the end-to-end operating model for
managing portfolios: mandate design, universe definition, signal intake,
allocation policy, construction oversight, trade implementation, risk,
compliance, attribution, liquidity, tax, monitoring, and governance.

## Group Workflow

```text
pm_orchestrator -> mandate_objectives -> universe_selection -> data_signal_intake -> allocation_policy -> construction_oversight -> rebalance_trade_implementation -> risk/compliance/performance/monitoring
```

Construction-specific math routes to `agents/optimization/portfolio_construction/`.
Trade scheduling routes to `agents/optimization/execution_optimization/`.

## Agents

| Agent | Handles |
| --- | --- |
| `pm_orchestrator/` | Routes portfolio-management work across mandate, research, allocation, construction, implementation, risk, attribution, and governance specialists. |
| `mandate_objectives/` | Defines portfolio objective, benchmark, horizon, constraints, fiduciary limits, stakeholder approvals, and non-goals. |
| `universe_selection/` | Defines eligible assets, filters, liquidity screens, corporate-action handling, survivorship controls, and coverage gaps. |
| `data_signal_intake/` | Reviews signals, forecasts, risk-model inputs, benchmark data, holdings, prices, and point-in-time readiness. |
| `allocation_policy/` | Designs capital allocation rules, risk budgets, sizing logic, factor tilts, rebalancing bands, and fallback baselines. |
| `construction_oversight/` | Translates policy into optimization-ready objectives, constraints, costs, and diagnostics; hands math to portfolio construction. |
| `rebalance_trade_implementation/` | Converts target weights into trade lists, execution constraints, cash impacts, turnover controls, and rollback notes. |
| `risk_budgeting/` | Reviews factor, sector, issuer, liquidity, leverage, drawdown, stress, and scenario risks against risk budgets. |
| `compliance_constraints/` | Tracks investment guidelines, restricted lists, concentration rules, ESG/client exclusions, approvals, and exception handling. |
| `performance_attribution/` | Decomposes return, risk, cost, timing, sizing, selection, and factor effects after each period or rebalance. |
| `liquidity_cash_management/` | Manages cash buffers, subscriptions/redemptions, liquidity tiers, funding, borrow, income, and forced-trade risk. |
| `tax_transition_management/` | Reviews tax lots, wash-sale constraints, transition trades, legacy positions, realization budgets, and after-tax trade-offs. |
| `monitoring_governance/` | Defines live monitoring, breach triage, model/portfolio review cadence, run cards, ownership, and governance evidence. |

## Inputs

- Current `spec.md`, `plan.md`, `tasks.md`, run card, IPS, or handoff memo.
- Mandate, benchmark, investment universe, constraints, risk budgets, and horizon.
- Forecasts, signals, risk models, holdings, tax lots, cash, prices, and costs.
- Runtime expectations for `src/quantsmith/`, notebooks, dashboards, reports, or
  downstream trading and governance systems.

## Outputs

- Specialist routing plan and PM lifecycle stage classification.
- Spec-ready requirements, risks, acceptance criteria, task suggestions, and
  monitoring hooks.
- Review findings on point-in-time data, feasibility, costs, constraints,
  compliance, risk, attribution, and governance.
- Handoffs to optimization, risk, backtest review, data quality, testing,
  reporting, deployment, and monitoring agents.

## Rules

- Do not let an attractive model output bypass mandate, risk, compliance, cost,
  liquidity, or governance review.
- Treat target weights, trade lists, and live portfolio mutations as controlled
  outputs that require an approved spec and rollback path.
- Keep each specialist narrow; broad portfolio changes should become a spec before
  implementation.
- Use `instructions/portfolio_management.md` as the shared standard for all agents
  in this group.
