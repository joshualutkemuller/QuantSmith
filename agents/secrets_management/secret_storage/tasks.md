# Secret Storage Tasks

## Design Secret Store Layout

Input: the secrets/keys to store, services, and environments.

Output: store selection, naming/structure convention, and access policy scoped to
least privilege.

## Migrate Secrets Out Of The Repo

Input: secrets currently in `.env`, config, or code.

Output: a migration plan into a managed store, with rotation of any exposed
secret and a gitignored `.env` plus `.env.example` placeholders.

## Access Policy Review

Input: an existing secret store setup.

Output: review of scope, environment separation, encryption, and ownership, with
least-privilege fixes.

## Custom Key/Value Configuration

Input: non-credential custom keys/values that are still sensitive.

Output: storage and access design that keeps sensitive configuration out of the
repo while remaining reproducible.
