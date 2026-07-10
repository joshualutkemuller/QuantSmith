# Prompt: Model Monitoring Plan

Use with the Maintenance & Monitoring Agent to define how a live model or signal
is watched.

## Inputs

- The live model/signal and its baselines (from validation / spec NFRs).
- Available metrics, logging, and alerting.
- Retrain, degrade, and retire policies.
- Owner and escalation path.

## Instructions

Fill `templates/docs/model_monitoring_plan.md`. For each monitored metric, give a
baseline, warning and alert thresholds, and a concrete breach action. Define the
drift and decay metrics and how to distinguish decay from noise. Make the
retrain/degrade/retire triggers explicit and name who decides.

## Output

A completed monitoring plan whose alerts map to failure modes that actually
matter, plus any thresholds that need calibration.
