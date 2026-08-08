# Spec: Optimal execution scheduling

- **ID:** 0012-execution-scheduling
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Second optimization runtime workflow (after `0007-portfolio-construction`), routing
> the `optimization/execution_optimization` agent. Continues the quant chain:
> signal → forecast → portfolio → **execution**.

## Problem & Context

Spec `0007` produces a target portfolio, but trading into it naively — all at once,
or blindly uniform — either pays too much market impact or carries too much price risk
while the order works. There is no disciplined way to schedule the trade. This spec
defines optimal execution: given a position to liquidate over a fixed horizon, the
impact and volatility parameters, and a risk aversion, compute the trade schedule that
trades expected implementation-shortfall cost against the variance of that cost
(the Almgren-Chriss framework).

## Goals

- A trade schedule (per-period holdings and trades) that fully liquidates a position
  over a fixed horizon.
- A tunable cost/risk trade-off: risk-neutral gives uniform (TWAP) execution; risk
  aversion front-loads to reduce exposure.
- Reported expected cost and cost variance so the trade-off is explicit, not hidden.

## Non-Goals

- Real-time/adaptive execution, limit-order placement, or venue routing (a later
  microstructure slice; this is the schedule, not the order type).
- Nonlinear or transient impact models beyond the linear Almgren-Chriss form.
- Multi-asset joint execution (single-name liquidation in this slice).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall compute an execution schedule (per-period holdings and trades) over N periods for a total position, given temporary/permanent impact and volatility. | must |
| REQ-002 | The schedule shall fully liquidate the position: trades sum to the total and the terminal holding is zero. | must |
| REQ-003 | With zero risk aversion the schedule shall reduce to uniform (TWAP); with positive risk aversion it shall front-load trading. | must |
| REQ-004 | The system shall report the expected implementation-shortfall cost and its variance, and risk aversion shall trade cost against variance. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same inputs yield an identical schedule on every run. |
| NFR-002 | Feasibility by construction | Holdings are monotone non-increasing from the full size to zero and non-negative; a pure liquidation never buys. |
| NFR-003 | Honest reporting | Both expected cost and cost variance are reported — never cost alone. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a position and N periods, when a schedule is computed, then it has N trades and N+1 holdings running from the full size to zero. | REQ-001 |
| AC-002 | Given a schedule, when the trades are summed, then they equal the total and the terminal holding is zero. | REQ-002 |
| AC-003 | Given zero risk aversion, then all trades are equal (TWAP); given positive risk aversion, then the first trade exceeds the last (front-loaded). | REQ-003 |
| AC-004 | Given two risk-aversion levels, when schedules are computed, then the more risk-averse one has lower cost variance and higher expected cost. | REQ-004, NFR-003 |
| AC-005 | Given a liquidation schedule, when holdings are inspected, then they are monotone non-increasing and non-negative and no trade is negative. | NFR-002 |
| AC-006 | Given the same inputs, when a schedule is computed twice, then the schedules are identical. | NFR-001 |

## Data & Dependencies

- The target trade from `0007-portfolio-construction` (position size to execute).
- Market-impact parameters (temporary `eta`, permanent `gamma`) and volatility
  `sigma`, as-of the execution window.
- Standard: `instructions/backtesting.md` (cost assumptions) and the
  `optimization/execution_optimization` agent.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Trading too fast pays excessive market impact. | Cost drag erodes the alpha. | Cost term penalizes fast trading; risk aversion tunes the pace (REQ-004). |
| RISK-002 | Trading too slowly carries price risk while the order works. | High variance of realized cost. | Variance term and front-loading under risk aversion (AC-003, AC-004). |
| RISK-003 | An infeasible schedule (over/under-fills). | Wrong position after execution. | Full-liquidation guarantee by construction (AC-002 / NFR-002). |
| RISK-004 | Reporting cost without variance hides the risk taken. | Misleading comparison of schedules. | Report both cost and variance (NFR-003). |

## Assumptions & Open Questions

- Assumption: linear temporary and permanent impact; `eta - 0.5*gamma*tau > 0`.
- Assumption: constant volatility over the execution window; a single name.
- Open question: extend to multi-asset joint execution and adaptive schedules
  (tracked, not silently deferred).

## Exceptions

None.
