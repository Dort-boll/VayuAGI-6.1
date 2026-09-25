import asyncio

from vayu_agi.config import CognitiveConfig, VayuConfig
from vayu_agi.core.cognitive_engine import CognitiveEngine, MentalState


def test_low_confidence_result_is_corrected() -> None:
    engine = CognitiveEngine(VayuConfig(cognitive=CognitiveConfig(correction_threshold=0.9)))
    result = engine.think("short request", "analytical")

    assert result.state is MentalState.REFLECTIVE
    assert any(c.issue == "Confidence below threshold" for c in result.corrections)
    assert result.confidence < 0.9


def test_invalid_input_is_safe_and_structured() -> None:
    result = CognitiveEngine().think("   ")

    assert result.state is MentalState.ERROR
    assert result.confidence == 0.0
    assert result.warnings


def test_async_and_sync_paths_have_same_contract() -> None:
    engine = CognitiveEngine()
    sync_result = engine.think("build a reliable system")
    async_result = asyncio.run(engine.think_async("build a reliable system"))

    assert sync_result.synthesis == async_result.synthesis
    assert sync_result.confidence == async_result.confidence


def test_input_is_normalized_and_warned() -> None:
    result = CognitiveEngine().think("  two   words  ")

    assert result.input_text == "two words"
    assert result.warnings == ("Input was normalized for consistent analysis.",)