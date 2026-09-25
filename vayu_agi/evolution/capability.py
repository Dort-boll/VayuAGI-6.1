"""Observable capability registry; it never mutates engine code."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    name: str
    strength: float
    emergent: bool = False


class CapabilityEvolver:
    def __init__(self, cognitive_engine: object) -> None:
        self.engine = cognitive_engine
        self.capabilities = {
            "analytical_reasoning": Capability("analytical_reasoning", 0.8),
            "creative_synthesis": Capability("creative_synthesis", 0.7),
            "error_correction": Capability("error_correction", 0.8),
        }

    def get_capability_report(self) -> dict[str, object]:
        return {"total_capabilities": len(self.capabilities), "capabilities": [cap.__dict__ for cap in self.capabilities.values()]}