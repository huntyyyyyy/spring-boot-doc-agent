"""Duplication policy setpoints — single owner for jscpd thresholds.

Gate command construction stays in ``quality_gate_checks``; this module owns
the tunable numbers only.
"""

from __future__ import annotations

DUPLICATION_MAX_PERCENT = 3
DUPLICATION_MIN_LINES = 5
