"""Configuration with validation and conservative defaults."""

from dataclasses import dataclass, field
from pathlib import Path


def _bounded(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass
class CognitiveConfig:
    analytical_depth: float = 0.8
    creativity: float = 0.7
    intuition: float = 0.6
    correction_threshold: float = 0.6
    max_input_chars: int = 10_000

    def __post_init__(self) -> None:
        for name in ("analytical_depth", "creativity", "intuition", "correction_threshold"):
            setattr(self, name, _bounded(getattr(self, name), name))
        if self.max_input_chars < 1:
            raise ValueError("max_input_chars must be positive")


@dataclass
class EvolutionConfig:
    enabled: bool = True
    learning_rate: float = 0.05
    max_parameter: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 < self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be greater than 0 and at most 1")
        _bounded(self.max_parameter, "max_parameter")


@dataclass
class VayuConfig:
    data_dir: Path = field(default_factory=lambda: Path.home() / ".vayu_agi")
    cognitive: CognitiveConfig = field(default_factory=CognitiveConfig)
    evolution: EvolutionConfig = field(default_factory=EvolutionConfig)

    def prepare(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)