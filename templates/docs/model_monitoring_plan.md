# Model Monitoring Plan: <model / signal name>

- **Owner:**
- **Spec:** NNNN-short-slug
- **On-call / escalation:**
- **Last updated:** YYYY-MM-DD

> A feature is not done until you can tell whether it is working in production
> (constitution P6). This plan defines what is watched, at what threshold, and
> what happens on a breach.

## What "Healthy" Means

Baselines the live system is measured against (from validation / the spec's NFRs).

## Monitored Metrics

| Metric | Type | Baseline | Warning | Alert | Action on breach |
| --- | --- | --- | --- | --- | --- |
| Prediction/feature drift (PSI or KS) | data | … | e.g. PSI > 0.1 | PSI > 0.25 | investigate / retrain |
| Live vs backtest performance | model | … | … | … | degrade / halt |
| Input coverage / missingness | data | … | … | … | pause / quarantine |
| Latency | ops | … | … | … | page on-call |
| Position/risk limits | risk | … | … | … | reduce / kill switch |

## Drift & Decay

- Drift metric(s) and computation window:
- Performance-decay definition and lookback:
- Regime-change indicators to distinguish decay from noise:

## Retrain / Degrade / Retire Policy

- **Retrain trigger:** …
- **Degrade (reduce size / confidence) trigger:** …
- **Retire trigger:** …
- Who decides, and where the decision is recorded (amend the spec).

## Alerting

- Channels and severities:
- Runbook link:
- Silence/snooze policy (no permanently silenced alerts).

## Review Cadence

- Scheduled health review frequency and owner.
