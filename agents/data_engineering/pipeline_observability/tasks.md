# Pipeline Observability Tasks

## Read A Run's Health

Input: a `RunManifest` (`0011`) and a freshness watermark.

Output: an `ObservabilityReport` with per-step health, freshness breaches, downtime
steps, and an SLA verdict.

## Check Freshness

Input: a manifest and the expected watermark partition per step.

Output: which steps are behind the watermark and by how much.

## Detect Data Downtime

Input: a manifest.

Output: the steps and partitions in downtime, and whether a later run recovered them.

## Produce A Lineage View

Input: the `Pipeline` definition.

Output: a step -> dependencies lineage map for tracing which steps feed which.
