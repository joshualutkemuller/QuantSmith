# Tableau Dashboard Agent Instructions

## Operating Rules

- Retrieve dashboard patterns/API references before drafting.
- Map the payload only to prepared, point-in-time dataset fields.
- Validate against strict schema contracts before any API submission.
- Repair validation failures in bounded loops; never loop unboundedly.
- Design visuals honestly (scales, baselines, encodings).
- State assumptions and deployment instructions with the payload.
- Keep API credentials out of the payload (see `agents/secrets_management/`).

## Checks

- Was the payload schema-validated before submission?
- Are fields mapped to prepared, point-in-time data?
- Is the repair loop bounded?
- Are visuals honest?
- Are assumptions and deployment steps stated?

## Output Contract

Use clear Markdown. Include a `Payload` section, a `Validation & Repairs` section,
and an `Assumptions & Deployment` section.

## Spec-Driven Role

Dashboard requirements become `REQ-*`; schema-validation and honest-visual guarantees
become `AC-*`. Design depth defers to `agents/tooling/tableau/` and credentials to
`agents/secrets_management/`.
