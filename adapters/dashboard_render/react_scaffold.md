# React Scaffold Dashboard Render Adapter

## Use For

- Delivering a governed dashboard as a runnable React web app.
- Standing up a web dashboard that stays consistent with the Power BI / Excel versions.
- Repository examples and spec evidence of a rendered web dashboard.

## Input

A `ReactDashboardPayload` from `render_react` (spec `0016`,
`src/quantsmith/pipelines/react_profile.py`): `title`, `dataset`, `page`, `components`
(each with a React `component` name and props carrying the governed `metric`,
`dimensions`, and `title`), a grid `layout`, and `filters`.

## Generation Rules

- Scaffold a minimal React project deterministically: `package.json` with a pinned
  lockfile, `src/Dashboard.jsx` (or `.tsx`) rendering one component per payload entry
  at its grid position, and a `src/components/` index mapping component names to a
  chart library.
- Fetch data through a governed endpoint derived from `dataset_source` (a
  `data_access/` adapter); never bake raw data or secrets into the client bundle —
  API keys and connection details stay server-side (P9).
- Carry the governed `metric` into each component's props; do not add components or
  invent metrics beyond the payload.
- Emit accessible markup by default: ARIA roles, labels, sufficient contrast, and
  non-color encodings, per the `dataviz` skill and the `tooling/react` agent.
- Handle loading, error, and empty states in the generated data hook.
- Use deterministic filenames and stable ordering so the same payload scaffolds the
  same source tree; produce a reproducible build (committed lockfile).

## Result Evidence

Capture the scaffold directory path, a manifest of generated files with checksums, the
component count, and classification. On `dry_run`, list the files that would be written
without creating them.

## Notes

- The scaffold presents governed results fetched from an API; it does not recompute
  metrics client-side.
- Publishing/hosting the built app is a separate deployment step (a scheduler or CI
  adapter), not this adapter.
