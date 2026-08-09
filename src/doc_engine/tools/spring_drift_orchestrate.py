"""Orchestrate tier-1 + tier-2 drift check into a drift_report payload."""

from __future__ import annotations

import os
from collections import Counter

from doc_engine.core.context import ScanContext
from doc_engine.tools import spring_signal_scan
from doc_engine.tools.spring_drift_common import DRIFT_REPORT_SCHEMA_VERSION
from doc_engine.tools.spring_drift_jpql import _reverify_jpql_lineage_provenance
from doc_engine.tools.spring_drift_process import (
    _group_citations_by_file,
    _index_fresh_evidence_by_file,
    _process_file_citations,
    _unchanged_fast_path_results,
)
from doc_engine.tools.spring_drift_tier1 import classify_files, tier1_scan


def _baseline_signatures_and_provenance(signals, manifest):
    """Pick tier-1 signatures + provenance from manifest or signals."""
    if manifest is not None:
        return manifest.get("file_signatures", {}), {
            "source": "run_manifest.json",
            "run_id": manifest.get("run_id"),
            "repo_path": manifest.get("target_repo", {}).get("path"),
            "commit_hash": manifest.get("target_repo", {}).get("commit_hash"),
            "dirty": manifest.get("target_repo", {}).get("dirty"),
        }
    return signals.get("file_signatures", {}), {"source": "spring_signals.json"}


def _assemble_drift_report(repo_path, signals, baseline_provenance, classification, results):
    results.sort(key=lambda row: (row["file"] or "", row["line"] or 0, row["source"]))
    status_counts = Counter(row["status"] for row in results)
    return {
        "schema_version": DRIFT_REPORT_SCHEMA_VERSION,
        "repo_path": os.path.abspath(repo_path),
        "prior_scan_repo_path": signals.get("repo_path"),
        "file_signatures_baseline": baseline_provenance,
        "file_summary": classification,
        "citations_checked": len(results),
        "status_counts": dict(status_counts),
        "results": results,
    }


def check_drift(repo_path, signals, manifest=None):
    """manifest: optional run_manifest.json dict (see load_manifest()). When
    given, its file_signatures is the tier-1 baseline instead of signals' own
    — signals is still required regardless, for tier-2 evidence/entity_table_map
    that run_manifest.json never carries."""
    old_signatures, baseline_provenance = _baseline_signatures_and_provenance(
        signals, manifest
    )

    scan_context = ScanContext.build(repo_path)
    current_signatures = tier1_scan(repo_path, scan_context=scan_context)
    classification = classify_files(old_signatures, current_signatures)
    changed_set = set(classification["changed"])
    deleted_set = set(classification["deleted"])
    unchanged_set = set(classification["unchanged"])

    # Fast path: nothing moved — skip the expensive full Stage-0 rescan.
    if not changed_set and not deleted_set and not classification["added"]:
        return _assemble_drift_report(
            repo_path,
            signals,
            baseline_provenance,
            classification,
            _unchanged_fast_path_results(signals),
        )

    # Fresh Stage 0 scan of the current repo (same scanners as the prior
    # signals). Tier 2 compares citations against this bag filtered by file.
    scanners = signals.get("scanners") or ["filesystem", "ast-grep"]
    fresh_signals = spring_signal_scan.scan(
        repo_path,
        scanners=scanners,
        scan_context=scan_context,
    )
    fresh_evidence_by_file = _index_fresh_evidence_by_file(fresh_signals)
    fresh_entity_map = fresh_signals.get("entity_table_map", {})
    citations_by_file = _group_citations_by_file(signals)

    results = []
    fresh_entity_tables = {}

    for file_rel in sorted(citations_by_file):
        _process_file_citations(
            repo_path,
            file_rel,
            citations_by_file[file_rel],
            deleted_set=deleted_set,
            unchanged_set=unchanged_set,
            changed_set=changed_set,
            signals=signals,
            fresh_evidence_by_file=fresh_evidence_by_file,
            fresh_entity_map=fresh_entity_map,
            results=results,
            fresh_entity_tables=fresh_entity_tables,
        )

    # JPQL-lineage re-verify needs fresh_entity_tables fully populated.
    _reverify_jpql_lineage_provenance(
        results, signals, fresh_entity_tables, changed_set, deleted_set
    )
    return _assemble_drift_report(
        repo_path, signals, baseline_provenance, classification, results
    )

