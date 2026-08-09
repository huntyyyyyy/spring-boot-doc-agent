#!/usr/bin/env python3
"""Shim: domain marker ratchet — prefer module entry below.

    python -m doc_engine.ci.test_domain_markers_check
"""

from __future__ import annotations

from doc_engine.ci.test_domain_markers_check import main

if __name__ == "__main__":
    raise SystemExit(main())
