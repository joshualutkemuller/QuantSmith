# Artifact Delivery Adapter Contract

## Input

```yaml
workflow_id: string
run_id: string
artifact_id: string
artifact_type: run_card | report | data_contract | model_card | monitoring_plan | draft_pack | chart_spec | evidence_bundle
title: string
source_path: string
destination: string
owner: string
visibility: private | team | org | public
retention_policy: string
classification: public | internal | confidential | restricted
correlation_id: string
dry_run: boolean
```

## Output

```yaml
adapter_name: string
provider: string
status: stored | delivered | skipped | failed
provider_object_id: string | null
artifact_uri: string | null
correlation_id: string
timestamp_utc: string
retryable: boolean
error_code: string | null
error_message_redacted: string | null
evidence_uri: string | null
```

## Required Behavior

- Validate destination, visibility, classification, and retention policy.
- Preserve artifact title, type, run ID, workflow ID, and correlation ID.
- Return a durable URI or provider object ID when storage succeeds.
- Do not loosen permissions relative to the requested classification.
- Support dry-run validation before writing or sharing.
