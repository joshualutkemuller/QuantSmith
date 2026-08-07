from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class UserRequest:
    """Natural-language request accepted by the CLI."""

    prompt: str
    output_format: str = "terminal"


@dataclass
class QueryPlan:
    """Execution plan produced by the orchestrator."""

    steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataArtifact:
    """Normalized dataset representation shared between agents."""

    rows: List[Dict[str, Any]]
    schema: Dict[str, str]
    lineage: List[str] = field(default_factory=list)


@dataclass
class DashboardPayload:
    """Structured dashboard payload for Tableau adapters."""

    title: str
    datasource: str
    worksheet: str
    metrics: List[str]
    dimensions: List[str]
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    """Final response returned by orchestrator."""

    plan: QueryPlan
    data: DataArtifact
    dashboard: DashboardPayload
    report: str
