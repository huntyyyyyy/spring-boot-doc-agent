#!/usr/bin/env python3
"""

Run with: python -m doc_engine.tools.build_cross_group_edges

build_cross_group_edges.py — resolve cross-group file relationships once,
deterministically, instead of broadcasting the whole reference table to
every Stage-1 subagent and asking each to infer them.

Concept modules: ``cross_group_resolve``, ``cross_group_emit``, ``cross_group_cli``.
This façade keeps the stable ``-m`` entrypoint and ``parse_references`` /
``resolve_targets`` import surface used by query handlers.

Run with:
    python -m doc_engine.tools.build_cross_group_edges groups.json spring_signals.json \
        --out cross_group_edges.json
"""

from __future__ import annotations

import sys

from doc_engine.tools.cross_group_cli import main
from doc_engine.tools.cross_group_emit import (
    SCHEMA_VERSION,
    build_report,
)
from doc_engine.tools.cross_group_resolve import (
    IMPORT_RE,
    PACKAGE_RE,
    build_membership,
    is_cut,
    parse_references,
    resolve_targets,
)

__all__ = [
    "IMPORT_RE",
    "PACKAGE_RE",
    "SCHEMA_VERSION",
    "build_membership",
    "build_report",
    "is_cut",
    "main",
    "parse_references",
    "resolve_targets",
]

if __name__ == "__main__":
    sys.exit(main())
