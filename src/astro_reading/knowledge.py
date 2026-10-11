"""A small in-memory knowledge base used for retrieval.

A Qdrant-backed implementation is planned (see docs/backlog.md). This version
needs no external service, which keeps tests and demos simple.
"""

from __future__ import annotations

import re
from pathlib import Path

_WORD = re.compile(r"\w+", re.UNICODE)
_MIN_WORD_LENGTH = 3
_MIN_PASSAGE_LENGTH = 40


def _words(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if len(w) >= _MIN_WORD_LENGTH}


class InMemoryKnowledgeBase:
    """Rank passages by how many query words they contain."""

    def __init__(self, passages: list[str]) -> None:
        self._passages = [p.strip() for p in passages if p.strip()]

    @classmethod
    def from_directory(cls, directory: Path) -> InMemoryKnowledgeBase:
        """Load .txt and .md files, splitting each one into paragraphs."""
        passages: list[str] = []
        for path in sorted(directory.glob("*")):
            if path.suffix.lower() not in {".txt", ".md"}:
                continue
            text = path.read_text(encoding="utf-8")
            for block in re.split(r"\n\s*\n", text):
                if len(block.strip()) >= _MIN_PASSAGE_LENGTH:
                    passages.append(block)
        return cls(passages)

    def __len__(self) -> int:
        return len(self._passages)

    def search(self, query: str, limit: int = 5) -> list[str]:
        query_words = _words(query)
        if not query_words:
            return []
        scored = [
            (len(query_words & _words(passage)), index, passage)
            for index, passage in enumerate(self._passages)
        ]
        scored = [item for item in scored if item[0] > 0]
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [passage for _, _, passage in scored[:limit]]
