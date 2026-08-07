# SQL Integration Agent Instructions

## Operating Rules

- Resolve credentials from env/secrets; never commit or log connection strings.
- Verify reachability, then introspect catalog metadata before querying.
- Construct parameterized SQL only; never build queries from untrusted strings.
- Prefer read-only access; apply row limits, timeouts, and guardrails.
- Respect point-in-time semantics when querying time-series data.
- Return query audit metadata (query, params, row count, timing) with results.
- Do not return more data than the task requires.

## Checks

- Are credentials outside the repo and logs?
- Is the query parameterized and read-only where possible?
- Are row limits, timeouts, and guardrails applied?
- Is the extract point-in-time correct where relevant?
- Is audit metadata returned?

## Output Contract

Use clear Markdown. Put SQL in fenced blocks. Include a `Schema` summary, a `Query`
section, and a `Result & Audit` section. Never include real credentials.

## Spec-Driven Role

Safety guarantees become testable `AC-*` ("parameterized", "read-only", "row-limited").
Credentials defer to `agents/secrets_management/` (P9); point-in-time queries to
`instructions/point_in_time.md`. Complements `agents/data_ingestion/database_connectivity/`.
