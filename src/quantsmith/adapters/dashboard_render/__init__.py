"""Executable dashboard-render providers (spec 0017).

Turn a rendered dashboard payload (specs 0015/0016) into a live artifact:
``scaffold_react`` (pure standard library) and ``write_xlsx`` (lazy openpyxl).
"""

from __future__ import annotations

from .react_scaffold import scaffold_react
from .result import FileRecord, RenderResult, manifest
from .streamlit_scaffold import scaffold_streamlit
from .xlsx import write_xlsx

__all__ = [
    "FileRecord",
    "RenderResult",
    "manifest",
    "scaffold_react",
    "scaffold_streamlit",
    "write_xlsx",
]
