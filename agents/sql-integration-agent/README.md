# SQL Integration Agent

## Purpose

The SQL Integration Agent connects to SQL databases, inspects schemas, and runs
safe analytical queries. It resolves connections, introspects catalog metadata,
constructs parameterized SQL aligned to user intent, and executes with guardrails.

## Use When

- A request needs relational data retrieval, joins, aggregations, or schema discovery.
- A database schema needs summarizing before querying.
- A query must run safely with limits, timeouts, and guardrails.

## Inputs

- The connection profile (from env/secrets) and target database.
- The user's data intent.
- Safety constraints (row limits, timeouts, read-only scope).

## Outputs

- Connection verification and catalog/schema summary.
- A parameterized query aligned to intent.
- A result set with query audit metadata.
- Safety notes (limits, guardrails applied).

## Example Requests

- "Discover the schema and summarize the tables relevant to this question."
- "Write a safe, parameterized query for this aggregation with row limits."
- "Run this query read-only with a timeout and return audit metadata."

## Required Review Themes

- Credentials from env/secrets; never embedded (see `agents/secrets_management/`).
- Parameterized SQL only; no string-built queries from untrusted input.
- Read-only where possible; row limits, timeouts, and guardrails applied.
- Point-in-time correctness when querying time-series data.
- Audit metadata returned with every result.
