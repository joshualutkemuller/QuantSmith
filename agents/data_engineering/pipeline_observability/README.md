# Pipeline Observability Agent

## Purpose

The Pipeline Observability Agent turns a pipeline's run manifest into a health read:
per-step status, data freshness against a watermark, data-downtime detection, an SLA
verdict, and a lineage view. It consumes the `RunManifest` the DAG runner emits
(`0011`) — it observes pipelines, it does not re-run them. This is the Data Engineer
node that answers "is the data fresh, complete, and on-SLA right now?"

## Use When

- A pipeline run needs a freshness / SLA / downtime read from its manifest.
- A data consumer asks whether a table is current and complete.
- A lineage view is needed to trace which steps feed which.
- An on-call engineer needs to know which step broke and whether it recovered.

## Inputs

- A `RunManifest` from the DAG runner (`0011`, `src/quantsmith/pipelines/data_pipeline.py`).
- A freshness watermark (the partition each step is expected to have reached).
- The `Pipeline` (for lineage) and an optional max-attempts SLA.

## Outputs

- An `ObservabilityReport`: per-step health (status counts, latest ok partition,
  attempts, fresh/downtime flags), freshness breaches, downtime steps, an SLA verdict,
  and a lineage map.
- A degraded/healthy status and the specific SLA breaches.
- Handoffs to `maintenance_monitoring`, the alerts agents, and `pipeline_orchestration`.

## Example Requests

- "Is the sales pipeline fresh as of today's partition?"
- "Which steps are in data downtime, and did they recover?"
- "Give me the lineage and SLA status for this run."

## Required Review Themes

- Freshness against an explicit watermark; a stale step is reported, not hidden.
- Data downtime: a failed partition is a gap until a later run recovers it.
- Honest SLA verdict — degraded when any step is stale, in downtime, or over its
  attempt budget.
- Lineage traces real DAG dependencies; observability reads, it does not re-orchestrate.
