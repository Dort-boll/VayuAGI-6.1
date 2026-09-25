"""Small logging facade shared by all subsystems."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"vayu_agi.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


class CognitiveLogger:
    def __init__(self, name: str = "engine") -> None:
        self.logger = get_logger(name)

    def log_thought(self, thought_id: str, content: str, state: str) -> None:
        self.logger.debug("thought=%s state=%s content=%s", thought_id, state, content[:100])

    def log_evolution(self, generation: int, improvement: str) -> None:
        self.logger.info("generation=%s improvement=%s", generation, improvement)