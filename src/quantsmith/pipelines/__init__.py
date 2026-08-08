"""Runnable reference pipelines that make specs executable.

Exposes the ``0006-ml-return-forecasting``, ``0007-portfolio-construction``,
``0008-metrics-semantic-layer``, and ``0009-experimentation`` reference pipelines.
"""

from __future__ import annotations

from .experimentation import (
    ExperimentReadout,
    ProportionTest,
    analyze_experiment,
    analyze_proportions,
    required_sample_size,
    sample_ratio_mismatch,
)
from .metrics_semantic_layer import (
    Fact,
    GovernanceError,
    MetricDefinition,
    SemanticLayer,
)
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
    # 0008 — metrics semantic layer
    "Fact",
    "GovernanceError",
    "MetricDefinition",
    "SemanticLayer",
    # 0009 — experimentation
    "ExperimentReadout",
    "ProportionTest",
    "analyze_experiment",
    "analyze_proportions",
    "required_sample_size",
    "sample_ratio_mismatch",
]
