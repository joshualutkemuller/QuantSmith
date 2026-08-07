# Reference Pipelines

Runnable, dependency-free reference implementations that make specs *executable*.
Each pipeline demonstrates a spec's leakage-safe contracts so its acceptance
criteria can be tested anywhere (standard library only — no numpy, pandas, or
deep-learning runtime).

## `return_forecasting` — spec `0006-ml-return-forecasting`

A cross-sectional short-horizon return forecast that routes the ML build chain with
a deep-learning challenger. It implements the spec's contracts:

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `build_labels` | REQ-001 / AC-001 | Forward excess-return labels use only returns realized strictly after the decision day. |
| `FeatureStore` | REQ-002 / AC-002 | One as-of code path for offline and online reads — parity by construction. |
| `make_folds` | REQ-003 / AC-003 | Purged + embargoed walk-forward; no train label reaches a test decision day. |
| `train_baseline` | REQ-004 | Closed-form ridge model — reference stand-in for gradient-boosted trees. |
| `train_challenger` | REQ-005 | Seeded gradient-descent model — reference stand-in for the deep temporal model. |
| `evaluate` | NFR-003 / AC-004 | Rank IC plus a net-of-cost score with turnover, on identical test rows. |
| `monitor` | REQ-006 / AC-005 | Drift, calibration, decay, and a retraining trigger with explicit thresholds. |
| `run_forecast` | — | Composes the whole walk-forward run over a price panel. |

The two model functions are deliberately simple stand-ins; a production build swaps
them for real models (gradient-boosted trees, a deep temporal network) while keeping
the surrounding labels/features/folds/evaluation/monitoring contracts intact.

Tests: `tests/test_return_forecasting.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_return_forecasting.py -q
```

## `portfolio_construction` — spec `0007-portfolio-construction`

Turns the `0006` forecast into portfolio weights by solving a constrained
mean-variance QP with projection onto the feasible set (budget, per-name box bounds,
gross-exposure cap, turnover penalty). Deterministic and dependency-free.

| Component | Spec | What it guarantees |
| --- | --- | --- |
| `solve_portfolio` | REQ-001 / NFR-001 | Deterministic projected-gradient solve of the mean-variance objective. |
| `ConstraintSet` + `_project` | REQ-002 / NFR-002 / AC-002 | Weights stay feasible (budget, box, gross) by construction. |
| turnover penalty | REQ-003 / AC-003 | Rebalancing cost controlled against a prior portfolio. |
| `diagnostics` | REQ-004 / AC-004 | Objective, max constraint violation, and a risk-aversion sensitivity curve. |

The solver is a focused reference for the mean-variance form; the closed-form
frontier in `quant/mean_variance.py` remains the unconstrained counterpart.

Tests: `tests/test_portfolio_construction.py` (one test per acceptance criterion).

```sh
PYTHONPATH=src python3 -m pytest tests/test_portfolio_construction.py -q
```
