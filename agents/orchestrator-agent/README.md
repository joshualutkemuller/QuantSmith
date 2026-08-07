# Orchestrator Agent

## Purpose

The Orchestrator Agent coordinates multi-agent analytics execution from a
natural-language request. It parses intent, builds a dependency-ordered plan, and
routes subtasks across the analytics-pipeline agents (SQL, data prep, EDA,
dashboards, quality, reporting), tracking status and assembling the result.

## Use When

- A request spans SQL querying, transformation, dashboarding, validation, and reporting.
- Work must be routed across several specialist agents in order.
- Subtask status, retries, and failures need tracking to a final summary.

## Inputs

- The user request and any constraints or output-format requirements.
- The available specialist agents and their input/output contracts.
- Data sources and access context.

## Outputs

- Parsed objectives, constraints, and target output format.
- A dependency-ordered execution plan across specialist agents.
- Per-subtask status, retries, and failure causes.
- A terminal-ready summary of artifacts and next actions.

## Example Requests

- "Turn this analytics request into a routed plan across the pipeline agents."
- "Coordinate SQL → prep → dashboard → QA → report for this question."
- "Report where this pipeline run failed and what to retry."

## Required Review Themes

- Intent parsed into explicit objectives before any routing.
- A correct dependency order across specialist agents.
- Typed input/output contracts on each delegated subtask.
- Honest status: failures and retries surfaced, not hidden.
- A clear final summary of artifacts and next actions.
