# Database Connectivity Tasks

## Reproducible Extract

Input: target store, tables/columns, date range, and point-in-time needs.

Output: parameterized query, snapshot identifier, and reproduction steps, with
credentials sourced from env/secrets.

## Connection & Credential Review

Input: existing connection/query code.

Output: review of credential exposure, SQL injection risk, access scope, and scan
cost, with fixes.

## Point-in-Time Extraction Plan

Input: a table with revision/restatement behavior.

Output: an as-of extraction plan that uses original vintage and avoids look-ahead.

## Snapshot & Contract

Input: an extracted dataset.

Output: a captured snapshot (hash/id) and a `data_contract.md` describing schema,
keys, and point-in-time rules.
