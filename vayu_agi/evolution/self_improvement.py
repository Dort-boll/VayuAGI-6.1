"""Conservative self-improvement based on observed correction rates."""

from __future__ import annotations

from dataclasses import dataclass

from ..core.cognitive_engine import CognitiveEngine


@dataclass(frozen=True)
class ImprovementReport:
    changed: bool
    reason: str
    parameter: str | None = None


class SelfImprovementEngine:
    def __init__(self, engine: CognitiveEngine) -> None:
        self.engine = engine
        self.generation = 0

    def improve(self) -> ImprovementReport:
        self.generation += 1
        if not self.engine.config.evolution.enabled:
            return ImprovementReport(False, "Evolution is disabled")
        status = self.engine.status()
        if status["total_requests"] == 0:
            return ImprovementReport(False, "No observations available")
        rate = status["corrected_requests"] / status["total_requests"]
        if rate <= 0.5:
            return ImprovementReport(False, "Correction rate is within tolerance")
        config = self.engine.config.cognitive
        old = config.analytical_depth
        config.analytical_depth = min(old + self.engine.config.evolution.learning_rate, self.engine.config.evolution.max_parameter)
        return ImprovementReport(True, "Raised analytical review weight", "analytical_depth")