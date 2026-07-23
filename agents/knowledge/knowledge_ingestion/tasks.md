# Knowledge Ingestion Tasks

## Index A Source

Input: a knowledge source and its access model.

Output: an extraction/chunking approach with provenance and access metadata captured
per item.

## Sensitive-Content Review

Input: content being ingested.

Output: PII, secret, and MNPI/restricted findings with handling for each.

## Incremental Sync Design

Input: a source that updates over time.

Output: an idempotent, deduplicated sync plan with content hashes and timestamps.

## Handoff To Curation

Input: an indexed corpus.

Output: a handoff describing domains, tags, and provenance so curation can organize
it.
