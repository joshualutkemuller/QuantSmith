# QuantSmith Twitter Visual Style Presets

These presets are the approved visual system for ThatQuantGuy/QuantSmith Twitter content. The controlling workflow in `SKILL.md` must resolve a `visual_style` before any publication-ready visual is drafted, generated, or handed off for design.

## Selection contract

Allowed style IDs:

- `terminal`
- `institutional-research`
- `minimalist-quant`
- `user-specified` — only when the user explicitly requests another visual treatment.

If a visual does not materially improve the content, return **No visual**. Never silently invent a fourth house style or blend presets into an inconsistent hybrid.

## `terminal`

**Intent:** A sober institutional quant terminal or research console. It should feel like a production analytics surface, not science fiction.

**Canvas:** Near-black, charcoal, or another dark neutral. Subtle grid or panel structure is acceptable only when it helps organize information.

**Typography:** Monospace-first. Compact hierarchy. Use small caps/status labels sparingly. Avoid oversized marketing headlines.

**Charts and data:** Thin axes and line geometry, exact labels, concise legends, and source/date footer for data-driven work. Dense information is acceptable when it remains immediately legible.

**Accent:** One restrained highlight accent. Do not create rainbow encoding unless the data genuinely requires categorical separation.

**Layout:** Modular panels, terminal-like labels, analytical tables, system diagrams, or compact charts. Prioritize information architecture over decoration.

**Best for:** AI infrastructure and compute, optimization, model internals, production ML, systems, market plumbing, securities finance mechanics, dense analytical tables, technical diagrams, routing, collateral/cash/inventory problems, and operational research.

**Avoid:** Cyberpunk neon, Matrix motifs, fake code, hacker clichés, excessive glow, decorative command prompts, sci-fi HUD elements, gratuitous grids, and illegible density.

**Prompt seed:**

> Design as a sober institutional quant terminal/research console, not sci-fi. Use a near-black neutral canvas, monospace-first typography, compact analytical hierarchy, thin chart geometry, restrained single accent, exact labels, and high information density without clutter. Avoid cyberpunk neon, fake code, Matrix motifs, glossy HUD styling, and decorative noise.

## `institutional-research`

**Intent:** A publishable institutional research chart or research-note visual that could sit naturally in a rigorous macro, equity, rates, or cross-asset report.

**Canvas:** White, off-white, or another light neutral background.

**Typography:** Clean sans-serif. Establish hierarchy through size and weight rather than ornamentation.

**Charts and data:** Precise axes, units, periods, labels, and scales. Annotate only turning points or comparisons that advance the thesis. Include source and as-of/release date in the footer for empirical visuals.

**Layout:** Analytical headline, concise subtitle when useful, primary chart or comparison, limited annotations, and a source/date footer. Prefer one dominant chart over a dashboard of small panels unless the thesis requires multiple views.

**Best for:** Macro, rates, inflation, labor, earnings, valuation, company comparisons, capital allocation, AI capex/ROIC, factor evidence, empirical market structure, time series, cross-sectional comparisons, and sourced quantitative claims.

**Avoid:** Glossy marketing visuals, ornamental illustrations, decorative gradients, 3D bars, oversized logos, chartjunk, unnecessary icons, vague axes, and unsupported callouts.

**Prompt seed:**

> Design as a polished institutional research chart. Use a light neutral canvas, restrained sans-serif typography, a clear analytical headline, precise chart axes and units, only decision-useful annotations, and a source/date footer. Favor evidence and hierarchy over decoration. Avoid glossy marketing treatment, gradients, 3D effects, clip-art, and chartjunk.

## `minimalist-quant`

**Intent:** Communicate one quantitative idea with maximum signal-to-ink. The viewer should understand the thesis within roughly three seconds.

**Canvas:** Plain light or dark neutral with substantial whitespace.

**Typography:** Clean and sharp. A single equation, key metric, short phrase, or comparison may dominate the composition.

**Charts and data:** Prefer one relationship, one series, one distribution, or one comparison. Remove labels that are not necessary to interpret the thesis.

**Layout:** One claim, one visual anchor, optional short annotation. No competing panels unless the comparison itself is the point.

**Best for:** Equations, optimization intuition, probability/statistics concepts, one surprising comparison, one relationship, one key number, portfolio intuition, educational quant content, and concise conceptual posts.

**Avoid:** Dashboards, dense legends, multiple competing panels, decorative illustration, excessive annotation, badges, repeated metrics, and anything that dilutes the single quantitative idea.

**Prompt seed:**

> Design a minimalist quant card: one thesis, one visual anchor, high whitespace, extremely restrained labels, no decorative elements, and a clean quantitative hierarchy. Make the equation, relationship, or key comparison visually dominant. Remove anything that does not improve comprehension.

## Routing guidance

Use `terminal` when the content is primarily about a system, process, optimizer, technical mechanism, infrastructure stack, production model, market plumbing, or dense operational state.

Use `institutional-research` when the visual's credibility depends on sourced empirical evidence such as market data, macro releases, earnings, valuation, rates, company comparisons, time series, or cross-sectional results.

Use `minimalist-quant` when the thesis can be reduced to one equation, concept, relationship, distribution, key number, or surprising comparison.

If two presets are plausible, choose based on the *job of the visual*, not merely the topic. For example, an AI infrastructure post showing a sourced capex time series should generally use `institutional-research`; a schematic of the compute/power/network constraint stack should use `terminal`; a single marginal-ROIC equation should use `minimalist-quant`.

An explicit user request for another treatment takes precedence and must be labeled `user-specified` in the brief.

## Shared QuantSmith visual rules

Across all presets:

- The quantitative thesis must be obvious before secondary detail.
- Use exact units, periods, and labels.
- Do not visually overstate precision or causality.
- For current/data-driven visuals, include the source and as-of/release date when feasible.
- Label conceptual or illustrative charts clearly.
- Never fabricate observations, estimates, or missing chart points.
- Prefer annotations that explain mechanism or surprise, not annotations that merely restate values.
- Maintain enough contrast and font size for mobile viewing on X.
- Do not imitate Bloomberg or another vendor's proprietary branding/trade dress.
- Avoid generic AI gradients, chartjunk, glossy 3D effects, clip-art, ornamental icons, decorative noise, and unnecessary dashboards.
- Provide concise alt text for every publication-ready visual.

## Visual brief template

Use this contract whenever a visual is recommended:

```text
Visual style: <terminal | institutional-research | minimalist-quant | user-specified>
Format: <chart | infographic | diagram | meme | quant card>
Thesis: <one sentence>
Canvas/layout: <preset-compliant description>
Data/source: <source + as-of/release date, or Conceptual>
Axes/variables: <when applicable>
Annotations: <only thesis-relevant callouts>
Caveat: <when applicable>
Alt text: <concise accessible description>
```

## Pre-publication validation

A visual is not publication-ready until all of the following are true:

- A valid style ID is stated, or the workflow explicitly returns **No visual**.
- The thesis is understandable within roughly three seconds.
- Canvas, typography, hierarchy, density, chart treatment, and annotations match the selected preset.
- Numeric labels, signs, units, denominators, periods, and scales are correct.
- Source/date is shown when the visual is data-based and it is feasible to include it.
- Conceptual visuals are labeled as conceptual.
- No visual element introduces an unsupported factual or causal claim.
- Alt text is included.
- None of the selected preset's anti-patterns are present.
