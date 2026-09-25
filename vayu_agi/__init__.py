"""VayuAGI: a local-first, inspectable cognitive architecture."""

from .config import (
	CONFIG,
	CognitiveConfig,
	CognitiveParams,
	EvolutionConfig,
	EvolutionParams,
	GUIParams,
	MemoryParams,
	ThinkingMode,
	VayuConfig,
)
from .core.cognitive_engine import CognitiveEngine, CognitiveResult, MentalState
from .evolution.self_improvement import ImprovementReport, SelfImprovementEngine
from .memory import EpisodicMemory, SemanticMemory, WorkingMemory

__version__ = "6.1.0"
__all__ = [
	"CONFIG",
	"CognitiveConfig",
	"CognitiveEngine",
	"CognitiveParams",
	"CognitiveResult",
	"EpisodicMemory",
	"EvolutionConfig",
	"EvolutionParams",
	"GUIParams",
	"ImprovementReport",
	"MentalState",
	"MemoryParams",
	"SemanticMemory",
	"SelfImprovementEngine",
	"ThinkingMode",
	"VayuConfig",
	"WorkingMemory",
]