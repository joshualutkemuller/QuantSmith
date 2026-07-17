# File Ingestion Tasks

## Typed Loader

Input: file(s), format, and expected schema.

Output: a loader with explicit dtypes, encoding/delimiter/header handling, date
parsing, and on-load validation.

## Format Review

Input: an existing file loader.

Output: review of schema, encoding, date/timezone, missing-value, and silent-
coercion pitfalls, with fixes.

## Multi-File / Partition Ingestion

Input: multiple files or partitions with possibly differing schemas.

Output: a reconciliation plan and a combined, validated load.

## Snapshot & Contract

Input: a loaded dataset and its source file(s).

Output: source checksum(s) captured and a `data_contract.md` describing schema,
keys, and missingness rules.
