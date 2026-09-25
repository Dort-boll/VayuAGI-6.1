"""Combine independent insights without fabricating unsupported detail."""

from __future__ import annotations

from dataclasses import dataclass

from .multi_path import PathInsight


@dataclass(frozen=True)
class Synthesis:
    text: str
    confidence: float
    modes: tuple[str, ...]


class SynthesisEngine:
    def combine(self, text: str, insights: list[PathInsight]) -> Synthesis:
        confidence = sum(item.confidence for item in insights) / max(len(insights), 1)
        modes = tuple(dict.fromkeys(item.mode for item in insights))
        return Synthesis(
            text=f"A {len(text.split())}-word request was examined through {', '.join(modes)} perspectives.",
            confidence=round(confidence, 4),
            modes=modes,
        )