# Workflow Memory

Persistent, provenance-tracked memory where workflows accumulate what they learn
about databases, datasets, schemas, fields, and their quirks over time — so a run
arrives already knowing the kinks of a dataset.

The standard is `instructions/workflow_memory.md`; the design is
`specs/0002-workflow-memory/`. Memory is served by the `knowledge/` agents (prime,
learn, curate, persist) and validated by the `memory-check` gate.

## Layout (two-axis)

```
memory/
  manifest.yaml                    # where memory lives, access levels, committed/external
  _shared/datasets/<ds>/           # facts about a source, reused by any workflow
    schema.md quirks.md pitfalls.md provenance.yaml
  <workflow>/                      # one per workflow in docs/workflows.md
    index.yaml lessons.md
    datasets/<ds>/ patterns.md decisions.md
```

- `_shared/` — what is true about a source (schema, quirks): reused by any workflow.
- `<workflow>/` — how a workflow uses a source (patterns, decisions).

`example_prices` and `quant_researcher/` below are filled-in references — copy the
structure, not the content.

## Rules (see the instruction for the full standard)

- **Metadata only.** Never store credentials, connection strings, data rows, or PII.
- **Provenance always.** Every record cites its source run with dates, confidence,
  and access level (`provenance.yaml` / `index.yaml`).
- **Point-in-time firewall.** Research/backtest runs use only records whose
  `pit_scope` is on or before the decision date — memory must not leak the future.
- **Freshness.** Old records are hypotheses; re-validate before trusting; mark drift
  `stale`. Never silently overwrite — supersede.
- **Reproducible.** Record the memory version a run used in its run card.

## How It Grows

1. **Prime** — a workflow loads relevant records before running on a dataset.
2. **Learn** — after the run, new observations are appended as candidate records.
3. **Curate** — records are deduped, corroborated, and conflicts resolved.

The SDK provides this convention, layout, and gate; the agent runtime performs the
actual read/write.
