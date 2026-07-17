# Secret Rotation Instructions

## Operating Rules

- Write and update secrets in the managed store; never in the repo or config.
- Version secrets so a new value can coexist with the old during rotation.
- Rotate without downtime: issue new, propagate, cut over, then revoke old.
- Always revoke the superseded secret; a rotation without revocation is half done.
- Give every secret a rotation cadence and an owner; automate where possible.
- On a suspected leak, rotate immediately, revoke, and open an incident record.
- Never print or embed the secret value in procedures or logs.

## Checks

- Do all writes/updates target the store, with nothing committed?
- Does versioning allow old/new overlap for a clean cutover?
- Is the superseded secret revoked at the end?
- Is there a cadence and an owner, ideally automated?
- Is there a defined leaked-secret rotate-revoke-record path?

## Output Contract

Use clear Markdown. Describe rotation as an ordered sequence. Include a `Rotation
Policy` section (cadence, owner) and a `Revocation` step. For a leak, include an
`Incident Rotation` sequence. Never include real secret values.

## Spec-Driven Role

Rotation guarantees are spec criteria: "zero-downtime rotation", "old secret
revoked", and "rotation cadence defined" become `AC-*`/`NFR-*`. A leaked-secret
rotation links to an incident postmortem (`templates/docs/incident_postmortem.md`).
