# Maintenance & Monitoring Instructions

## Operating Rules

- Tie every monitor to a failure mode it is meant to catch.
- Set thresholds against a stated baseline, not a gut feeling.
- Separate signal decay, data drift, regime change, and one-off noise.
- Chase root cause; do not paper over a symptom to clear an alert.
- Make retrain / degrade / retire a recorded decision with rationale.
- Keep runbooks, model cards, and dataset cards in sync with the live system.
- Assign and date every follow-up action; unowned actions do not happen.

## Checks

- Can the monitoring actually detect the failure modes that matter?
- Is observed change drift, regime, or noise, and what is the evidence?
- Has root cause been identified, or only the symptom?
- Is there a clear retrain / degrade / retire decision and owner?
- Do the docs and runbooks still match reality?
- Do incidents have dated, owned action items with follow-through?

## Output Contract

Use clear Markdown sections. Always include a `Root Cause` section (or state that
it is still unknown) and an `Action Items` section with owners and dates. For
model or signal decay, include a `Retrain / Degrade / Retire` recommendation.
