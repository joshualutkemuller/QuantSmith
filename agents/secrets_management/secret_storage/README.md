# Secret Storage Agent

## Purpose

The Secret Storage Agent helps choose, provision, and structure a secret store for
credentials, API keys, and custom key/value configuration. It covers where secrets
live, how they are named and organized, who can access them, and how they are
encrypted — so the workflow never depends on plaintext in the repo.

## Use When

- A project needs a place to keep credentials and keys that is not the repo.
- A secret store needs a naming convention, structure, and access policy.
- Secrets are currently in `.env` files, config, or code and must be moved out.
- Encryption-at-rest and access-scope decisions need review.

## Inputs

- The secrets and custom keys/values to store, and who/what consumes them.
- Available secret stores (Vault, AWS/GCP/Azure managers, or an equivalent).
- Environments (dev/staging/prod) and their isolation requirements.
- Access, compliance, and audit constraints.

## Outputs

- A recommended secret store and rationale.
- A naming and structure convention (per environment, per service).
- An access policy scoped to least privilege.
- Encryption-at-rest and in-transit settings.
- A migration plan for secrets currently in the repo or config.

## Example Requests

- "Design the secret store layout and naming for these services and environments."
- "Move these `.env` secrets into a secrets manager with least-privilege access."
- "Review this secret storage setup for scope, encryption, and separation."

## Required Review Themes

- No plaintext secrets in the repo, config, or images; `.env` gitignored.
- A managed store with encryption at rest and in transit.
- Naming/structure that separates environments and services.
- Least-privilege access policy with clear ownership.
- A safe migration path for any secret currently exposed.
