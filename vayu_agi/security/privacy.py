"""Local-first request validation and basic rate limiting."""

from __future__ import annotations

import time
from collections import deque


class RequestRejected(ValueError):
    """Raised when a request violates a configured safety boundary."""


class PrivacyGuard:
    def __init__(self, max_chars: int = 10_000, requests_per_minute: int = 60) -> None:
        self.max_chars = max_chars
        self.requests_per_minute = requests_per_minute
        self._requests: deque[float] = deque()

    def validate(self, text: str) -> str:
        if not isinstance(text, str):
            raise RequestRejected("request must be a string")
        normalized = " ".join(text.split())
        if not normalized:
            raise RequestRejected("request must not be empty")
        if len(normalized) > self.max_chars:
            raise RequestRejected("request exceeds the configured limit")
        now = time.monotonic()
        while self._requests and now - self._requests[0] >= 60:
            self._requests.popleft()
        if len(self._requests) >= self.requests_per_minute:
            raise RequestRejected("request rate limit exceeded")
        self._requests.append(now)
        return normalized