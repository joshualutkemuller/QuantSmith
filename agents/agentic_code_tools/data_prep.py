from __future__ import annotations

from typing import Any, Dict, List

from .contracts import DataArtifact


class DataPrepAgent:
    """Apply deterministic cleaning and simple transformations."""

    def clean(self, artifact: DataArtifact) -> DataArtifact:
        cleaned_rows: List[Dict[str, Any]] = []
        for row in artifact.rows:
            cleaned = {k: v for k, v in row.items() if v is not None}
            cleaned_rows.append(cleaned)

        lineage = artifact.lineage + ["data_prep:drop_null_fields"]
        schema = {k: type(v).__name__ for k, v in cleaned_rows[0].items()} if cleaned_rows else artifact.schema
        return DataArtifact(rows=cleaned_rows, schema=schema, lineage=lineage)
