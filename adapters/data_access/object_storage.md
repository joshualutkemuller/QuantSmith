# Object Storage Data Access Adapter

## Use For

- Parquet, Arrow, CSV, JSON, and model artifacts in S3, Azure Blob, GCS, or local
  object stores.
- Lakehouse or partitioned dataset reads.
- Reproducible snapshot capture.

## Delivery Rules

- Capture URI, version ID when available, checksum, byte size, and partition list.
- Validate expected schema before downstream use.
- Record read options such as compression, delimiter, encoding, and partition
  filters.
- Avoid broad recursive reads without explicit partition bounds.

## Risks

- Partition pruning mistakes can mix as-of periods.
- Object overwrites can break reproducibility without versioning.
- Large scans can create cost surprises.
