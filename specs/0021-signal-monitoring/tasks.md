# Tasks: Model/signal monitoring

- **Spec:** 0021-signal-monitoring (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; tests exist and pass deterministically.
- A degraded signal is reported degraded (no false healthy).
- Monitoring emits observations; it does not page, route, or remediate.
- No secrets or private data; runtime code lives under `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement drift/calibration/decay/regime computation (`monitor_signal`, helpers). | REQ-001, NFR-001 | done | `model_signal_monitoring` | Reference vs live. |
| T-002 | Implement threshold breaches and the `healthy`/degraded verdict. | REQ-002, NFR-002 | done | `model_signal_monitoring` | `MonitorThresholds`, breaches list. |
| T-003 | Implement `observations()` feeding the alerting engine. | REQ-003, NFR-003 | done | `model_signal_monitoring` | Values as `Observation`s for `0020`. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtime: `src/quantsmith/pipelines/signal_monitoring.py`. Pipeline/data monitoring is
`pipeline_observability` (`0019`); alerting is `0020`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_signal_monitoring.py::test_health_metrics_AC_001` | done |
| AC-002 | `tests/test_signal_monitoring.py::test_breaches_flagged_AC_002` | done |
| AC-003 | `tests/test_signal_monitoring.py::test_feeds_alerting_AC_003` | done |
| AC-004 | `tests/test_signal_monitoring.py::test_regime_shift_AC_004` | done |
| AC-005 | `tests/test_signal_monitoring.py::test_deterministic_AC_005` | done |

## Follow-ups

- Per-feature drift, turnover/capacity decay, and a full PSI/KS drift test.
- A dedicated infrastructure-cost monitoring runtime for the
  `infrastructure_cost_monitoring` agent.
