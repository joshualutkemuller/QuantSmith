# Prompt: Incident Postmortem

Use with the Maintenance & Monitoring Agent to write a blameless postmortem for a
data or model incident.

## Inputs

- What happened and the timeline of detection, mitigation, and resolution.
- Systems and decisions affected, quantified where possible.
- What is known about the cause.

## Instructions

Fill `templates/docs/incident_postmortem.md`. Stay blameless. Chase the root
cause, not the symptom; if it is still unknown, say so and give the investigation
plan. Every action item has an owner and a due date (constitution P8, P10). Link
the spec amendments, tests, or `RISK-*` entries that prevent recurrence.

## Output

A completed postmortem with a clear root cause (or investigation plan) and owned,
dated action items.
