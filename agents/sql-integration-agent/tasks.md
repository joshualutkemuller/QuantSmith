# SQL Integration Agent Tasks

## Schema Discovery

Input: a connection profile and a data question.

Output: catalog introspection and a summary of the relevant tables.

## Safe Query

Input: user intent and schema.

Output: a parameterized, read-only query with limits and guardrails.

## Execute & Audit

Input: a validated query.

Output: the result set plus query audit metadata (params, row count, timing).

## Connection Review

Input: existing SQL integration code.

Output: review of credential exposure, injection risk, and scope, with fixes.
