#!/usr/bin/env python3
"""Deprecated shim — prefer ``doc-engine quality-gates``."""

from __future__ import annotations

import warnings

from doc_engine.ci.quality_gates import main

if __name__ == "__main__":
    warnings.warn(
        "scripts/ci/run_quality_gates.py is deprecated; use "
        "`doc-engine quality-gates` (same flags).",
        DeprecationWarning,
        stacklevel=1,
    )
    raise SystemExit(main())
