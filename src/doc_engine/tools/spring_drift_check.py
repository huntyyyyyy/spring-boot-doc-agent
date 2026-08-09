#!/usr/bin/env python3
"""Two-tier drift detection façade for spring_signals.json.

Run with: python -m doc_engine.tools.spring_drift_check

Tier-1 hashes files; tier-2 rechecks citations when something moved. Concept
modules: ``spring_drift_load``, ``spring_drift_tier1``, ``spring_drift_orchestrate``,
``spring_drift_cli``, plus existing ``spring_drift_tier2`` / ``_jpql`` / ``_common``.
"""

from __future__ import annotations

from doc_engine.paths import (
    PathValidationError,
    checked_output_path,
    checked_path,
)
from doc_engine.tools import spring_signal_scan as spring_signal_scan
from doc_engine.tools.spring_drift_cli import (
    _print_drift_summary,
    _require_path,
    _validate_drift_cli_paths,
    main,
)
from doc_engine.tools.spring_drift_common import (
    DRIFT_REPORT_SCHEMA_VERSION,
    STATUS_CONFIG_STRUCTURE_CHANGED,
    STATUS_CONFIG_VALUES_ONLY_CHANGED,
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
    STATUS_FILE_DELETED,
    STATUS_NO_RULE_FALLBACK,
    STATUS_UNCHANGED,
    STATUS_UNKNOWN_NO_SIGNATURE,
    drift_result,
)
from doc_engine.tools.spring_drift_jpql import (
    _raw_query_entries_with_resolved_entity,
    _reverify_jpql_lineage_provenance,
)
from doc_engine.tools.spring_drift_load import (
    _empty_signatures_are_legitimate,
    _reject_manifest,
    _validate_manifest_baseline,
    load_manifest,
    load_signals,
)
from doc_engine.tools.spring_drift_orchestrate import (
    _assemble_drift_report,
    _baseline_signatures_and_provenance,
    check_drift,
)
from doc_engine.tools.spring_drift_ports import DriftCheckStrategy
from doc_engine.tools.spring_drift_process import (
    _append_uniform_status,
    _group_citations_by_file,
    _index_fresh_evidence_by_file,
    _process_changed_file_citations,
    _process_file_citations,
    _recheck_citations_without_rule,
    _unchanged_fast_path_results,
)
from doc_engine.tools.spring_drift_tier1 import (
    _classify_known_path,
    all_citations,
    classify_files,
    tier1_scan,
)
from doc_engine.tools.spring_drift_tier2 import tier2_recheck_file
from doc_engine.tools.spring_drift_tier2_rules import _recheck_config_keys

__all__ = [
    "DRIFT_REPORT_SCHEMA_VERSION",
    "DriftCheckStrategy",
    "PathValidationError",
    "STATUS_CONFIG_STRUCTURE_CHANGED",
    "STATUS_CONFIG_VALUES_ONLY_CHANGED",
    "STATUS_CONFIRMED",
    "STATUS_DRIFTED",
    "STATUS_FILE_DELETED",
    "STATUS_NO_RULE_FALLBACK",
    "STATUS_UNCHANGED",
    "STATUS_UNKNOWN_NO_SIGNATURE",
    "_append_uniform_status",
    "_assemble_drift_report",
    "_baseline_signatures_and_provenance",
    "_classify_known_path",
    "_empty_signatures_are_legitimate",
    "_group_citations_by_file",
    "_index_fresh_evidence_by_file",
    "_print_drift_summary",
    "_process_changed_file_citations",
    "_process_file_citations",
    "_raw_query_entries_with_resolved_entity",
    "_recheck_citations_without_rule",
    "_recheck_config_keys",
    "_reject_manifest",
    "_require_path",
    "_reverify_jpql_lineage_provenance",
    "_unchanged_fast_path_results",
    "_validate_drift_cli_paths",
    "_validate_manifest_baseline",
    "all_citations",
    "check_drift",
    "checked_output_path",
    "checked_path",
    "classify_files",
    "drift_result",
    "load_manifest",
    "load_signals",
    "main",
    "spring_signal_scan",
    "tier1_scan",
    "tier2_recheck_file",
]

if __name__ == "__main__":
    raise SystemExit(main())
