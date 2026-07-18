---
name: powerbi-dashboard-agent
description: Generate and manage PowerBI dashboards/reports using retrieval-augmented context and strict payload validation. Use when users request PowerBI report creation, updates, governance checks, or schema-safe API payload generation.
---

# PowerBI Dashboard Agent Skill

1. Retrieve PowerBI model/report patterns from the knowledge base.
2. Draft a structured PowerBI payload aligned to prepared dataset fields.
3. Validate payload against strict schema contracts before API submission.
4. Repair invalid payloads using bounded correction retries.
5. Return final payload, assumptions, and deployment/management instructions.
