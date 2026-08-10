#!/usr/bin/env python3
"""Hard vacuity gate — ast-grep + vacuous(crate) + empty telemetry (E-AST0-E).

Usage:
    python3 scripts/ci/vacuous_test_gate.py
    python3 -m doc_engine.ci.vacuity
    python3 scripts/ci/vacuous_test_gate.py --no-ledger
"""

from __future__ import annotations

from doc_engine.ci.vacuity.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
