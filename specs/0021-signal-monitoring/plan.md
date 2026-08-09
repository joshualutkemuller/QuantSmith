# Plan: Model/signal monitoring

- **Spec:** 0021-signal-monitoring (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

A single pure function, `monitor_signal`, that computes four health checks from a
reference vs a live sample and flags breaches against thresholds. Honesty holds by
construction (any check over threshold makes the signal degraded), and separation
holds because it returns measured values as `Observation`s that the alerting engine
(`0020`) evaluates — monitoring never pages. Pure Python, deterministic.

## Agent Routing

```text
model/signal (live vs reference) -> monitoring/model_signal_monitoring [monitor_signal]
  -> observations -> alerts/alert_policy (0020) -> alert_router -> delivery
```

## Architecture & Components

- `MonitorThresholds` — drift, calibration, decay, regime thresholds.
- `SignalHealth` — the four measured values, a breaches list, a `healthy` property, and
  `observations()` (the values as `Observation`s for alerting).
- `monitor_signal(reference, live, baseline_ic, live_ic, thresholds)` — computes drift
  (population shift), calibration (mean shift), decay (IC drop), and regime shift (vol
  ratio), and assembles the report.

## Interfaces & Data Contracts

- Input: reference/live samples, baseline/live IC, optional thresholds.
- Output: `SignalHealth`; `observations()` yields `Observation("drift"|"calibration"|
  "decay"|"regime_shift", value)` for the alerting engine.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Pure computation; deterministic; thresholded breaches. |
| P5 Reversibility | yes | Read-only analysis. |
| P6 Observability | yes | This is a monitoring surface; emits measured values + breaches. |
| P9 Security & data | yes | No secrets or private data. |
| P10 Honest reporting | yes | Degraded on any threshold breach; no false healthy. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | drift/calibration/decay/regime computation | T-001 |
| REQ-002 | threshold breaches + `healthy` verdict | T-002 |
| REQ-003 | `observations()` for alerting | T-003 |
| NFR-001 | deterministic helpers | T-001 |
| NFR-002 | degraded on any breach | T-002 |
| NFR-003 | emits observations, does not page | T-003 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Drift metric | Mean+spread population proxy | Full PSI/KS with binning | A dependency-free proxy is enough for a reference; PSI/KS is a follow-up. |
| Decay | Baseline IC − live IC | Rolling Sharpe | IC drop is the direct alpha-decay signal for a cross-sectional signal. |
| Output | Observations for alerting | Fire alerts directly | Keeps detection and notification separate (NFR-003). |
| Scope | Model/signal plane | Also pipeline/cost here | Pipeline is `0019`; cost is a declared-metric follow-up. |

## Validation Strategy

- AC-001: assert the four metrics are computed.
- AC-002: assert breaches and a degraded verdict on a shifted/decayed sample.
- AC-003: feed `observations()` to `evaluate_policies`; assert the policies fire.
- AC-004: assert regime shift on a volatility change.
- AC-005: monitor twice; assert identical.

## Rollout, Observability & Rollback

A read-only library consumed by the monitoring agent; its observations hand off to
alerting. Nothing to roll back; a changed reference/threshold changes the verdict.

## Open Questions

- Per-feature drift, turnover/capacity decay, and a dedicated infrastructure-cost
  monitoring runtime.
