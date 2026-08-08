"""Runnable reference pipelines that make specs executable.

Exposes the ``0001-daily-momentum-signal``, ``0006-ml-return-forecasting``,
``0007-portfolio-construction``,
``0008-metrics-semantic-layer``, ``0009-experimentation``,
``0010-analytics-pipeline``, ``0011-data-pipeline-orchestration``,
``0012-execution-scheduling``, ``0013-optimization-solvers``, and the dashboard
renderers (``0015`` Power BI, ``0016`` Excel and React) reference pipelines.
"""

from __future__ import annotations

from .analytics_pipeline import (
    FactSchema,
    PreparedData,
    QualityResult,
    Report,
    Table,
    prepare,
    profile_facts,
    run_pipeline,
    run_query,
)
from .dashboard_spec import (
    CHART_TYPES,
    DashboardSpec,
    DashboardSpecError,
    Panel,
)
from .data_pipeline import (
    DataContract,
    Pipeline,
    RunManifest,
    Step,
    StepResult,
    backfill,
    run,
)
from .execution_optimization import (
    ExecutionSchedule,
    optimal_schedule,
)
from .excel_profile import (
    ExcelChart,
    ExcelWorkbookPayload,
    render_excel,
)
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
from .momentum_signal import (
    PriceBar as MomentumPriceBar,
    build_signal,
    liquidity_filter,
    raw_momentum,
)
from .optimization_solvers import (
    DPProblem,
    DPResult,
    FlowResult,
    LPResult,
    min_cost_flow,
    solve_dp,
    solve_lp,
    solve_milp,
)
from .powerbi_profile import render_powerbi
from .react_profile import (
    ReactComponent,
    ReactDashboardPayload,
    render_react,
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
    # 0001 — momentum signal
    "MomentumPriceBar",
    "build_signal",
    "liquidity_filter",
    "raw_momentum",
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
    # 0010 — analytics pipeline
    "FactSchema",
    "PreparedData",
    "QualityResult",
    "Report",
    "Table",
    "prepare",
    "profile_facts",
    "run_pipeline",
    "run_query",
    # 0011 — data-pipeline orchestration
    "DataContract",
    "Pipeline",
    "RunManifest",
    "Step",
    "StepResult",
    "backfill",
    "run",
    # 0012 — execution scheduling
    "ExecutionSchedule",
    "optimal_schedule",
    # 0013 — optimization solvers
    "DPProblem",
    "DPResult",
    "FlowResult",
    "LPResult",
    "min_cost_flow",
    "solve_dp",
    "solve_lp",
    "solve_milp",
    # 0014/0015/0016 — dashboard spec + tool renderers
    "CHART_TYPES",
    "DashboardSpec",
    "DashboardSpecError",
    "Panel",
    "render_powerbi",
    "ExcelChart",
    "ExcelWorkbookPayload",
    "render_excel",
    "ReactComponent",
    "ReactDashboardPayload",
    "render_react",
]
