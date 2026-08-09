# Spec: Alerting (policy evaluation + routing)

- **ID:** 0020-alerting
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> The alerting engine for the `alerts/*` agents: evaluate policies into alerts, then
> route them. Delivery is the `adapters/alert_delivery/` contract's job.

## Problem & Context

QuantSmith detects problems (`pipeline_observability` `0019`, `signal_monitoring`
`0021`, and other monitors) but had no engine to turn those observations into
actionable, routed notifications — so alerting was ad hoc, noisy, and vendor-coupled.
This spec adds the alerting engine: evaluate alert policies (threshold and missing-data
rules) into alerts with a severity and a dedup key, then route them — deduplicate,
suppress muted rules, assign an owner and channel, and escalate high-severity alerts —
without coupling to any delivery vendor.

## Goals

- Evaluate alert policies against observations into alerts with severity and dedup keys.
- Route alerts: deduplicate, suppress muted rules, assign owner and channel by
  severity, and escalate high-severity alerts.
- Keep detection separate from delivery; produce routed payloads the
  `adapters/alert_delivery/` providers deliver.
- Carry the shared alert contract and redact secrets.

## Non-Goals

- Delivering the notifications (owned by `adapters/alert_delivery/`).
- Detecting the problems (owned by the monitoring runtimes, `0019`/`0021`).
- Automated remediation — notification never mutates a portfolio, job, or model.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Evaluate alert policies (threshold `max`/`min` and missing-data) against observations, firing an alert with a severity and a dedup key per breach. | must |
| REQ-002 | Route alerts: deduplicate by key (keeping the highest severity, with a count), suppress muted rules, assign an owner and a severity-based channel, and escalate high-severity alerts. | must |
| REQ-003 | Keep detection separate from delivery — routing produces payloads for the `adapters/alert_delivery/` providers and never mutates portfolios, jobs, or models. | must |
| REQ-004 | Alerts carry the shared alert contract fields and contain no secrets/PII. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same policies and observations yield identical alerts and routing. |
| NFR-002 | No false silence | A real breach always fires unless a rule is explicitly suppressed. |
| NFR-003 | Redaction | Alert payloads contain no credential-shaped content. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given policies and observations, when evaluated, then a threshold breach and a missing metric fire alerts, and within-threshold present metrics do not. | REQ-001, NFR-002 |
| AC-002 | Given duplicate breaches, when routed, then they collapse to one alert with a count; a suppressed rule is dropped. | REQ-002 |
| AC-003 | Given routing, when alerts are routed, then each carries an owner and a severity-based channel, and a critical alert is escalated. | REQ-002, REQ-003 |
| AC-004 | Given any alert, when inspected, then it carries no secret-shaped content. | REQ-004, NFR-003 |
| AC-005 | Given the same inputs, when evaluated and routed twice, then the results are identical. | NFR-001 |

## Data & Dependencies

- Input: `AlertPolicy` rules and `Observation`s (from the monitoring runtimes,
  `0019`/`0021`).
- Standard: `instructions/alerting.md`; delivery via `adapters/alert_delivery/`.
- Agents: `alerts/alert_policy`, `alerts/alert_router`, `alerts/incident_notification`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Alert fatigue from noise. | Real alerts ignored. | Dedup, suppression, and severity routing (AC-002). |
| RISK-002 | A real breach is missed. | Silent failure. | A breach always fires unless explicitly suppressed (NFR-002). |
| RISK-003 | Vendor coupling. | Rework to switch channels. | Detection separate from delivery; channels are adapters (REQ-003). |
| RISK-004 | Secrets leak in a payload. | Credential exposure. | Redaction; no credential-shaped content (NFR-003). |

## Assumptions & Open Questions

- Assumption: observations are already computed by a monitor; this engine decides
  policy and routing.
- Open question: add anomaly (z-score) and composite (AND/OR) policy kinds and a
  stateful acknowledgement lifecycle (tracked, not deferred silently).

## Exceptions

None.
