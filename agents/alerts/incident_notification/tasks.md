# Incident Notification Tasks

## Write A Notification

Input: a routed alert.

Output: an actionable payload (what broke, impact, owner, evidence, runbook, next step).

## Track A Lifecycle

Input: an active alert.

Output: the lifecycle state (triggered/acknowledged/resolved/closed) with a stable
correlation ID and escalation on non-acknowledgement.

## Send A Recovery Notice

Input: a cleared condition.

Output: a recovery notification closing the incident.

## Capture The Lesson

Input: a resolved incident.

Output: a handoff to `knowledge/institutional_memory` with the cause and fix.
