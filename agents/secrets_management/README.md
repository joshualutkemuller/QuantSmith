# Secrets Management Agents

This folder groups agents that handle secret keys, credentials, and custom
key/value configuration safely across their lifecycle — storing, reading, writing,
updating, rotating, and detecting leaks.

They exist to enforce constitution P9: **secrets never enter the repository, logs,
or notebook outputs.** Their job is to make the correct handling the easy path,
using a real secret store rather than plaintext files in version control.

## Agents

| Agent | Handles |
| --- | --- |
| `secret_storage/` | Choosing and provisioning a secret store; naming, structure, access policy, encryption at rest. |
| `credential_access/` | Reading/retrieving secrets at runtime safely — env injection, SDK clients, caching, least privilege, no logging. |
| `secret_rotation/` | Writing, updating, and rotating credentials and custom keys/values; versioning, zero-downtime rotation, revocation. |
| `secret_scanning/` | Detecting leaked secrets in code, history, logs, and notebooks; remediation and prevention. |

## Shared Principles

- **Never in the repo.** No plaintext secrets, connection strings, tokens, or keys
  in tracked files, logs, or notebook outputs. `.env` files stay gitignored;
  templates use `.env.example` with placeholder values only.
- **A real store.** Use a secrets manager or vault (HashiCorp Vault, AWS Secrets
  Manager, GCP Secret Manager, Azure Key Vault, or an equivalent). Encrypt at rest
  and in transit.
- **Least privilege.** Grant the narrowest scope and shortest lifetime that works;
  prefer short-lived, dynamically issued credentials over long-lived static ones.
- **Rotatable by design.** Every secret has an owner, a rotation policy, and a
  revocation path. Rotation must not require downtime or code changes.
- **Auditable.** Access and changes are logged (without logging the secret value).
- **No secrets in prompts or transcripts.** These agents describe *how* to handle
  secrets; they never ask for, echo, or embed real secret values.

## Where They Fit

Secrets handling cuts across the lifecycle. It is a Design concern (how the system
authenticates), an Implementation concern (how code reads secrets), a Deployment
concern (how secrets reach production and rotate), and a Maintenance concern
(rotation and leak response). Encode secret-handling requirements as spec `AC-*`
so the P9 check is explicit, not assumed.
