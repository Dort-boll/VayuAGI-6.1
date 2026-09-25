"""Bounded short-term context memory."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkingMemoryItem:
    content: str
    kind: str = "thought"
    relevance: float = 0.5


class WorkingMemory:
    def __init__(self, capacity: int = 100) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._items: deque[WorkingMemoryItem] = deque(maxlen=capacity)

    def add(self, content: str, kind: str = "thought", relevance: float = 0.5) -> None:
        if not content.strip():
            raise ValueError("content must not be empty")
        self._items.append(WorkingMemoryItem(content.strip(), kind, max(0.0, min(relevance, 1.0))))

    def recent(self, limit: int = 5) -> list[WorkingMemoryItem]:
        return list(self._items)[-max(limit, 0):]

    def search(self, query: str, limit: int = 5) -> list[WorkingMemoryItem]:
        query_words = set(query.lower().split())
        ranked = sorted(self._items, key=lambda item: len(query_words & set(item.content.lower().split())) * item.relevance, reverse=True)
        return [item for item in ranked if query_words & set(item.content.lower().split())][:limit]

    def clear(self) -> None:
        self._items.clear()

    def status(self) -> dict[str, int]:
        return {"capacity": self.capacity, "current_items": len(self._items)}