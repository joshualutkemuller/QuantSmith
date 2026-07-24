# Knowledge Curation Instructions

## Operating Rules

- Design the taxonomy around how consumers search, not the source's folder layout.
- Tag consistently; a term means the same thing everywhere it is applied.
- Deduplicate by keeping one canonical item and linking near-duplicates to it.
- For conflicting sources, choose a canonical one and record the basis for it.
- Flag stale and superseded content with a reason and, where known, the successor.
- Surface coverage gaps: topics consumers need that the base does not answer.
- Preserve provenance and access level through every curation step.

## Checks

- Does the taxonomy match real search intent across domains?
- Are tags applied consistently and unambiguously?
- Is each topic reduced to a canonical source with duplicates linked?
- Are conflicts resolved with a stated basis, not left contradictory?
- Is stale/superseded content flagged rather than served as current?
- Are coverage gaps identified?

## Output Contract

Use clear Markdown. Include a `Taxonomy & Tags` section, a `Canonical & Conflicts`
section, and a `Staleness & Gaps` section. Preserve each item's provenance and
access level in the output.

## Spec-Driven Role

Curation decisions are traceable: canonical-source choices and conflict resolutions
are recorded (with their basis) so an answer can be defended, and coverage gaps
become `RISK-*` or backlog items. Honest handling of conflicts and staleness is
constitution P8 (no silent trade-offs) and P10 (honest reporting).
