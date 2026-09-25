"""Deterministic cognitive pipeline with explicit error correction."""

from __future__ import annotations

import asyncio
import hashlib
import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..config import VayuConfig
from ..reasoning.multi_path import MultiPathReasoner
from ..reasoning.synthesis import SynthesisEngine
from ..routing.router import CognitiveRouter
from ..security.privacy import PrivacyGuard, RequestRejected


class MentalState(str, Enum):
    DORMANT = "dormant"
    ATTENTIVE = "attentive"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    REFLECTIVE = "reflective"
    ERROR = "error"


@dataclass(frozen=True)
class Insight:
    mode: str
    description: str
    confidence: float
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class Correction:
    issue: str
    action: str
    applied: bool


@dataclass(frozen=True)
class CognitiveResult:
    request_id: str
    input_text: str
    synthesis: str
    confidence: float
    state: MentalState
    insights: tuple[Insight, ...] = ()
    corrections: tuple[Correction, ...] = ()
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "input": self.input_text,
            "synthesis": self.synthesis,
            "confidence": self.confidence,
            "state": self.state.value,
            "insights": [
                {
                    "mode": insight.mode,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "evidence": list(insight.evidence),
                }
                for insight in self.insights
            ],
            "corrections": [correction.__dict__ for correction in self.corrections],
            "warnings": list(self.warnings),
        }


class CognitiveEngine:
    """A local reasoning scaffold that never presents unchecked output as fact."""

    def __init__(self, config: VayuConfig | None = None) -> None:
        self.config = config or VayuConfig()
        self.state = MentalState.DORMANT
        self.router = CognitiveRouter()
        self.reasoner = MultiPathReasoner(self.config.cognitive)
        self.synthesizer = SynthesisEngine()
        self.guard = PrivacyGuard(self.config.security.max_request_chars, self.config.security.rate_limit_per_minute)
        self._lock = threading.RLock()
        self._total_requests = 0
        self._corrected_requests = 0
        self._history: list[CognitiveResult] = []

    async def think_async(self, signal: str, mode: str = "natural") -> CognitiveResult:
        return await asyncio.to_thread(self.think, signal, mode)

    def think(self, signal: str, mode: str = "natural") -> CognitiveResult:
        """Analyze a request and run correction before returning its result."""
        request_id = hashlib.sha256((signal if isinstance(signal, str) else repr(signal)).encode("utf-8")).hexdigest()[:12]
        with self._lock:
            self._total_requests += 1
            try:
                normalized, warnings = self._validate_input(signal)
                selected_mode = self._normalize_mode(mode)
                paths = self.router.select(selected_mode, normalized)
                generated = self.reasoner.generate(normalized, paths)
                synthesis_result = self.synthesizer.combine(normalized, generated)
                insights = [Insight(item.mode, item.description, item.confidence, item.evidence) for item in generated]
                synthesis, confidence = synthesis_result.text, synthesis_result.confidence
                corrections = self._correct(synthesis, confidence, insights)
                if corrections:
                    self._corrected_requests += 1
                result = CognitiveResult(
                    request_id=request_id,
                    input_text=normalized,
                    synthesis=synthesis,
                    confidence=confidence,
                    state=MentalState.REFLECTIVE if corrections else MentalState.ATTENTIVE,
                    insights=tuple(insights),
                    corrections=tuple(corrections),
                    warnings=tuple(warnings),
                )
            except ValueError as exc:
                self.state = MentalState.ERROR
                return CognitiveResult(
                    request_id=request_id,
                    input_text=signal if isinstance(signal, str) else "",
                    synthesis="The request could not be processed safely.",
                    confidence=0.0,
                    state=MentalState.ERROR,
                    warnings=(str(exc),),
                )
            self.state = result.state
            self._history.append(result)
            return result

    def _validate_input(self, signal: str) -> tuple[str, list[str]]:
        try:
            normalized = self.guard.validate(signal)
        except RequestRejected as exc:
            raise ValueError(str(exc)) from exc
        warnings = ["Input was normalized for consistent analysis."] if normalized != signal else []
        return normalized, warnings

    @staticmethod
    def _normalize_mode(mode: str) -> str:
        if not isinstance(mode, str):
            return "natural"
        mode = mode.strip().lower()
        return mode if mode in {"natural", "analytical", "creative", "intuitive", "transcendent", "reflective"} else "natural"

    def _generate_insights(self, signal: str, mode: str) -> list[Insight]:
        words = tuple(dict.fromkeys(re.findall(r"[\w'-]+", signal.lower())))
        complexity = min(len(words) / 20.0, 1.0)
        modes = [mode] if mode != "natural" else ["analytical", "creative", "reflective"]
        weights = {"analytical": self.config.cognitive.analytical_depth, "creative": self.config.cognitive.creativity, "reflective": self.config.cognitive.intuition}
        return [Insight(name, f"{name.title()} review of {len(words)} distinct terms", min(weights[name] * (0.55 + complexity * 0.45), 1.0), words[:5]) for name in modes]

    @staticmethod
    def _synthesize(signal: str, insights: list[Insight]) -> tuple[str, float]:
        confidence = sum(i.confidence for i in insights) / max(len(insights), 1)
        return f"A {len(signal.split())}-word request was examined through {', '.join(i.mode for i in insights)} perspectives.", round(confidence, 4)

    def _correct(self, synthesis: str, confidence: float, insights: list[Insight]) -> list[Correction]:
        corrections: list[Correction] = []
        if not insights:
            corrections.append(Correction("No insights were generated", "Return a low-confidence result", True))
        if confidence < self.config.cognitive.correction_threshold:
            corrections.append(Correction("Confidence below threshold", "Mark result for human review", True))
        if len(synthesis) < 20:
            corrections.append(Correction("Synthesis is too short", "Retain warning instead of inventing detail", True))
        return corrections

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {"state": self.state.value, "total_requests": self._total_requests, "corrected_requests": self._corrected_requests, "history_size": len(self._history)}

    def get_status(self) -> dict[str, Any]:
        return self.status()

    def shutdown(self) -> None:
        self.state = MentalState.DORMANT