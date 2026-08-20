# Plan: Workflow Memory Runtime & Author Attribution

- **Spec:** 0048-workflow-memory-runtime (`spec.md`)
- **Last updated:** 2026-08-21

> HOW. Architecture, contracts, and the trade-offs taken.

## Shape

One module, `src/quantsmith/pipelines/workflow_memory.py`, plus one identity
helper. It follows the pattern every other `pipelines/` runtime uses: frozen
dataclasses in, frozen dataclasses out, standard library only, no I/O beyond
reading the files it is pointed at.

```
load_store(root)                      -> Store          REQ-001
query(store, ...)                     -> tuple[Record]  REQ-002, REQ-003
render_context(records, budget_chars) -> str            REQ-004
validate(store)                       -> tuple[Finding] REQ-005, REQ-009, REQ-010
check_decay(store, as_of)             -> tuple[Finding] REQ-006
resolve_author(env, root)             -> Author         REQ-007, REQ-008
store_version(store)                  -> str            REQ-011
```

`validate` and `check_decay` are separate because they answer different
questions — "is this record well-formed?" versus "is this record still true?" —
and a gate may want to enforce the first while only advising on the second.

## Data contracts

```python
@dataclass(frozen=True)
class Record:
    id: str
    scope: str                  # "dataset:x" | "table:x" | "field:x"
    type: str                   # schema|quirk|pattern|pitfall|decision|metric|performance
    statement: str
    evidence: Mapping[str, str] # source_run, optional sample_query — never data
    confidence: str             # low|medium|high
    corroboration_count: int
    first_seen: date
    last_confirmed: date
    status: str                 # active|stale|superseded|retired
    pit_scope: str
    access_level: str           # inherited from the manifest when absent
    author: str | None          # NEW (0048) — handle, never an email
    source_file: str            # provenance for findings; not a memory field
    source_line: int
```

`author` is appended and optional, so every file `0002` committed parses
unchanged (NFR-003). A record without one is a finding (REQ-010), not an error —
the existing store predates the field, and failing on it would make the gate
unusable on day one.

`Finding` reuses the shape the other gates' runtimes use: `severity`, `code`,
`message`, `record_id`, `source_file`, `source_line`.

## The YAML subset

No PyYAML (NFR-001), so the parser supports exactly the grammar the committed
files use:

- `key: value` mappings, two-space indentation
- `- ` list items, one level, each opening a mapping
- one level of nested mapping (`evidence:` → `source_run:`)
- `#` comments and blank lines
- scalars: bare, `'single'`, or `"double"` quoted; no block scalars, no anchors,
  no flow collections, no multi-document files

Anything else raises `MemoryParseError(file, line, reason)`. **This is the
central trade-off (RISK-001):** a permissive parser that guesses would let a
malformed record through as a plausible-looking one, and wrong memory is worse
than absent memory. Loud failure keeps the blast radius at "this file did not
load" instead of "this field means something else now". The committed store is
the parser's fixture set, so the subset is pinned by real files rather than by
an author's imagination.

## Point-in-time filtering (REQ-003, RISK-004)

`pit_scope` is free text today. Two forms appear in the committed store:

| `pit_scope` | Meaning | Behaviour under `as_of` |
| --- | --- | --- |
| `<= run date`, `<= decision date` | Learned from data available at the time | Included when `first_seen <= as_of` |
| `original vintage only` | Depends on unrevised vintage data | **Excluded** from point-in-time queries |
| anything else | Unknown | **Excluded**, and reported as a validation finding |

Unrecognised means excluded, never included. A missing record makes a workflow
ask again; a leaked record makes a backtest lie, and P4 forbids that. The
asymmetry is deliberate and is the reason the default is exclusion.

## Ranking and rendering (REQ-004, RISK-005)

Records are ranked by, in order: `confidence` (high > medium > low),
`corroboration_count` descending, `last_confirmed` descending, then `id`
ascending as a total-order tiebreak — so the ordering is deterministic
(NFR-002) rather than dependent on filesystem or dict iteration order.

`render_context` emits one line per record — id, scope, type, statement,
confidence, `last_confirmed` — and fills up to `budget_chars`, then appends
`"... N further record(s) omitted (ranked below the included set)."` The budget
is in characters, not tokens: the module has no tokenizer and will not pretend
to. Callers converting tokens to characters own that ratio.

Showing `last_confirmed` on every line is not decoration — it is how a reader
discounts an old record when the decay gate is only advisory (RISK-003).

## Identity resolution (REQ-007, REQ-008)

A chain, first hit wins, each step total:

| Order | Source | Handle produced |
| --- | --- | --- |
| 1 | `QF_MEMORY_AUTHOR` env var | used verbatim (must satisfy the pattern) |
| 2 | `identity.yml` at repo root — local-only, gitignored | `author:` used verbatim |
| 3 | `git config user.email` | derived, pseudonymous |
| 4 | OS username (`getpass.getuser()`) | derived, pseudonymous |
| 5 | nothing resolvable | `None` → REQ-010 finding |

Steps 1–2 give the **opaque handle** path: a person picks `jl`, and the
handle↔person table lives outside the repository. Steps 3–4 are the automatic
path for anyone who has not configured one, so attribution works with zero
setup.

Derivation: `"anon-" + sha256(salt + normalized_identity).hexdigest()[:10]`,
where `normalized_identity` is lowercased and stripped. Stable for the same
input (AC-011), distinct for different inputs (AC-012), and — because the output
is hex — **structurally incapable of containing `@`** (AC-013). That is the
point: the PII guard is not "remember not to paste your email", it is "an email
cannot survive this function".

Step 1 is checked before any subprocess runs, so CI and agent contexts never
shell out to git (AC-010, NFR-004). `git config` is invoked with a timeout and
its failure is a fall-through, not an error — a copied scaffold with no git
still resolves an author.

**The handle is pseudonymous, not anonymous.** On a ten-person desk, handle plus
commit history re-identifies the author trivially. The module docstring says so
in those words (RISK-002); a reader who believes otherwise will store something
they shouldn't.

## Gate wiring

`memory-check.sh` currently greps for field names. It gains a Python path:

```sh
if python3 -c 'import quantsmith' 2>/dev/null; then
  python3 -m quantsmith.pipelines.workflow_memory --validate --decay --as-of "$(date -u +%F)"
else
  # existing grep-based checks, unchanged
fi
```

The grep path stays as the fallback for a copied scaffold with no package
installed — consistent with "gates degrade gracefully when optional tools are
missing" (`docs/handoff.md`, Conventions To Preserve). The secret/PII scan is
untouched and keeps running either way; the new `author` validation (REQ-009) is
a second, independent guard over the same property, and AC-013 pins that the two
agree rather than contradict.

## Alternatives considered

- **Add PyYAML.** Rejected: every `pipelines/` runtime is dependency-free, and
  the scaffold is copied into repos that may not install extras. The subset
  parser is ~80 lines against a fixed fixture set.
- **Store author as the raw git email.** Rejected: it puts PII in a committed
  store and would require narrowing the existing PII scan — weakening a guard to
  add a feature.
- **SQLite index alongside the Markdown/YAML.** Deferred. At the current
  store size a linear scan is instant, and a second copy of the data is a
  synchronisation problem. Revisit when a store's scan time is measurable.
- **Rewrite `memory-check.sh` entirely in Python.** Rejected: it would strand
  adopters who copy the scaffold without the package.

## Test strategy

`tests/test_workflow_memory.py`, one test per AC, named `test_..._AC_0NN`,
matching the repo's convention. The committed `memory/` store is the primary
fixture (AC-001 asserts it parses with no edits); malformed cases are built in
`tmp_path` so no broken YAML is committed. Identity tests inject a fake
environment and never touch the real git config.
