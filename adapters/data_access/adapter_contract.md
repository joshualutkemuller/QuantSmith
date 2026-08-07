# Data Access Adapter Contract

## Input

```yaml
workflow_id: string
run_id: string
source_id: string
source_type: sql | object_storage | market_data | api
as_of_utc: string
query_or_path: string
parameters:
  key: value
entitlement_context: string
snapshot_required: boolean
expected_schema_uri: string | null
correlation_id: string
dry_run: boolean
```

## Output

```yaml
adapter_name: string
provider: string
status: retrieved | skipped | failed
dataset_uri: string | null
snapshot_uri: string | null
row_count: integer | null
schema_hash: string | null
checksum: string | null
as_of_utc: string
correlation_id: string
timestamp_utc: string
retryable: boolean
error_code: string | null
error_message_redacted: string | null
```

## Required Behavior

- Preserve as-of time and entitlement context.
- Return checksums or hashes when data is materialized.
- Support dry-run validation of access and query/path shape.
- Never log credentials or raw secrets.
- Fail closed when entitlements or data classification are unclear.
