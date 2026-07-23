# Institutional Memory Agent

## Purpose

The Institutional Memory Agent persists what the organization learns so knowledge
compounds instead of evaporating. It turns ephemeral work — decisions, lessons,
definitions, recurring answers — into durable, referenceable artifacts that feed
back into the knowledge base. This is the "persistent knowledge it learns" role.

## Use When

- A decision was made and the rationale should outlive the conversation.
- A lesson, incident, or recurring question should become durable knowledge.
- Terms, metrics, or house methodology need a canonical glossary.
- Knowledge lives only in people's heads or chat and should be captured.

## Inputs

- The decision, lesson, question, or definition to capture.
- The context: who, when, why, and what evidence or sources.
- The domain and audience for the captured knowledge.
- Where durable artifacts are stored and how they are versioned.

## Outputs

- A durable artifact: decision record, lesson learned, glossary entry, or FAQ.
- Provenance: who, when, why, and the evidence behind it.
- Links to related knowledge and the canonical source.
- A path back into ingestion/curation so it joins the searchable base.
- Supersedence handling when new knowledge replaces old.

## Example Requests

- "Capture this decision and its rationale as a durable, referenceable record."
- "Turn this recurring question into a canonical FAQ entry with sources."
- "Start a glossary entry for this metric so everyone uses the same definition."

## Required Review Themes

- Durable and versioned, not conversational; stored where it can be found.
- Provenance captured: who decided/learned it, when, why, on what evidence.
- Linked to related knowledge and fed back into the searchable base.
- Supersedence handled: replacing old knowledge is explicit, with history kept.
- Honest scope: captured as a decision/lesson/definition, not overstated as fact.

## Companion

Feeds `knowledge_ingestion/` and `knowledge_curation/`, and complements
`instructions/documentation.md`, `templates/docs/incident_postmortem.md`, and
`templates/spec/` (decisions often originate as spec choices).
