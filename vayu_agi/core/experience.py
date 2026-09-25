"""Experience records and bounded learning signals."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Experience:
    context: str
    action: str
    outcome: str
    success: bool
    timestamp: str


class ExperienceIntegrator:
    def __init__(self, cognitive_engine: Any) -> None:
        self.engine = cognitive_engine
        self.experiences: list[Experience] = []

    async def integrate_experience(self, context: str, action: str, outcome: str, success: bool) -> dict[str, Any]:
        experience = Experience(context, action, outcome, success, datetime.now(timezone.utc).isoformat())
        self.experiences.append(experience)
        return {"stored": True, "total_experiences": len(self.experiences), "success": success}

    def get_learning_report(self) -> dict[str, Any]:
        total = len(self.experiences)
        successes = sum(item.success for item in self.experiences)
        return {"total_experiences": total, "success_rate": successes / max(total, 1)}