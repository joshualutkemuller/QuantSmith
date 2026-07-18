---
name: tableau-dashboard-agent
description: Generate Tableau dashboard specifications using retrieval-augmented context and strict schema validation. Use when users request dashboard creation, updates, or layout recommendations.
---

# Tableau Dashboard Agent Skill

1. Retrieve dashboard patterns and API references from knowledge base.
2. Draft a structured dashboard payload mapped to prepared data fields.
3. Validate payload with Pydantic contracts before API submission.
4. Repair validation failures through bounded correction loops.
5. Emit final payload, assumptions, and deployment instructions.
