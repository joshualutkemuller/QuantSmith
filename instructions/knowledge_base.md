# Knowledge Base Instructions

## Purpose

Use this instruction set when absorbing, organizing, retrieving, or persisting a
company's unstructured institutional knowledge. It is the shared standard behind
the `agents/knowledge/` group. The goal is a knowledge base that is grounded,
access-aware, provenance-tracked, and durable — one whose answers can be trusted
and defended.

## Required Inputs

- The knowledge source(s) or the question to answer.
- The access model: who is allowed to see what, and any information barriers.
- Provenance available for each item (source, author, date, version).
- Domains covered and intended consumers.
- Confidentiality classification (public, internal, restricted, MNPI).

## Expected Output

- Grounded, cited answers, or indexed/curated knowledge with provenance.
- Access-appropriate results that respect authorization and barriers.
- Freshness and confidence signals.
- Durable artifacts for knowledge worth keeping, not conversational recall.

## Standards

- **Ground everything.** Never assert what a source does not support; attach a
  citation to every claim. "Not found" or "uncertain" is a valid, required answer.
- **Preserve access level.** Each item keeps the access level of its source;
  ingestion never widens it, and retrieval filters by the asker's authorization.
- **Respect information barriers.** Never surface MNPI or restricted-list material
  to an unauthorized asker, and do not confirm its existence to them.
- **Track provenance.** Record source, author, date, version, and a content hash
  for every item so an answer is reproducible from its sources.
- **Flag freshness.** Mark stale and superseded knowledge; never serve it as current.
- **Resolve conflicts explicitly.** When sources disagree, designate a canonical
  one and state the basis (ownership, recency, authority).
- **Persist over memory.** Store durable knowledge as versioned artifacts, not chat.
- **Keep PII and secrets out.** Detect on ingestion; never expose them in answers.

## Checks

- Is every claim backed by a citation the asker is allowed to see?
- Was retrieval access-filtered before the answer was composed?
- Are MNPI and restricted material withheld from unauthorized askers?
- Does every item carry provenance (source, author, date, version)?
- Is stale or superseded content flagged rather than served as current?
- Are conflicts resolved with a canonical source and a stated basis?
- Is durable knowledge stored as a versioned artifact?
- Are PII and secrets kept out of both the index and the answers?

## Common Failure Modes

- Confident answers with no citation, or citations that do not support the claim.
- Widening access on ingestion, so restricted content becomes generally visible.
- Leaking MNPI or restricted-list material across an information barrier.
- Serving stale or superseded knowledge as if it were current.
- Presenting contradictory sources without resolving which is authoritative.
- Losing knowledge to chat and meetings instead of capturing it durably.
- Indexing PII or secrets without detection or handling.

## Spec-Driven Alignment

This standard backs the `agents/knowledge/` group across the lifecycle. Grounding,
citation, and honest gaps are constitution P10; access control and confidentiality
are P9 and defer to `agents/secrets_management/`. Retrieval guarantees ("every
claim cited", "access-filtered", "barriers respected", "not-found when
unsupported") become testable `AC-*`; provenance and reproducibility of answers
are P4. Durable capture is the SDK's "artifacts over memory" principle; captured
decisions can cite the `REQ-*`/`RISK-*` they resolved. See
`instructions/documentation.md` for durable-artifact standards.
