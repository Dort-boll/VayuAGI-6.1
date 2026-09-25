"""Intuitive pattern scoring kept separate from synthesis."""

from __future__ import annotations

import re


class IntuitiveReasoner:
    def score(self, text: str) -> float:
        words = re.findall(r"[\w'-]+", text.lower())
        unique = len(set(words))
        return min(unique / max(len(words), 1), 1.0)