# Knowledge Management Agents

This folder groups agents that absorb a company's knowledge across domains,
organize it, answer questions from it with references, and persist what the
organization learns. Unlike `data_ingestion/` (structured data), these agents deal
with unstructured institutional knowledge: wikis, docs, tickets, chat, research
archives, code comments, and decisions.

## Agents

| Agent | Handles |
| --- | --- |
| `knowledge_ingestion/` | Absorbing internal sources (wiki, Confluence/SharePoint/Notion, docs, tickets, chat, code): extraction, chunking, provenance and access metadata, PII/secret/MNPI flagging. |
| `knowledge_curation/` | Organizing absorbed knowledge: taxonomy/ontology across domains, tagging, deduplication, canonical-source designation, conflict resolution, staleness and gap detection. |
| `knowledge_retrieval/` | Answering user questions grounded in the knowledge base, with citations, respecting the asker's access level and information barriers. |
| `institutional_memory/` | Persisting what the organization learns: decision records, lessons learned, glossary, FAQs, runbooks — durable, referenceable artifacts, not conversational memory. |

## Shared Principles

Every knowledge agent upholds the constitution (`instructions/engineering_principles.md`):

- **Grounded and cited (P10).** Never assert what a source does not support. Every
  answer carries citations to the documents behind it; "not found" or "uncertain"
  is a valid, required answer when the base does not cover the question.
- **Access control & information barriers.** Respect who is allowed to see what.
  In a research/trading firm this includes MNPI, restricted lists, and Chinese
  walls: absorbed knowledge carries its access level, and retrieval never surfaces
  restricted material to an unauthorized asker.
- **PII and secrets stay controlled (P9).** Flag and handle personal data,
  credentials, and confidential content on ingestion; never expose secrets in an
  answer. See `agents/secrets_management/`.
- **Provenance and freshness.** Every item records its source, author, date, and
  version. Stale or superseded knowledge is flagged, not served as current.
- **Persistence over memory.** Durable, versioned artifacts beat conversational
  recall (an SDK principle); knowledge is stored so it compounds and is auditable.

## Where They Fit

Knowledge agents are cross-cutting: they inform Planning (what is already known and
decided), support every domain agent with references, and feed Maintenance (keeping
institutional memory current). Curated knowledge and decisions can be cited by spec
`REQ-*`/`RISK-*` so work builds on what the organization already knows.

## Related

- `agents/data_ingestion/` — structured data (this group is unstructured knowledge).
- `agents/secrets_management/` — access, secrets, and confidentiality handling.
- `instructions/documentation.md` — durable-artifact standards.
