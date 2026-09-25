"""Select reasoning modes from explicit user intent."""

from __future__ import annotations

from ..config import ThinkingMode


class CognitiveRouter:
    VALID = {mode.value for mode in ThinkingMode}

    def select(self, requested: str, text: str = "") -> list[str]:
        mode = requested.strip().lower() if isinstance(requested, str) else "natural"
        if mode not in self.VALID:
            mode = ThinkingMode.NATURAL.value
        if mode == ThinkingMode.NATURAL.value:
            return ["analytical", "creative", "reflective"]
        if mode == ThinkingMode.TRANSCENDENT.value:
            return ["creative", "intuitive", "reflective", "transcendent"]
        return [mode]