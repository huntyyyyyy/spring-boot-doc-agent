"""Stalker sensors (E-STK1) — deterministic gap classes G1–G10.

Sensors only: emit findings; never rewrite fail_under / baselines.
"""

from __future__ import annotations

from typing import Any

__all__ = ["run_all_sensors"]


def __getattr__(name: str) -> Any:
    if name == "run_all_sensors":
        from doc_engine.ci.stalker_sensors.scan import run_all_sensors

        return run_all_sensors
    raise AttributeError(name)
