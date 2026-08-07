# Evening Quant Content Memory

Workflow-specific memory for the evening content pipeline. It stores metadata about
style, prior themes, hooks, formats, visual concepts, meme templates, and rejected
framing. It does not store raw social metrics, credentials, private desk context,
client details, MNPI, or source data rows.

- `index.yaml` catalogs memory records.
- `themes.md` tracks topics and hooks already used.
- `style_preferences.md` captures stable voice and format preferences.
- `rejected_framing.md` records risky or stale framing to avoid.
- `visual_playbook.md` tracks visual concepts, chart types, and caveats.

Facts about datasets and sources live under `memory/_shared/`; this folder records
how the evening content workflow uses them.