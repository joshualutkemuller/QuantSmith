from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class KnowledgeDoc:
    title: str
    tags: List[str]
    content: str


class SimpleRAGStore:
    """Tiny file-backed retrieval store for dashboard best practices."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.docs = self._load_docs()

    def _load_docs(self) -> List[KnowledgeDoc]:
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text())
        return [KnowledgeDoc(**doc) for doc in payload]

    def retrieve(self, query: str, top_k: int = 3) -> List[KnowledgeDoc]:
        query_terms = {term.lower() for term in query.split() if term.strip()}
        scored = []
        for doc in self.docs:
            haystack = f"{doc.title} {' '.join(doc.tags)} {doc.content}".lower()
            score = sum(term in haystack for term in query_terms)
            if score:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]
