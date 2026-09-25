"""Single source of truth for VayuAGI configuration."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ThinkingMode(str, Enum):
    NATURAL = "natural"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    INTUITIVE = "intuitive"
    TRANSCENDENT = "transcendent"


def _bounded(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass
class CognitiveParams:
    attention_span: float = 0.8
    creativity_flow: float = 0.7
    analytical_depth: float = 0.8
    intuition_strength: float = 0.6
    memory_integration: float = 0.7
    association_radius: float = 0.5
    insight_threshold: float = 0.6
    transcendence_capacity: float = 0.4
    pattern_sensitivity: float = 0.6
    abstraction_level: float = 0.7
    correction_threshold: float = 0.6
    max_input_chars: int = 10_000

    @property
    def creativity(self) -> float:
        return self.creativity_flow

    @property
    def intuition(self) -> float:
        return self.intuition_strength

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def update_param(self, name: str, value: float) -> bool:
        if not hasattr(self, name) or name.startswith("_"):
            return False
        setattr(self, name, _bounded(value, name))
        return True

    def __post_init__(self) -> None:
        for name, value in self.to_dict().items():
            if name != "max_input_chars":
                _bounded(value, name)
        if self.max_input_chars < 1:
            raise ValueError("max_input_chars must be positive")


@dataclass
class CognitiveConfig(CognitiveParams):
    """Backward-compatible name for the cognitive parameter group."""


@dataclass
class EvolutionParams:
    enabled: bool = True
    interval: int = 30
    aggressiveness: float = 0.5
    risk_tolerance: float = 0.2
    exploration_bias: float = 0.6
    learning_rate: float = 0.05
    max_parameter: float = 1.0
    max_modifications_per_cycle: int = 3
    retain_successful: bool = True
    revert_failures: bool = True

    def __post_init__(self) -> None:
        if self.interval < 1 or self.max_modifications_per_cycle < 1:
            raise ValueError("evolution limits must be positive")
        for name in ("aggressiveness", "risk_tolerance", "exploration_bias", "learning_rate", "max_parameter"):
            _bounded(getattr(self, name), name)


@dataclass
class EvolutionConfig(EvolutionParams):
    """Backward-compatible name for evolution settings."""


@dataclass
class GUIParams:
    theme: str = "dark"
    width: int = 1400
    height: int = 900
    font_size: int = 12
    accent: str = "#14B8A6"
    auto_update_stats: bool = True
    update_interval: int = 5


@dataclass
class MemoryParams:
    working_size: int = 100
    episodic_ttl: int = 604800
    semantic_persist: bool = True
    retrieval_limit: int = 10


@dataclass
class SecurityParams:
    local_only: bool = True
    max_request_chars: int = 10_000
    rate_limit_per_minute: int = 60


@dataclass
class VayuConfig:
    data_dir: Path = field(default_factory=lambda: Path.home() / ".vayu_agi")
    cognitive: CognitiveParams = field(default_factory=CognitiveParams)
    evolution: EvolutionParams = field(default_factory=EvolutionParams)
    gui: GUIParams = field(default_factory=GUIParams)
    memory: MemoryParams = field(default_factory=MemoryParams)
    security: SecurityParams = field(default_factory=SecurityParams)
    endpoint: str = "http://localhost:11434"
    default_model: str = "qwen2.5"
    debug: bool = False

    def __post_init__(self) -> None:
        self.prepare()

    @property
    def memory_dir(self) -> Path:
        return self.data_dir / "memory"

    def prepare(self) -> None:
        for directory in (self.data_dir, self.data_dir / "logs", self.memory_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["data_dir"] = str(self.data_dir)
        return data

    def save(self, path: Path | None = None) -> Path:
        target = path or self.data_dir / "config.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return target

    @classmethod
    def load(cls, path: Path) -> "VayuConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["data_dir"] = Path(data.get("data_dir", Path.home() / ".vayu_agi"))
        groups = {"cognitive": CognitiveParams, "evolution": EvolutionParams, "gui": GUIParams, "memory": MemoryParams, "security": SecurityParams}
        for name, group_type in groups.items():
            if name in data:
                data[name] = group_type(**data[name])
        allowed = set(cls.__dataclass_fields__)
        return cls(**{key: value for key, value in data.items() if key in allowed})


CONFIG = VayuConfig()
VAYU_CONFIG = CONFIG


def get_config() -> VayuConfig:
    return CONFIG


def reset_config() -> VayuConfig:
    global CONFIG, VAYU_CONFIG
    CONFIG = VayuConfig()
    VAYU_CONFIG = CONFIG
    return CONFIG
