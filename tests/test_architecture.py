import asyncio
from pathlib import Path

from vayu_agi.config import VayuConfig
from vayu_agi.core.consciousness import ConsciousnessSimulator
from vayu_agi.core.experience import ExperienceIntegrator
from vayu_agi.memory import EpisodicMemory, SemanticMemory, WorkingMemory
from vayu_agi.routing import CognitiveRouter
from vayu_agi.security import PrivacyGuard, RequestRejected


def test_memory_components_have_distinct_responsibilities(tmp_path: Path) -> None:
    working = WorkingMemory(capacity=2)
    working.add("alpha context")
    assert working.search("alpha")

    episodic = EpisodicMemory(tmp_path)
    episodic.store("alpha context", "inspect", "complete", True)
    assert episodic.retrieve("alpha")

    semantic = SemanticMemory()
    semantic.add_fact("alpha", "state", "ready")
    semantic.add_fact("alpha", "state", "blocked")
    assert semantic.check_consistency()


def test_routing_and_privacy_boundaries() -> None:
    assert CognitiveRouter().select("unknown") == ["analytical", "creative", "reflective"]
    guard = PrivacyGuard(max_chars=3)
    try:
        guard.validate("four")
    except RequestRejected:
        pass
    else:
        raise AssertionError("oversized request was accepted")


def test_observability_modules_use_engine_contract(tmp_path: Path) -> None:
    from vayu_agi import CognitiveEngine

    engine = CognitiveEngine(VayuConfig(data_dir=tmp_path))
    engine.think("observe this")
    introspection = asyncio.run(ConsciousnessSimulator(engine).introspect())
    learning = asyncio.run(ExperienceIntegrator(engine).integrate_experience("context", "action", "outcome", True))

    assert introspection["engine"]["total_requests"] == 1
    assert learning["stored"] is True