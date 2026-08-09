# Spec: Model/signal monitoring

- **ID:** 0021-signal-monitoring
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> The model/signal monitoring node: detect drift, calibration error, alpha decay, and
> regime shift, and emit observations the alerting engine (`0020`) evaluates.

## Problem & Context

A model or signal that was correct at launch degrades — data drifts, alpha decays,
regimes change — but QuantSmith had no runtime to detect that and hand a clean signal
to alerting. This spec adds model/signal monitoring: compute drift, calibration error,
alpha decay (information-coefficient drop), and a volatility-regime shift from a
reference vs a live sample, flag breaches against thresholds, and emit the measured
values as observations the alerting engine turns into routed notifications. It
generalizes the ad-hoc `monitor` in `return_forecasting` (`0006`).

## Goals

- Compute signal health — drift, calibration, decay, regime shift — from reference vs
  live samples.
- Flag breaches against thresholds and report an honest healthy/degraded verdict.
- Emit observations the alerting engine (`0020`) evaluates, so detection and
  notification stay separate.

## Non-Goals

- Notification, routing, or delivery (owned by `0020` and `adapters/alert_delivery/`).
- Pipeline/data freshness monitoring (owned by `pipeline_observability` `0019`).
- Retraining or remediation (a separately approved runbook decision).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Compute signal health from a reference vs a live sample: distribution drift, calibration error, alpha decay (baseline IC − live IC), and a volatility-regime shift. | must |
| REQ-002 | Flag each check that exceeds its threshold and report a healthy/degraded verdict; a degraded signal is never reported healthy. | must |
| REQ-003 | Emit the measured values as observations the alerting engine (`0020`) can evaluate. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same samples and thresholds yield an identical health report. |
| NFR-002 | Honest reporting | Any check over its threshold makes the signal degraded. |
| NFR-003 | Separation | Monitoring emits observations; it does not page, route, or remediate. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given reference and live samples, when monitored, then drift, calibration, decay, and regime shift are computed. | REQ-001 |
| AC-002 | Given a shifted/decayed live sample, when monitored, then the breaching checks appear in the report and the verdict is degraded. | REQ-002, NFR-002 |
| AC-003 | Given a health report, when its observations are passed to the alerting engine, then the corresponding policies fire. | REQ-003, NFR-003 |
| AC-004 | Given a volatility change, when monitored, then the regime shift is detected against its threshold. | REQ-001, REQ-002 |
| AC-005 | Given the same inputs, when monitored twice, then the reports are identical. | NFR-001 |

## Data & Dependencies

- Input: reference and live value samples, a baseline and live information coefficient,
  and optional thresholds.
- Standard: `instructions/monitoring.md`; hands off to `instructions/alerting.md` and
  the `alerts/*` agents.
- Agents: `monitoring/model_signal_monitoring` (and `pipeline_monitoring`,
  `infrastructure_cost_monitoring`).
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Degradation missed. | Bad decisions on a stale model. | Explicit thresholds and honest breaches (AC-002). |
| RISK-002 | Accuracy-only view. | An uneconomic "healthy" model. | Cover turnover/capacity/cost via added metrics (standard). |
| RISK-003 | Monitoring pages directly. | Coupled, noisy alerts. | Emit observations; alerting decides severity/routing (NFR-003). |
| RISK-004 | Look-ahead in the reference. | False stability. | Point-in-time reference window (standard). |

## Assumptions & Open Questions

- Assumption: the reference is a valid, point-in-time baseline (e.g. a training window).
- Open question: add per-feature drift, turnover/capacity decay, and a cost-monitoring
  runtime (tracked, not deferred silently).

## Exceptions

None.
