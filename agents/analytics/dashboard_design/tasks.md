# Dashboard Design Tasks

## Design A Dashboard

Input: governed metrics (`0008`), the analytics `Report` (`0010`), the audience, and
the key questions.

Output: a tool-agnostic dashboard spec (panels, chart types, encodings, hierarchy,
drill paths, filters, accessibility) handed to a tool-specific agent to render.

## Review An Existing Dashboard

Input: a dashboard's layout and chart choices.

Output: a review of chart-type fit, information hierarchy, misleading encodings, and
accessibility, with concrete fixes.

## Structure A Dashboard Around A Narrative

Input: a narrative from `data_storytelling` and the supporting metrics.

Output: a dashboard spec whose hierarchy leads with the narrative's key message.

## Make A Dashboard Portable Across Tools

Input: a dashboard spec targeted at one BI tool.

Output: a tool-agnostic spec plus per-tool rendering handoffs, so the same design is
consistent across Tableau, Power BI, and other profiles.
