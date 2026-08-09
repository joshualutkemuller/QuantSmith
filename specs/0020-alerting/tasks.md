# Tasks: Alerting (policy evaluation + routing)

- **Spec:** 0020-alerting (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; tests exist and pass deterministically.
- A breach always fires unless a rule is explicitly suppressed.
- Payloads carry the shared contract and no secrets; no delivery or remediation here.
- No secrets or private data; runtime code lives under `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `AlertPolicy`/`Observation`/`Alert` and `evaluate_policies`. | REQ-001, REQ-004, NFR-001, NFR-002, NFR-003 | done | `alert_policy` | threshold + missing kinds; severity + dedup key. |
| T-002 | Implement `Routing`/`RoutedAlert` and `route` (dedup/suppress/assign/escalate). | REQ-002, REQ-003, NFR-001 | done | `alert_router` | Highest-severity dedup + count; owner/channel; escalation. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtime: `src/quantsmith/pipelines/alerting.py`. Delivery is the
`adapters/alert_delivery/` contract; `alerts/incident_notification` owns the lifecycle.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_alerting.py::test_policy_evaluation_AC_001` | done |
| AC-002 | `tests/test_alerting.py::test_dedup_and_suppression_AC_002` | done |
| AC-003 | `tests/test_alerting.py::test_routing_assignment_AC_003` | done |
| AC-004 | `tests/test_alerting.py::test_no_secrets_AC_004` | done |
| AC-005 | `tests/test_alerting.py::test_deterministic_AC_005` | done |

## Follow-ups

- Add anomaly (z-score) and composite (AND/OR) policy kinds, cooldown/market-calendar
  suppression windows, and a stateful acknowledgement lifecycle.
- Executable provider implementations behind `adapters/alert_delivery/`.
