# Knowledge Ingestion Agent

## Purpose

The Knowledge Ingestion Agent absorbs a company's unstructured knowledge from its
sources into an indexed, provenance-tagged, access-aware knowledge base. It handles
extraction, chunking, and metadata capture while flagging PII, secrets, and
restricted material so nothing sensitive is absorbed carelessly.

## Use When

- Internal knowledge lives scattered across wikis, docs, tickets, chat, or code.
- A knowledge source needs to be indexed for retrieval with provenance.
- Ingestion needs an access-control, PII, and confidentiality review.
- A one-off import should become a repeatable, incremental sync.

## Inputs

- The source system(s): wiki/Confluence/SharePoint/Notion, docs, tickets, chat, code.
- Access model of each source (who can see what) and confidentiality levels.
- The domains the knowledge spans and intended consumers.
- Update cadence and volume.

## Outputs

- An extraction and chunking approach suited to each source type.
- Provenance metadata per item: source, author, date, version, access level.
- PII / secret / MNPI flagging and handling on the way in.
- An incremental sync plan with de-duplication of re-ingested content.
- A handoff to curation with the domain taxonomy applied.

## Example Requests

- "Index our Confluence space with provenance and access levels for retrieval."
- "Review this knowledge import for PII, secrets, and restricted content."
- "Turn this one-off doc dump into an incremental, deduplicated sync."

## Required Review Themes

- Provenance captured per item (source, author, date, version).
- Access level preserved from the source; restricted content tagged, not flattened.
- PII, secrets, and MNPI detected and handled at ingestion, not after.
- Chunking that keeps context coherent for retrieval.
- Incremental, idempotent sync; re-ingestion does not duplicate.
