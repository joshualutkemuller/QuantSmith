from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class WorkflowMode:
    name: str
    focus: str
    preferred_metrics: List[str]
    preferred_dimensions: List[str]


MODES: Dict[str, WorkflowMode] = {
    "general": WorkflowMode(
        name="general",
        focus="Broad analytics workflow",
        preferred_metrics=["sales", "profit"],
        preferred_dimensions=["region", "segment"],
    ),
    "portfolio_management": WorkflowMode(
        name="portfolio_management",
        focus="Allocations, exposures, performance attribution, and risk views",
        preferred_metrics=["allocation", "exposure", "performance", "risk"],
        preferred_dimensions=["client", "asset_class", "strategy"],
    ),
    "securities_lending_collateral": WorkflowMode(
        name="securities_lending_collateral",
        focus="Lending balances, collateral quality, utilization, and concentration",
        preferred_metrics=["loan_balance", "collateral_value", "utilization", "haircut"],
        preferred_dimensions=["counterparty", "collateral_type", "security"],
    ),
    "sales_specialist": WorkflowMode(
        name="sales_specialist",
        focus="Revenue trends, conversion, and territory segmentation",
        preferred_metrics=["sales", "revenue", "margin"],
        preferred_dimensions=["region", "segment", "rep"],
    ),
    "broad_data_scientist": WorkflowMode(
        name="broad_data_scientist",
        focus="Flexible exploratory analysis and feature discovery",
        preferred_metrics=["count", "mean", "variance"],
        preferred_dimensions=["time", "category", "cohort"],
    ),
}


def resolve_mode(prompt: str, explicit_mode: str | None = None) -> WorkflowMode:
    if explicit_mode and explicit_mode in MODES:
        return MODES[explicit_mode]

    lowered = prompt.lower()
    if "portfolio" in lowered:
        return MODES["portfolio_management"]
    if "securities lending" in lowered or "collateral" in lowered:
        return MODES["securities_lending_collateral"]
    if "sales" in lowered:
        return MODES["sales_specialist"]
    if "data scientist" in lowered or "eda" in lowered:
        return MODES["broad_data_scientist"]
    return MODES["general"]
