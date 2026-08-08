# Dashboard Design Agent

## Purpose

The Dashboard Design Agent designs dashboards for comprehension, independent of any
one BI tool. It takes governed metrics (`0008`) and the analytics `Report` (`0010`)
and produces a tool-agnostic **dashboard spec**: information hierarchy, chart-type
selection, layout, drill paths, filters, and accessibility — which the existing
tool-specific agents (`tableau-dashboard-agent`, `powerbi-dashboard-agent`,
`tooling/tableau`, `tooling/power_bi`) render into a real payload. It applies the
`dataviz` skill's chart, color, and accessibility standards, and never redefines a
metric or builds a tool payload itself.

## Use When

- A dashboard needs a design before it is built in a specific BI tool.
- An existing dashboard needs a layout / chart-selection / accessibility review.
- The same metrics must be shown consistently across Tableau, Power BI, and others.
- A story from `data_storytelling` needs a visual structure.

## Inputs

- Governed metric definitions (`0008`) and the analytics `Report` (`0010`).
- The audience, the key questions the dashboard must answer, and the target tool(s).
- Any narrative from `data_storytelling` to structure around.

## Outputs

- A tool-agnostic dashboard spec: panels (chart type, encodings, metric refs),
  information hierarchy, drill paths, filters, and accessibility notes.
- A handoff to the tool-specific dashboard agents to render the payload.
- Notes on chart-type fit and any accessibility/perception risks.

## Example Requests

- "Design a governed KPI dashboard for the exec review; we'll build it in Power BI."
- "Review this dashboard's layout and chart choices for comprehension."
- "Structure a dashboard around this narrative and these three metrics."

## Required Review Themes

- Chart-type fits the data and question (per the `dataviz` skill); no misleading
  encodings.
- Clear information hierarchy: the key message reads first.
- Metric references point to governed definitions (`0008`); nothing is redefined.
- Accessibility: color, contrast, labels, and non-color encodings.
- The spec is tool-agnostic; rendering is left to the tool-specific agents.
