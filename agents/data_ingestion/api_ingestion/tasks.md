# API Ingestion Tasks

## Reproducible API Pull

Input: API, endpoints, auth, and the data needed.

Output: a paginated client with rate-limit and retry handling, as-of capture, and
archived raw payloads.

## API Client Review

Input: an existing API client.

Output: review of token exposure, pagination completeness, rate-limit and retry
handling, and idempotency, with fixes.

## Incremental Load Design

Input: an API with update semantics and volume constraints.

Output: an incremental load with a durable cursor, idempotency, and a documented
full-refresh path.

## Schema Validation & Contract

Input: sample API responses.

Output: a response-schema validation step and a `data_contract.md` describing the
mapped schema, keys, and point-in-time rules.
