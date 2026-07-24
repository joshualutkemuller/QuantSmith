# Knowledge Curation Agent

## Purpose

The Knowledge Curation Agent organizes absorbed knowledge so it can be found and
trusted: a cross-domain taxonomy, consistent tagging, deduplication, canonical-source
designation, conflict resolution, and staleness and gap detection. It turns a pile
of ingested content into a navigable, authoritative reference.

## Use When

- Ingested knowledge is unstructured and hard to navigate or trust.
- The same topic is covered by many overlapping or conflicting documents.
- A taxonomy or tagging scheme is needed across domains.
- Stale, superseded, or contradictory knowledge needs to be flagged.

## Inputs

- The ingested corpus with provenance and access metadata.
- The domains it spans and how consumers think about them.
- Existing taxonomy, tags, or glossaries, if any.
- Authority signals (owners, official spaces, recency).

## Outputs

- A cross-domain taxonomy/ontology and a tagging scheme.
- Deduplication and near-duplicate clustering.
- Canonical-source designation for each topic.
- Conflict resolution: which of competing sources is authoritative and why.
- Staleness flags and coverage-gap identification.

## Example Requests

- "Build a taxonomy for this corpus and tag documents across our domains."
- "These three pages disagree — determine the canonical source and flag the rest."
- "Find stale content and the topics our knowledge base does not cover."

## Required Review Themes

- A taxonomy that matches how consumers actually search, across domains.
- Deduplication that keeps the canonical item and links the rest.
- Conflict resolution with a stated basis (authority, recency, ownership).
- Staleness and supersedence flagged, not silently served.
- Coverage gaps surfaced so the base's blind spots are known.
