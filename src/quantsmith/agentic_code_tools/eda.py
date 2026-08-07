from __future__ import annotations

from typing import Dict, List

from .contracts import DataArtifact, EDAReport


class EDAAgent:
    """Generate lightweight exploratory data analysis summaries."""

    def analyze(self, artifact: DataArtifact) -> EDAReport:
        row_count = len(artifact.rows)
        columns = list(artifact.schema.keys())

        numeric_columns: List[str] = []
        for col, dtype in artifact.schema.items():
            if dtype in {"int", "float", "int64", "float64"}:
                numeric_columns.append(col)

        profile: Dict[str, Dict[str, float]] = {}
        for col in numeric_columns:
            values = [r[col] for r in artifact.rows if isinstance(r.get(col), (int, float))]
            if values:
                profile[col] = {
                    "min": float(min(values)),
                    "max": float(max(values)),
                    "mean": float(sum(values) / len(values)),
                }

        insights = [
            f"Rows analyzed: {row_count}",
            f"Columns detected: {', '.join(columns) if columns else 'none'}",
            f"Numeric profile generated for {len(profile)} columns",
        ]

        return EDAReport(
            row_count=row_count,
            columns=columns,
            numeric_profile=profile,
            insights=insights,
        )
