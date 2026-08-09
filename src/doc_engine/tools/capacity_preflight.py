#!/usr/bin/env python3
"""Capacity preflight façade — Stage-0 scale estimate before a full pipeline run.

Run with: python -m doc_engine.tools.capacity_preflight

Concept modules: ``capacity_preflight_constants``, ``_groups``, ``_stage4``,
``_compute``, ``_calibration``, ``_cli``, ``_ports``. Historical rationale for
thresholds and Stage-4 proxy honesty lives in those modules and CONSTRAINTS.md;
this façade keeps the stable ``-m`` entrypoint and test import surface.
"""

from __future__ import annotations

from doc_engine.paths import (
    PathValidationError,
    checked_output_path,
    checked_path,
)
from doc_engine.tools import (
    build_cross_group_edges,
    partition_repo,
    spring_signal_scan,
)
from doc_engine.tools.capacity_preflight_calibration import (
    _proxy_pool_from_stage0_report,
    _resolve_stage4_proxy,
    compute_stage4_calibration,
)
from doc_engine.tools.capacity_preflight_cli import (
    _build_arg_parser,
    _load_optional_json,
    _maybe_write_report,
    _print_l2b_summary,
    _print_stage0_summary,
    _print_warnings,
    _run_l2b_calibration,
    _run_stage0_preflight,
    main,
)
from doc_engine.tools.capacity_preflight_compute import (
    _preflight_threshold_warnings,
    _stage4_pool_fields,
    _stage4_shared_pool_warning,
    _stage_fanout_for_groups,
    compute_preflight,
)
from doc_engine.tools.capacity_preflight_constants import (
    CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION,
    STAGE3_ARCH_TEST_REVIEW_FANOUT,
    STAGE3_FIXED_FANOUT,
    STAGE4_FIXED_FANOUT,
    STAGE4_MEASURED_ALWAYS_OMITTED,
    STAGE4_PROXY_INCLUDED,
    STAGE4_PROXY_OMITTED,
)
from doc_engine.tools.capacity_preflight_groups import (
    _estimate_file_token_pairs,
    _groups_payload,
    _load_or_build_edges,
    _load_or_build_groups,
    estimate_stage1_slice_tokens,
)
from doc_engine.tools.capacity_preflight_ports import (
    CapacityEstimatePort,
    CapacityReportWriter,
    write_capacity_report,
)
from doc_engine.tools.capacity_preflight_stage4 import (
    _json_est_tokens,
    _measured_included_omitted,
    _measured_stage4_note,
    _optional_json_est,
    compare_stage4_proxy_to_measured,
    estimate_stage4_shared_pool_tokens,
    measure_stage4_shared_pool_tokens,
)
from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES

__all__ = [
    "CAPACITY_PREFLIGHT_REPORT_SCHEMA_VERSION",
    "CapacityEstimatePort",
    "CapacityReportWriter",
    "PathValidationError",
    "STAGE3_ARCH_TEST_REVIEW_FANOUT",
    "STAGE3_FIXED_FANOUT",
    "STAGE4_FIXED_FANOUT",
    "STAGE4_MEASURED_ALWAYS_OMITTED",
    "STAGE4_PROXY_INCLUDED",
    "STAGE4_PROXY_OMITTED",
    "VALID_DOC_FILES",
    "_build_arg_parser",
    "_estimate_file_token_pairs",
    "_groups_payload",
    "_json_est_tokens",
    "_load_optional_json",
    "_load_or_build_edges",
    "_load_or_build_groups",
    "_maybe_write_report",
    "_measured_included_omitted",
    "_measured_stage4_note",
    "_optional_json_est",
    "_preflight_threshold_warnings",
    "_print_l2b_summary",
    "_print_stage0_summary",
    "_print_warnings",
    "_proxy_pool_from_stage0_report",
    "_resolve_stage4_proxy",
    "_run_l2b_calibration",
    "_run_stage0_preflight",
    "_stage4_pool_fields",
    "_stage4_shared_pool_warning",
    "_stage_fanout_for_groups",
    "build_cross_group_edges",
    "checked_output_path",
    "checked_path",
    "compare_stage4_proxy_to_measured",
    "compute_preflight",
    "compute_stage4_calibration",
    "estimate_stage1_slice_tokens",
    "estimate_stage4_shared_pool_tokens",
    "main",
    "measure_stage4_shared_pool_tokens",
    "partition_repo",
    "spring_signal_scan",
    "write_capacity_report",
]

if __name__ == "__main__":
    raise SystemExit(main())
