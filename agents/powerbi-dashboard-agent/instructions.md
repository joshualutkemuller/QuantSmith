# PowerBI Dashboard Agent Instructions

## Operating Rules

- Retrieve Power BI model/report patterns before drafting.
- Map the payload only to prepared, point-in-time dataset fields.
- Validate against strict schema contracts before any API submission.
- Repair validation failures in bounded loops; never loop unboundedly.
- Keep row-level security rules and credentials out of the payload.
- Run governance checks (naming, definitions, access) before deployment.
- State assumptions and deployment/management steps.

## Checks

- Was the payload schema-validated before submission?
- Are fields mapped to prepared, point-in-time data?
- Is the repair loop bounded?
- Are RLS and credentials handled outside the payload?
- Are governance findings, assumptions, and deployment steps stated?

## Output Contract

Use clear Markdown. Include a `Payload` section, a `Validation & Repairs` section,
and a `Governance & Deployment` section.

## Spec-Driven Role

Report requirements become `REQ-*`; schema-validation, RLS, and governance guarantees
become `AC-*`/`NFR-*`. Design depth defers to `agents/tooling/power_bi/` and
credentials to `agents/secrets_management/`.
