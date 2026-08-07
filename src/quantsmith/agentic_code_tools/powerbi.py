from __future__ import annotations

from typing import Dict, List

from .contracts import PowerBIPayload
from .rag import KnowledgeDoc


class PowerBIValidationError(ValueError):
    pass


class PowerBIPayloadValidator:
    """Validate PowerBI payload schemas with optional pydantic enforcement."""

    def __init__(self) -> None:
        self._use_pydantic = False
        self._model = None

        try:
            from pydantic import BaseModel

            class _PowerBIModel(BaseModel):
                title: str
                dataset: str
                report_page: str
                visuals: List[str]
                measures: List[str]
                filters: Dict[str, str] = {}

            self._model = _PowerBIModel
            self._use_pydantic = True
        except Exception:
            self._use_pydantic = False

    def validate(self, payload: PowerBIPayload) -> PowerBIPayload:
        if self._use_pydantic:
            try:
                self._model(
                    title=payload.title,
                    dataset=payload.dataset,
                    report_page=payload.report_page,
                    visuals=payload.visuals,
                    measures=payload.measures,
                    filters=payload.filters,
                )
            except Exception as exc:  # noqa: BLE001
                raise PowerBIValidationError(str(exc)) from exc

        if not payload.visuals:
            raise PowerBIValidationError("At least one visual is required.")
        if not payload.measures:
            raise PowerBIValidationError("At least one measure is required.")
        return payload


class PowerBIDashboardAgent:
    """Build PowerBI report payloads from prompt + retrieved guidance."""

    def __init__(self, validator: PowerBIPayloadValidator) -> None:
        self.validator = validator

    def build_payload(
        self,
        prompt: str,
        dataset: str,
        available_columns: List[str],
        knowledge_docs: List[KnowledgeDoc],
    ) -> PowerBIPayload:
        measures = [c for c in available_columns if c.lower() in {"sales", "revenue", "profit", "exposure", "allocation"}]
        if not measures:
            measures = [available_columns[-1]] if available_columns else ["count"]

        visuals = ["clustered_column", "line", "matrix"]
        if "risk" in prompt.lower():
            visuals.append("gauge")

        filters: Dict[str, str] = {}
        if "client" in prompt.lower() and "segment" in {c.lower() for c in available_columns}:
            filters["segment"] = "ALL"

        page_name = knowledge_docs[0].title if knowledge_docs else "Auto Report Page"

        payload = PowerBIPayload(
            title=f"PowerBI Report: {prompt[:40]}",
            dataset=dataset,
            report_page=page_name,
            visuals=visuals,
            measures=measures,
            filters=filters,
        )
        return self.validator.validate(payload)
