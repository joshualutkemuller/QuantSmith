# Local File Artifact Delivery Adapter

## Use For

- Repository examples.
- Local development.
- Spec evidence and generated handoff files.
- Draft packs that should be inspected before external delivery.

## Delivery Rules

- Write artifacts under a workflow-specific output directory.
- Use deterministic filenames that include workflow ID, run ID, and artifact type.
- Emit a manifest listing artifact paths, checksums, and classification.
- Avoid storing secrets, credentials, raw PII, MNPI, or restricted position data.
- Prefer Markdown, JSON, CSV, Parquet, PNG, or PDF according to artifact type.

## Result Evidence

Capture path, checksum, byte size, timestamp, artifact type, and classification.
