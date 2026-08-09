"""Strategy port for drift tier orchestration (OCP: add tiers via registry)."""

from __future__ import annotations

from typing import Any, Protocol


class DriftCheckStrategy(Protocol):
    """Port: compare prior signals (+ optional manifest) against a live repo."""

    def check_drift(self, *args: Any, **kwargs: Any) -> dict:
        ...
