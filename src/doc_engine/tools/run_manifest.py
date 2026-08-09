#!/usr/bin/env python3
"""Run-manifest façade — per-run telemetry for one document-spring-repo pipeline.

Run with: python -m doc_engine.tools.run_manifest

Concept modules: ``run_manifest_constants``, ``_io``, ``_stages``, ``_finalize``,
``_summary``, ``_cli``, ``_ports``. Historical rationale (ML Metadata vocabulary,
atomic write contract, concurrency) lives in those modules and steering prompt
04; this façade keeps the stable ``-m`` entrypoint and climb monkeypatch surface
(``os``, ``subprocess``, ``dfs_walk``, ``compute_file_signature``).

Usage:
    python -m doc_engine.tools.run_manifest init <repo_path> --out run_manifest.json
    python -m doc_engine.tools.run_manifest start-stage run_manifest.json signal_scan
    python -m doc_engine.tools.run_manifest end-stage run_manifest.json signal_scan --status complete
    python -m doc_engine.tools.run_manifest finalize run_manifest.json \\
        --signals-file spring_signals.json --docs-dir docs/ \\
        --interview-file interview_answers.json \\
        --preflight-file capacity_preflight_report.json
    python -m doc_engine.tools.run_manifest summary run_manifest.json
"""

from __future__ import annotations

import os
import subprocess

from doc_engine.core.jsonio import load_json as _read_json
from doc_engine.core.walk import compute_file_signature, dfs_walk
from doc_engine.tools.run_manifest_cli import (
    _COMMAND_HANDLERS,
    _build_arg_parser,
    _cmd_end_stage,
    _cmd_finalize,
    _cmd_init,
    _cmd_start_stage,
    _cmd_summary,
    _finalize_side_inputs,
    main,
)
from doc_engine.tools.run_manifest_constants import (
    _TAG_KEY_MAP,
    END_STAGE_STATUSES,
    PREFLIGHT_TO_MANIFEST_STAGE,
    STAGE_STATUSES,
)
from doc_engine.tools.run_manifest_finalize import (
    _apply_finalize_optional_fields,
    _cancel_running_stages,
    _infer_finalize_status,
    compute_capacity_preflight_tie_in,
    compute_evidence_tag_counts,
    finalize_manifest,
    load_file_signatures,
)
from doc_engine.tools.run_manifest_interview import (
    _empty_interview,
    _tally_interview_entry,
    parse_interview_file,
)
from doc_engine.tools.run_manifest_io import (
    _iso8601,
    _now_ms,
    _run_git,
    _write_json_atomic,
    git_commit_hash,
    git_is_dirty,
    make_run_id,
)
from doc_engine.tools.run_manifest_ports import (
    RunManifestLifecycle,
    RunManifestStore,
    default_manifest_store,
)
from doc_engine.tools.run_manifest_stages import (
    build_init_manifest,
    end_stage,
    start_stage,
)
from doc_engine.tools.run_manifest_summary import (
    _fanout_compare_line,
    _format_preflight_lines,
    _format_stage_line,
    _format_tag_totals,
    _summary_interview_line,
    _summary_optional_sections,
    _summary_timestamp_line,
    format_summary,
)

__all__ = [
    "END_STAGE_STATUSES",
    "PREFLIGHT_TO_MANIFEST_STAGE",
    "RunManifestLifecycle",
    "RunManifestStore",
    "STAGE_STATUSES",
    "_COMMAND_HANDLERS",
    "_TAG_KEY_MAP",
    "_apply_finalize_optional_fields",
    "_build_arg_parser",
    "_cancel_running_stages",
    "_cmd_end_stage",
    "_cmd_finalize",
    "_cmd_init",
    "_cmd_start_stage",
    "_cmd_summary",
    "_empty_interview",
    "_fanout_compare_line",
    "_finalize_side_inputs",
    "_format_preflight_lines",
    "_format_stage_line",
    "_format_tag_totals",
    "_infer_finalize_status",
    "_iso8601",
    "_now_ms",
    "_read_json",
    "_run_git",
    "_summary_interview_line",
    "_summary_optional_sections",
    "_summary_timestamp_line",
    "_tally_interview_entry",
    "_write_json_atomic",
    "build_init_manifest",
    "compute_capacity_preflight_tie_in",
    "compute_evidence_tag_counts",
    "compute_file_signature",
    "default_manifest_store",
    "dfs_walk",
    "end_stage",
    "finalize_manifest",
    "format_summary",
    "git_commit_hash",
    "git_is_dirty",
    "load_file_signatures",
    "main",
    "make_run_id",
    "os",
    "parse_interview_file",
    "start_stage",
    "subprocess",
]

if __name__ == "__main__":
    main()
