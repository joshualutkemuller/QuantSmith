# Technology & Tooling Agents

This folder groups agents for the specific platforms and tools quants work in —
spreadsheets, BI/reporting, and (as the group grows) compute and data-store
technologies. They bring the SDK's engineering discipline to tools that are often
used without version control, tests, or point-in-time rigor.

## Agents

| Agent | Handles |
| --- | --- |
| `excel/` | Excel models and workbooks: structure, formula auditability, reproducibility, VBA/Power Query safety, model-risk review. |
| `power_bi/` | Power BI datasets and reports: data model (star schema), DAX, refresh/lineage, row-level security, performance. |
| `tableau/` | Tableau workbooks and data sources: extracts vs live, LOD/table calcs, honest visualization, publishing/permissions. |

## Shared Principles

Every tooling agent upholds the constitution (`instructions/engineering_principles.md`):

- **Reproducibility (P4).** These tools resist version control and reproducibility.
  Externalize data and logic where possible, capture the inputs (snapshot/refresh
  time), and document how a result can be regenerated. Recommend graduating heavy
  logic out of the tool into tested code when the tool becomes the risk.
- **Point-in-time correctness.** Time-series layouts, refreshes, and joins must not
  introduce look-ahead; use point-in-time data and record as-of times. See
  `instructions/point_in_time.md`.
- **Auditability.** No hidden logic, no magic constants buried in formulas, no
  undocumented manual overrides. A reviewer must be able to trace every number.
- **Secrets stay out (P9).** Data-source credentials live in the platform's secret
  store or gateway, never embedded in a workbook, PBIX, or macro. See
  `agents/secrets_management/`.
- **Honest presentation (P10).** Reports and dashboards must not mislead — correct
  scales, baselines, and uncertainty.

## Where They Fit

Tooling agents span Implementation (building the model/report), Testing
(reconciliation and validation), and Maintenance (refresh, monitoring). Encode the
tool's assumptions and reconciliation checks as spec `AC-*` so the artifact is
traceable, not a black box.

## Growing This Group

Candidate future agents as demand appears: `kdb_q/` (tick/time-series database),
`matlab/`, `r/`, and `jupyter/` (notebook reproducibility). Add each with the full
four-file contract and a row above.
