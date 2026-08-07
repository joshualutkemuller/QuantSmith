"""Runnable reference pipelines that make specs executable.

Exposes the ``0006-ml-return-forecasting`` and ``0007-portfolio-construction``
reference pipelines.
"""

from __future__ import annotations

from .portfolio_construction import (
    ConstraintSet,
    diagnostics,
    gross_exposure,
    portfolio_alpha,
    portfolio_variance,
    solve_portfolio,
    turnover,
)
from .return_forecasting import (
    EvalResult,
    FeatureConfig,
    FeatureStore,
    Fold,
    ForecastRun,
    LinearModel,
    PriceBar,
    build_labels,
    evaluate,
    make_folds,
    monitor,
    run_forecast,
    train_baseline,
    train_challenger,
)

__all__ = [
    # 0006 — return forecasting
    "EvalResult",
    "FeatureConfig",
    "FeatureStore",
    "Fold",
    "ForecastRun",
    "LinearModel",
    "PriceBar",
    "build_labels",
    "evaluate",
    "make_folds",
    "monitor",
    "run_forecast",
    "train_baseline",
    "train_challenger",
    # 0007 — portfolio construction
    "ConstraintSet",
    "diagnostics",
    "gross_exposure",
    "portfolio_alpha",
    "portfolio_variance",
    "solve_portfolio",
    "turnover",
]
