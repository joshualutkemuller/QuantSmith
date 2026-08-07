# Notion Artifact Delivery Adapter

## Use For

- Publishing human-readable workflow notes.
- Capturing research decisions, incident summaries, and content calendars.
- Creating pages or database entries from approved artifacts.

## Delivery Rules

- Map artifact type to page or database schema.
- Preserve source artifact URI, workflow ID, run ID, owner, and as-of timestamp.
- Use Notion for narrative artifacts, not as the canonical store for large data.
- Do not publish restricted artifacts unless workspace permissions are approved.

## Risks

- Database schemas drift without contract checks.
- Rich text conversion can lose tables, citations, or code formatting.
- Notion pages can become informal sources of truth unless linked back to the
  canonical artifact.
