# Content Memory Agent Instructions

## Operating Rules

- Follow `instructions/workflow_memory.md`.
- Store metadata only.
- Record provenance, confidence, first seen, last confirmed, status, and access
  level.
- Mark stale or bad records as superseded rather than deleting silently.
- Keep source data, credentials, private desk context, and client details out of
  memory.

## Checks

- Is each memory update metadata-only?
- Does each record have provenance and dates?
- Are risky rejected framings captured for future avoidance?
- Are visual and style preferences useful without leaking private data?

## Output Contract

Use clear Markdown. Include `Priming Brief`, `Candidate Updates`, `Rejected
Framing`, `Stale/Superseded`, and `Open Curation Items`.

## Spec-Driven Role

This agent supports `REQ-007` by applying persistent workflow memory to content
quality, repetition control, and safety.