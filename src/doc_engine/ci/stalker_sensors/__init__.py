"""Stalker sensors (E-STK1) — deterministic gap classes G1–G6.

Sensors only: emit findings; never rewrite fail_under / baselines.
"""
from __future__ import annotations

from doc_engine.ci.stalker_sensors.scan import run_all_sensors

__all__ = ["run_all_sensors"]
