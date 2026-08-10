"""Shared package roots for Python quality gates (scope, not thresholds).

Owns which trees complexity / duplication / related gates scan. Thresholds
live on concept ``*_policy`` modules — not here.
"""

from __future__ import annotations

PACKAGE_ROOTS = ("src/doc_engine", "src/stf")
