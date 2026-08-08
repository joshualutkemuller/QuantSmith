# XLSX Dashboard Render Adapter

## Use For

- Delivering a governed dashboard as a real Excel workbook analysts can open.
- Spec evidence and repository examples of a rendered dashboard.
- Handing a reviewed design to a team that lives in Excel.

## Input

An `ExcelWorkbookPayload` from `render_excel` (spec `0016`,
`src/quantsmith/pipelines/excel_profile.py`): `title`, `dataset`, `data_sheet`,
`dashboard_sheet`, `charts` (each with an Excel `chart_type`, governed `measure`, and
`dimensions`), and `filters`.

## Generation Rules

- Write a `.xlsx` using a spreadsheet library (e.g. `openpyxl`); the adapter carries
  that optional dependency, keeping the core pipeline dependency-free.
- Create the data sheet (`data_sheet`) populated from `dataset_source` via a
  `data_access/` adapter — never embed raw data or a live credentialed connection
  string in the workbook.
- Create the dashboard sheet (`dashboard_sheet`), adding one native Excel chart per
  `ExcelChart` in payload order, bound to its governed measure and dimensions.
- Apply `filters` as workbook slicers or documented filter cells.
- Use deterministic filenames including `workflow_id`, `run_id`, and the sheet names;
  the same payload must produce a byte-stable workbook where the library allows.
- Do not add panels, measures, or calculations beyond the payload; the design is
  fixed upstream.

## Result Evidence

Capture the workbook path, checksum, byte size, sheet names, chart count, and
classification. On `dry_run`, report the planned sheets and charts without writing.

## Notes

- `kpi` panels render as formatted "card" cells; `gauge` renders as the doughnut
  substitute chosen by `render_excel`.
- Graduate heavy logic out of the workbook: the workbook presents governed results, it
  does not recompute them.
