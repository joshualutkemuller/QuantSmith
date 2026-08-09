# Pipeline Manifest: <pipeline-name>

> The reviewable contract for a data pipeline. Validated by
> `hooks/stages/pipeline-contract-check.sh` and the standard
> `instructions/pipeline_engineering.md`. Copy this file next to your pipeline as
> `<name>_pipeline_manifest.md`.

## Ownership

- **Owner / steward:** <team or person>
- **Classification:** public | internal | confidential | restricted

## Schedule

- **Cadence / schedule:** <e.g. daily 06:00 UTC — cron `0 6 * * *`>
- **Partitioning:** <e.g. by trading day>

## Inputs & Outputs

| Direction | Dataset | Source / sink | Data contract |
| --- | --- | --- | --- |
| input | <name> | <source> | `templates/data/data_contract.md` |
| output | <name> | <sink> | `templates/data/data_contract.md` |

## Reliability

- **Retry policy:** <max attempts, transient only>
- **Backfill:** <window and how missing partitions are reprocessed>
- **Idempotency:** <keying / dedup that makes a re-run a no-op>

## Observability & Runbook

- **Freshness / SLA:** <watermark and max staleness per step>
- **Runbook / on-call:** <link; steps for a failed or stale run>
- **Escalation:** <who to page and when>

## DAG

```text
<source steps> -> <transform steps> -> <sink steps>
```

Runtime: `src/quantsmith/pipelines/data_pipeline.py` (`0011`); observability:
`src/quantsmith/pipelines/pipeline_observability.py` (`0019`).
