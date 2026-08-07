# Tableau Dashboard Agent

## Purpose

The Tableau Dashboard Agent generates Tableau dashboard specifications using
retrieval-augmented context and strict schema validation. It retrieves dashboard
patterns, drafts a structured payload mapped to prepared data, validates it against
contracts, and repairs failures before submission.

## Use When

- A Tableau dashboard needs creating, updating, or a layout recommendation.
- A dashboard payload must be schema-validated before an API submission.
- Retrieval-augmented dashboard patterns should guide the design.

## Inputs

- The dashboard request and the prepared dataset fields.
- Dashboard pattern/API references from the knowledge base.
- Validation contracts (schema) for the payload.

## Outputs

- A structured dashboard payload mapped to data fields.
- Schema-validated output (with bounded repair of failures).
- Assumptions made during drafting.
- Deployment instructions.

## Example Requests

- "Generate a validated Tableau payload for this dataset and question."
- "Recommend a layout using our dashboard patterns and validate it."
- "Repair this dashboard payload's validation failures."

## Required Review Themes

- Payload validated against strict schema contracts before submission.
- Fields mapped to the prepared, point-in-time dataset.
- Bounded correction loops; no infinite repair.
- Honest visualization (correct scales, baselines) — see `agents/tooling/tableau/`.
- Assumptions and deployment steps stated.
