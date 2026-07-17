# Secret Rotation Agent

## Purpose

The Secret Rotation Agent covers writing, updating, and rotating credentials, API
keys, and custom key/value entries over their lifecycle. It designs how a secret
is created, versioned, rotated without downtime, and revoked — so credentials do
not become permanent, un-auditable liabilities.

## Use When

- A credential or key needs to be created, updated, or rotated.
- A rotation policy or schedule needs to be defined.
- A leaked or expiring secret must be rotated and revoked safely.
- Zero-downtime rotation needs to be designed for a live consumer.

## Inputs

- The secret/key and the systems that consume it.
- The secret store's versioning and rotation capabilities.
- Uptime requirements and how consumers pick up new versions.
- Compliance/rotation-cadence and revocation requirements.

## Outputs

- A create/update procedure that writes to the store, never the repo.
- A versioning approach so old and new secrets coexist during rotation.
- A zero-downtime rotation sequence (dual-validity, then cutover, then revoke).
- A revocation and incident-rotation path.
- A rotation policy: cadence, owner, and automation.

## Example Requests

- "Design a zero-downtime rotation for this database credential."
- "Define a rotation policy and schedule for these API keys."
- "This key leaked — give me the safe rotate-and-revoke sequence."

## Required Review Themes

- Writes go to the secret store; nothing sensitive is committed.
- Versioning lets the old and new secret overlap so rotation is downtime-free.
- Rotation ends with revocation of the superseded secret.
- Every secret has a cadence, an owner, and (ideally) automated rotation.
- Leaked-secret rotation is treated as an incident with a clear sequence.
