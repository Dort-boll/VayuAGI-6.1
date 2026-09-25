"""Persistent, JSON-backed records of completed interactions."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Episode:
    episode_id: str
    context: str
    action: str
    outcome: str
    success: bool
    timestamp: float


class EpisodicMemory:
    def __init__(self, directory: Path, ttl_seconds: int = 604800) -> None:
        self.path = directory / "episodes.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self.episodes = self._load()

    def store(self, context: str, action: str, outcome: str, success: bool) -> Episode:
        episode = Episode(f"ep_{time.time_ns()}", context, action, outcome, success, time.time())
        self.episodes.append(episode)
        self._save()
        return episode

    def retrieve(self, query: str, limit: int = 5) -> list[Episode]:
        words = set(query.lower().split())
        ranked = sorted(self.episodes, key=lambda episode: len(words & set(episode.context.lower().split())), reverse=True)
        return [episode for episode in ranked if words & set(episode.context.lower().split())][:limit]

    def _load(self) -> list[Episode]:
        if not self.path.exists():
            return []
        episodes = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                item = Episode(**json.loads(line))
                if time.time() - item.timestamp <= self.ttl_seconds:
                    episodes.append(item)
            except (TypeError, ValueError, json.JSONDecodeError):
                continue
        return episodes

    def _save(self) -> None:
        self.path.write_text("\n".join(json.dumps(asdict(item)) for item in self.episodes) + "\n", encoding="utf-8")