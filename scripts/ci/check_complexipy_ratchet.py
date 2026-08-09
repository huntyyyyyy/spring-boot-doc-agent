#!/usr/bin/env python3
"""Deprecated shim — prefer ``doc-engine complexipy-ratchet``.

Run with:
    python3 scripts/ci/check_complexipy_ratchet.py
    # preferred:
    doc-engine complexipy-ratchet
"""

from __future__ import annotations

import warnings

from doc_engine.ci.complexipy_ratchet import main

if __name__ == "__main__":
    warnings.warn(
        "scripts/ci/check_complexipy_ratchet.py is deprecated; use "
        "`doc-engine complexipy-ratchet` (same flags).",
        DeprecationWarning,
        stacklevel=1,
    )
    raise SystemExit(main())
