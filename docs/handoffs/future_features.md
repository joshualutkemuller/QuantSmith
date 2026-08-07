# Future Features

The running backlog of features to build. Add new ideas as rows; promote one to a
full `specs/NNNN-slug/` when work starts (see `docs/handoffs/README.md`).

**Status:** `proposed` → `in-progress` → `done`.
**Priority:** P1 (high) · P2 (medium) · P3 (nice-to-have).

## Agents

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `agents/data_engineering/data_modeling/` | Dimensional/warehouse modeling: star/snowflake schemas, slowly-changing dimensions, grain | P1 | proposed |
| `agents/data_engineering/pipeline_orchestration/` | dbt-style models, DAGs, scheduling, incremental loads, backfills, idempotency | P1 | proposed |
| `agents/data_engineering/pipeline_observability/` | Data freshness, SLAs, lineage, data-downtime detection | P2 | proposed |
| `agents/data_engineering/data_governance/` | Catalog, lineage, access policy, ownership | P3 | proposed |
| `agents/analytics/metrics_semantic_layer/` | Canonical KPI/metric definitions (semantic layer) — the biggest data-analyst consistency win | P1 | proposed |
| `agents/analytics/experimentation/` | A/B testing, power analysis, causal caveats | P2 | proposed |
| Normalize `agents/quant_analyst/` | Bring the consolidated `quant_analyst` (and `agentic_quant/` Python) into the four-file contract and catalog | P2 | proposed |

## Instructions (backing standards)

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `instructions/risk_management.md` | Standard behind the `risk` agent (exposure, tail, limits) | P2 | proposed |
| `instructions/data_ingestion.md` | Standard behind `data_ingestion/*` (PIT capture, snapshots, schema validation) | P2 | proposed |
| `instructions/reproducibility.md` | Operationalize P4 for the `repro` gate and run card | P2 | proposed |
| `instructions/monitoring.md` | Standard behind `maintenance_monitoring` and the monitoring plan | P3 | proposed |

## Gates

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| `hooks/stages/ingestion-snapshot-check.sh` | Verify ingestion captures a snapshot/checksum | P3 | proposed |
| Stricter notebook-output gate | Beyond the current `implementation` check | P3 | proposed |
| Enforce `leakage` in CI | Currently advisory (heuristic); revisit once patterns are tuned | P3 | proposed |

## Docs & Packaging

| Feature | What it adds | Priority | Status |
| --- | --- | --- | --- |
| Expand `docs/adoption_guide.md` | Full walkthrough with per-project-type recipes | P1 | proposed |
| Copier-style sync CLI | Selective install + update per `docs/packaging.md` | P2 | proposed |
| More worked examples | A risk/forecast spec end to end; an ingestion example that emits a data contract | P2 | proposed |
| `CHANGELOG.md` + versioning policy | Once the SDK is consumed by other repos | P2 | proposed |
| Visual workflow diagram | A rendered diagram of `docs/workflows.md` | P3 | proposed |

## Recently Shipped (for reference)

- Model-development standard (`instructions/model_development.md`) and the
  consolidated workflow map (`docs/workflows.md`).
- Securities financing, formulaic alphas, trading strategies, tooling, knowledge,
  and secrets agent groups.
- The consolidation pass (refreshed `sdk_plan`, `handoff`, `agentic_dictionary`;
  added the adoption guide).
