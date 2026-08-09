"""Finalize payloads: signatures, evidence tags, preflight tie-in, finalize.

``dfs_walk`` / ``compute_file_signature`` resolve via the ``run_manifest``
façade so climb tests can monkeypatch the public module surface.
"""

from __future__ import annotations

import json
import sys

from doc_engine.core.jsonio import load_json as _read_json
from doc_engine.tools import doc_tag_utils
from doc_engine.tools.run_manifest_constants import (
    PREFLIGHT_TO_MANIFEST_STAGE,
    _TAG_KEY_MAP,
)


def load_file_signatures(signals_file=None, repo_path=None):
    """Reuse spring_signals.json file_signatures if given; else re-walk/hash."""
    from doc_engine.tools import run_manifest as rm

    if signals_file:
        return _read_json(signals_file).get("file_signatures", {})
    if not repo_path:
        return {}
    sigs = {}
    for full in rm.dfs_walk(repo_path):
        rel = rm.os.path.relpath(full, repo_path).replace("\\", "/")
        try:
            sigs[rel] = rm.compute_file_signature(full)
        except OSError as e:
            print(
                f"warning: could not read '{rel}' to compute its content signature: {e}",
                file=sys.stderr,
            )
    return sigs


def compute_evidence_tag_counts(docs_dir):
    """Count tags per doc-writer output file via doc_tag_utils."""
    from doc_engine.tools import run_manifest as rm

    result = {}
    for stem in sorted(doc_tag_utils.VALID_DOC_FILES):
        path = rm.os.path.join(docs_dir, f"{stem}.md")
        if not rm.os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        counts = doc_tag_utils.count_tags_by_kind(text)
        result[f"{stem}.md"] = {_TAG_KEY_MAP[k]: v for k, v in counts.items()}
    return result


def compute_capacity_preflight_tie_in(preflight_path):
    """Map capacity_preflight stage_fanout keys through PREFLIGHT_TO_MANIFEST_STAGE."""
    try:
        data = _read_json(preflight_path)
    except (OSError, json.JSONDecodeError) as e:
        print(
            f"warning: could not read/parse capacity preflight file "
            f"'{preflight_path}': {e}",
            file=sys.stderr,
        )
        return None

    stage_fanout = data.get("stage_fanout", {})
    predicted_by_manifest_stage = {}
    unmapped = []
    for key, value in stage_fanout.items():
        manifest_stage = PREFLIGHT_TO_MANIFEST_STAGE.get(key)
        if manifest_stage is None:
            unmapped.append(key)
            print(
                f"warning: capacity_preflight stage key '{key}' has no known "
                f"mapping to a run_manifest stage name, skipping",
                file=sys.stderr,
            )
            continue
        predicted_by_manifest_stage[manifest_stage] = (
            predicted_by_manifest_stage.get(manifest_stage, 0) + value
        )

    return {
        "source_file": preflight_path,
        "total_predicted_fanout": data.get(
            "total_fanout", sum(stage_fanout.values())
        ),
        "predicted_fanout_by_manifest_stage": predicted_by_manifest_stage,
        "unmapped_preflight_keys": unmapped,
    }


def _cancel_running_stages(manifest, now_ms):
    """Mark still-running stages canceled; return human-readable warnings."""
    warnings = []
    for stage in manifest.get("stages", []):
        if stage["status"] != "running":
            continue
        stage["end_time_ms"] = now_ms
        stage["duration_ms"] = now_ms - stage["start_time_ms"]
        stage["status"] = "canceled"
        stage["error"] = (
            "stage never ended before finalize — orchestrating session may have "
            "crashed or skipped end-stage"
        )
        warnings.append(
            f"stage '{stage['name']}' was still running at finalize; marked canceled"
        )
    return warnings


def _infer_finalize_status(manifest):
    statuses = {s["status"] for s in manifest.get("stages", [])}
    if "failed" in statuses:
        return "failed"
    if "canceled" in statuses:
        return "partial"
    return "complete"


def _apply_finalize_optional_fields(
    manifest,
    file_signatures,
    evidence_tag_counts,
    interview,
    capacity_preflight,
):
    """Copy optional finalize payloads into the manifest when supplied."""
    if file_signatures is not None:
        manifest["file_signatures"] = file_signatures
    if evidence_tag_counts is not None:
        manifest["evidence_tag_counts"] = evidence_tag_counts
    if interview is not None:
        manifest["interview"] = interview
    if capacity_preflight is not None:
        manifest["capacity_preflight"] = capacity_preflight


def finalize_manifest(
    manifest,
    status=None,
    file_signatures=None,
    evidence_tag_counts=None,
    interview=None,
    capacity_preflight=None,
    now_ms=None,
):
    from doc_engine.tools import run_manifest as rm

    now_ms = rm._now_ms(now_ms)
    warnings = _cancel_running_stages(manifest, now_ms)

    if status is None:
        status = _infer_finalize_status(manifest)

    manifest["timestamp_end"] = rm._iso8601(now_ms)
    manifest["status"] = status
    _apply_finalize_optional_fields(
        manifest,
        file_signatures,
        evidence_tag_counts,
        interview,
        capacity_preflight,
    )
    return manifest, warnings
