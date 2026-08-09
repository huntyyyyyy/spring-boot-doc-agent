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
    append_cut_edge as _append_cut_edge,
    build_report,
    empty_per_group_buckets as _empty_per_group_buckets,
    emit_targets_for_import as _emit_targets_for_import,
    maybe_emit_cut_arc as _maybe_emit_cut_arc,
    record_resolved_import_arcs as _record_resolved_import_arcs,
    record_same_package_adjacency as _record_same_package_adjacency,
    shipping_stats as _shipping_stats,
)
from doc_engine.tools.cross_group_resolve import (
    IMPORT_RE,
    PACKAGE_RE,
    build_membership,
    ingest_reference_row as _ingest_reference_row,
    is_cut,
    parse_references,
    resolve_targets,
    resolve_type_import as _resolve_type_import,
    resolve_wildcard_import as _resolve_wildcard_import,
    type_stem_from_path as _type_stem_from_path,
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
