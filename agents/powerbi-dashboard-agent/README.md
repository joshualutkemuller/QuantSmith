# PowerBI Dashboard Agent

## Purpose

The PowerBI Dashboard Agent generates and manages Power BI dashboards and reports
using retrieval-augmented context and strict payload validation. It retrieves model/
report patterns, drafts a schema-aligned payload, validates it, and repairs failures
before API submission, with governance checks.

## Use When

- A Power BI report needs creating, updating, or governance checks.
- A schema-safe API payload must be generated and validated.
- Retrieval-augmented Power BI patterns should guide the design.

## Inputs

- The report request and prepared dataset fields.
- Power BI model/report patterns from the knowledge base.
- Schema contracts and governance rules.

## Outputs

- A structured Power BI payload aligned to dataset fields.
- Schema-validated output (with bounded repair of failures).
- Governance and assumptions notes.
- Deployment/management instructions.

## Example Requests

- "Generate a validated Power BI payload for this dataset."
- "Run governance checks on this report before deployment."
- "Repair this payload's schema-validation failures."

## Required Review Themes

- Payload validated against strict schema contracts before submission.
- Fields mapped to prepared, point-in-time data.
- Bounded correction loops.
- Row-level security and credentials handled outside the payload — see `agents/tooling/power_bi/`.
- Governance, assumptions, and deployment steps stated.
