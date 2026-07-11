# Incident Postmortem: <short title>

- **Incident ID:**
- **Severity:** SEV1 | SEV2 | SEV3
- **Status:** open | mitigated | resolved
- **Owner:**
- **Date of incident:** YYYY-MM-DD
- **Systems affected:** (data pipeline, model, signal, portfolio, execution, …)

> Blameless. The goal is a fixed root cause and prevention, not fault. Honest
> reporting (constitution P10) and owned, dated action items (P8).

## Summary

What happened, in two or three sentences, and the impact.

## Impact

- Who/what was affected (positions, P&L, downstream consumers, decisions).
- Quantified where possible (magnitude, duration, dollar or model impact).

## Timeline

| Time (UTC) | Event |
| --- | --- |
| … | Detection … |
| … | Mitigation … |
| … | Resolution … |

## Root Cause

The underlying cause, not just the symptom. If still unknown, say so and state
the investigation plan.

## Contributing Factors

- What made the incident more likely or harder to detect/fix.

## Detection

- How it was found. Would monitoring have caught it sooner? If not, why.

## Resolution & Recovery

- How service/behavior was restored, and how correctness was verified.

## Action Items

| # | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| 1 | … | … | YYYY-MM-DD | open |

## Lessons & Prevention

- What changes (spec, monitoring, tests, process) prevent recurrence. Link the
  spec amendments or new `AC-*`/`RISK-*` created.
