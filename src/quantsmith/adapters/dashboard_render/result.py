"""Shared result types for dashboard-render providers.

Mirrors the ``adapters/dashboard_render/adapter_contract.md`` output: a status, an
artifact URI, and an evidence manifest of generated files with checksums.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class FileRecord:
    path: str
    checksum: str   # sha256 hex of the content ("" when planned but not written)
    bytes: int


@dataclass(frozen=True)
class RenderResult:
    adapter_name: str
    provider: str                       # "react_scaffold" | "xlsx"
    status: str                         # "generated" | "planned" | "skipped" | "failed"
    artifact_uri: Optional[str]
    files: Tuple[FileRecord, ...] = field(default_factory=tuple)
    dry_run: bool = False

    def paths(self) -> List[str]:
        return [f.path for f in self.files]


def manifest(files: Dict[str, str]) -> Tuple[FileRecord, ...]:
    """Deterministic manifest: one FileRecord per (relative path, content), path-sorted."""
    records = []
    for path in sorted(files):
        content = files[path]
        data = content.encode("utf-8")
        records.append(
            FileRecord(path=path, checksum=hashlib.sha256(data).hexdigest(), bytes=len(data))
        )
    return tuple(records)


def contains_secret(text: str) -> bool:
    """Conservative check for an embedded credential value in generated content.

    Matches credential-shaped tokens (assignments, bearer headers, key material), not
    the mere mention of the words "secret" or "password" in documentation prose.
    """
    lowered = text.lower()
    needles = (
        "api_key", "apikey", "secret_key", "client_secret", "aws_secret",
        "authorization: bearer ", "password=", "passwd=", "-----begin ",
    )
    return any(n in lowered for n in needles)
