from vayu_agi.config import CognitiveConfig, VayuConfig
from vayu_agi.core.cognitive_engine import CognitiveEngine
from vayu_agi.evolution.self_improvement import SelfImprovementEngine


def test_evolution_does_nothing_without_observations() -> None:
    evolution = SelfImprovementEngine(CognitiveEngine())
    report = evolution.improve()

    assert report.changed is False
    assert report.reason == "No observations available"


def test_evolution_is_bounded() -> None:
    config = VayuConfig(cognitive=CognitiveConfig(correction_threshold=1.0))
    engine = CognitiveEngine(config)
    evolution = SelfImprovementEngine(engine)
    for _ in range(4):
        engine.think("brief")

    original = config.cognitive.analytical_depth
    report = evolution.improve()

    assert report.changed is True
    assert config.cognitive.analytical_depth <= config.evolution.max_parameter
    assert config.cognitive.analytical_depth > original