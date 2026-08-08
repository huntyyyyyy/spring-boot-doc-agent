#!/usr/bin/env python3
"""Deprecated shim — prefer ``doc-engine coverage-gap-average``."""

from __future__ import annotations

import warnings

from doc_engine.ci.coverage_gap_average import main

if __name__ == "__main__":
    warnings.warn(
        "scripts/ci/coverage_gap_average.py is deprecated; use "
        "`doc-engine coverage-gap-average` (same flags).",
        DeprecationWarning,
        stacklevel=1,
    )
    raise SystemExit(main())
