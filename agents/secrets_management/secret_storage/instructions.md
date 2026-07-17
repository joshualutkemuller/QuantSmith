# Secret Storage Instructions

## Operating Rules

- Keep secrets out of the repo, config files, container images, and logs.
- Use a managed secret store; do not roll a custom plaintext or lightly-obscured one.
- Encrypt at rest and in transit; never store base64 and call it encryption.
- Name and structure secrets by environment and service; isolate prod from non-prod.
- Scope access to least privilege; grant to roles/services, not shared humans.
- Give every secret an owner and a documented lifecycle.
- When migrating an exposed secret, rotate it — moving it is not enough.
- Provide `.env.example` with placeholders; keep real `.env` gitignored.

## Checks

- Are any secrets present in tracked files, config, images, or history?
- Is the store managed, with encryption at rest and in transit?
- Does naming separate environments and services cleanly?
- Is access least-privilege and role/service-scoped?
- Does every secret have an owner and a lifecycle?
- Does the migration plan rotate anything that was previously exposed?

## Output Contract

Use clear Markdown. Include a `Store & Structure` section and an `Access Policy`
section. When migrating, include a `Migration & Rotation` section. Never include
real secret values — use placeholders.

## Spec-Driven Role

Storage requirements are spec criteria: "secrets in a managed store", "encrypted
at rest", and "least-privilege access" become `AC-*`/`NFR-*`, making the P9 check
explicit rather than assumed.
