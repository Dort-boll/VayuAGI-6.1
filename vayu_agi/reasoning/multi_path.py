"""Deterministic multi-perspective insight generation."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..config import CognitiveParams


@dataclass(frozen=True)
class PathInsight:
    mode: str
    description: str
    confidence: float
    evidence: tuple[str, ...]


class MultiPathReasoner:
    """Generates inspectable paths without claiming external knowledge."""

    def __init__(self, params: CognitiveParams) -> None:
        self.params = params

    def generate(self, text: str, modes: list[str]) -> list[PathInsight]:
        words = tuple(dict.fromkeys(re.findall(r"[\w'-]+", text.lower())))
        complexity = min(len(words) / 20, 1.0)
        weights = {
            "analytical": self.params.analytical_depth,
            "creative": self.params.creativity_flow,
            "intuitive": self.params.intuition_strength,
            "reflective": self.params.memory_integration,
            "transcendent": self.params.transcendence_capacity,
        }
        return [
            PathInsight(
                mode=mode,
                description=f"{mode.title()} review of {len(words)} distinct terms",
                confidence=round(min(weights.get(mode, 0.5) * (0.55 + complexity * 0.45), 1.0), 4),
                evidence=words[:5],
            )
            for mode in modes
        ]