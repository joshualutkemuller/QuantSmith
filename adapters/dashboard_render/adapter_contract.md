# Dashboard Render Adapter Contract

## Input

```yaml
workflow_id: string
run_id: string
target: xlsx | react | powerbi
payload_kind: excel_workbook | react_dashboard | powerbi_report
payload: object            # a rendered payload from render_excel / render_react / render_powerbi
dataset_source: string     # a data_access reference; the adapter does NOT embed data or credentials
destination: string        # output directory or path
owner: string
classification: public | internal | confidential | restricted
correlation_id: string
dry_run: boolean
```

## Output

```yaml
adapter_name: string
provider: string
status: generated | published | skipped | failed
artifact_uri: string | null      # path to the .xlsx / scaffolded app dir / published report
provider_object_id: string | null
correlation_id: string
timestamp_utc: string
retryable: boolean
error_code: string | null
error_message_redacted: string | null
evidence_uri: string | null      # manifest of files + checksums
```

## Required Behavior

- Accept an **already-rendered, governed** payload; do not redesign the dashboard,
  recompute metrics, or add panels. The payload's measures are the governed metrics.
- Materialize the artifact deterministically: the same payload yields the same files
  (stable filenames, ordering, and layout).
- Reach data through a `data_access/` adapter via `dataset_source`; never embed raw
  data, credentials, MNPI, PII, or restricted positions in the artifact.
- Preserve the payload's title, dataset reference, page, filters, and panel order.
- Support `dry_run` (validate the payload and report the planned outputs without
  writing) and a no-op when nothing changed.
- Emit an evidence manifest (paths, checksums, byte sizes, classification).
- Redact secrets and keep them out of client bundles and workbook connections.

## Workflow Boundary

```text
analytics/dashboard_design -> DashboardSpec
  -> render_excel | render_react | render_powerbi -> governed payload
  -> dashboard_render adapter (this contract) -> live artifact + evidence
```
