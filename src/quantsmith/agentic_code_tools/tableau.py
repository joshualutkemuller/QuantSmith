from __future__ import annotations

from typing import Dict, List

from .contracts import DashboardPayload
from .rag import KnowledgeDoc


class DashboardValidationError(ValueError):
    pass


class TableauPayloadValidator:
    """Use Pydantic when available, fallback to strict manual checks."""

    def __init__(self) -> None:
        self._use_pydantic = False
        self._model = None

        try:
            from pydantic import BaseModel

            class _DashboardModel(BaseModel):
                title: str
                datasource: str
                worksheet: str
                metrics: List[str]
                dimensions: List[str]
                filters: Dict[str, str] = {}

            self._model = _DashboardModel
            self._use_pydantic = True
        except Exception:
            self._use_pydantic = False

    def validate(self, payload: DashboardPayload) -> DashboardPayload:
        if self._use_pydantic:
            try:
                self._model(
                    title=payload.title,
                    datasource=payload.datasource,
                    worksheet=payload.worksheet,
                    metrics=payload.metrics,
                    dimensions=payload.dimensions,
                    filters=payload.filters,
                )
            except Exception as exc:  # noqa: BLE001 - normalize runtime pydantic errors
                raise DashboardValidationError(str(exc)) from exc

        if not payload.metrics:
            raise DashboardValidationError("At least one metric is required.")
        if not payload.dimensions:
            raise DashboardValidationError("At least one dimension is required.")
        return payload


class TableauDashboardAgent:
    """Create dashboard payloads from prompts + retrieved guidance."""

    def __init__(self, validator: TableauPayloadValidator) -> None:
        self.validator = validator

    def build_payload(
        self,
        prompt: str,
        datasource: str,
        available_columns: List[str],
        knowledge_docs: List[KnowledgeDoc],
    ) -> DashboardPayload:
        metrics = [c for c in available_columns if c.lower() in {"sales", "revenue", "profit", "count"}]
        dimensions = [c for c in available_columns if c not in metrics][:2] or available_columns[:1]

        if not metrics:
            metrics = [available_columns[-1]] if available_columns else ["count"]

        filters: Dict[str, str] = {}
        if "region" in prompt.lower() and "region" in {c.lower() for c in available_columns}:
            filters["region"] = "ALL"

        worksheet_name = knowledge_docs[0].title if knowledge_docs else "Auto Worksheet"

        payload = DashboardPayload(
            title=f"Auto Dashboard: {prompt[:40]}",
            datasource=datasource,
            worksheet=worksheet_name,
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
        )
        return self.validator.validate(payload)
