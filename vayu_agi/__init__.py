"""VayuAGI: a local-first, inspectable cognitive architecture."""

from .config import VayuConfig
from .core.cognitive_engine import CognitiveEngine, CognitiveResult

__version__ = "6.1.0"
__all__ = ["CognitiveEngine", "CognitiveResult", "VayuConfig"]