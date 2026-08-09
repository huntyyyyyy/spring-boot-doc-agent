"""Load prior signals / optional run_manifest baselines for drift check."""

from __future__ import annotations

import json
import os
import sys

from doc_engine.paths import checked_path
from doc_engine.tools import spring_signal_scan


def load_signals(path):
    with open(path) as f:
        data = json.load(f)
    version = data.get("schema_version", 1)
    if version < 2:
        print(
            f"error: '{path}' was produced by an older spring_signal_scan.py "
            f"(schema_version={version}) that doesn't record file_signatures "
            f"or rule_id on evidence entries — both required for drift "
            f"detection. Re-run spring_signal_scan.py against the repo to "
            f"regenerate it, then re-run this tool against the new file.",
            file=sys.stderr,
        )
        sys.exit(1)
    return data


def _reject_manifest(path: str, message: str) -> None:
    print(f"error: '{path}' {message}", file=sys.stderr)
    sys.exit(1)


def _empty_signatures_are_legitimate(data) -> bool:
    target_path = data.get("target_repo", {}).get("path")
    if not target_path or not os.path.isdir(target_path):
        return False
    return not any(spring_signal_scan.dfs_walk(target_path))


def _validate_manifest_baseline(path: str, data) -> None:
    if "file_signatures" not in data:
        _reject_manifest(
            path,
            "has no 'file_signatures' field — is this a real "
            "run_manifest.json (from doc_engine.tools.run_manifest)? Not usable as a "
            "tier-1 baseline.",
        )
    if data.get("status") == "running":
        _reject_manifest(
            path,
            "has status 'running' — its pipeline run was never "
            "finalized (doc_engine.tools.run_manifest finalize was never called), so "
            "its file_signatures is likely still the empty placeholder from "
            "init and would misreport every file in the repo as newly added. "
            "Point --manifest at a manifest from after finalize, or omit "
            "--manifest to use spring_signals.json's own baseline instead.",
        )
    if data["file_signatures"]:
        return
    if _empty_signatures_are_legitimate(data):
        target_path = data.get("target_repo", {}).get("path")
        print(
            f"note: '{path}' has an empty 'file_signatures' map, but its recorded "
            f"target_repo.path ('{target_path}') genuinely has zero trackable files right "
            f"now too — treating this as a real empty-repo baseline, not a broken finalize.",
            file=sys.stderr,
        )
        return
    _reject_manifest(
        path,
        "has an empty 'file_signatures' map — finalize was "
        "called without ever recording any (e.g. no --signals-file and no "
        "repo to re-hash), so there's no real baseline to compare against. "
        "Point --manifest at a manifest with a populated file_signatures, "
        "or omit --manifest to use spring_signals.json's own baseline "
        "instead.",
    )


def load_manifest(path):
    """Load an optional run_manifest.json to use as the tier-1 file_signatures
    baseline instead of spring_signals.json's own — see the module docstring's
    "OPTIONAL --manifest" section for why this is a provenance choice, not a
    recency heuristic. Only file_signatures (plus target_repo, for the report's
    own provenance metadata) is used from it; run_manifest.json's other fields
    (stages, evidence_tag_counts, interview, ...) are irrelevant here.

    run_manifest.py's build_init_manifest() sets file_signatures to {} and
    status to "running", and only finalize_manifest() ever changes either
    (status becomes one of "complete"/"failed"/"partial"; file_signatures is
    only overwritten if finalize was actually given some). So status=="running"
    reliably means finalize never ran on this manifest at all, and an empty
    file_signatures map is *usually* a sign it was never given any (e.g.
    finalize was called without --signals-file) — treating that as a real
    baseline would silently classify every file in the repo as "added" instead
    of comparing against a real prior state (see classify_files()). This
    mirrors OpenLineage's run-lifecycle model
    (https://openlineage.io/docs/spec/run-cycle/): RUNNING is a non-terminal
    state a consumer shouldn't treat as a finished fact; only a terminal state
    (COMPLETE/FAIL/ABORT there, complete/failed/partial here) is trustworthy
    to act on.

    One legitimate exception: a repo that genuinely had zero trackable files
    at scan time also finalizes with an empty file_signatures map, and an
    "everything is newly added" report is the *correct* answer for that case,
    not a misreport. Since target_repo.path is recorded on every manifest,
    that's checked directly — if the path still exists and a fresh dfs_walk
    of it also finds zero files, the empty map is accepted as a real
    (if unusual) empty-repo baseline rather than rejected."""
    path = str(checked_path(path, want="file"))
    with open(path) as handle:
        data = json.load(handle)
    _validate_manifest_baseline(path, data)
    return data

