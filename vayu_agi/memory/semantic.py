"""Small semantic fact store with contradiction detection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fact:
    subject: str
    predicate: str
    object: str
    confidence: float = 0.5
    source: str = "internal"


class SemanticMemory:
    def __init__(self) -> None:
        self.facts: list[Fact] = []

    def add_fact(self, subject: str, predicate: str, object: str, confidence: float = 0.5, source: str = "internal") -> Fact:
        fact = Fact(subject, predicate, object, max(0.0, min(confidence, 1.0)), source)
        self.facts.append(fact)
        return fact

    def search(self, query: str, limit: int = 5) -> list[Fact]:
        words = set(query.lower().split())
        return [fact for fact in self.facts if words & set(f"{fact.subject} {fact.predicate} {fact.object}".lower().split())][:limit]

    def check_consistency(self) -> list[str]:
        contradictions = []
        for index, first in enumerate(self.facts):
            for second in self.facts[index + 1:]:
                if first.subject == second.subject and first.predicate == second.predicate and first.object != second.object:
                    contradictions.append(f"{first.subject} {first.predicate} {first.object} conflicts with {second.object}")
        return contradictions