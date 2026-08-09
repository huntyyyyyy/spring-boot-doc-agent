"""Init / start-stage / end-stage mutations for run_manifest."""

from __future__ import annotations

from doc_engine.tools.run_manifest_constants import END_STAGE_STATUSES


def build_init_manifest(repo_path, now_ms=None):
    from doc_engine.tools import run_manifest as rm

    now_ms = rm._now_ms(now_ms)
    abspath = rm.os.path.abspath(repo_path)
    return {
        "schema_version": 1,
        "run_id": rm.make_run_id(now_ms),
        "target_repo": {
            "path": abspath,
            "commit_hash": rm.git_commit_hash(abspath),
            "dirty": rm.git_is_dirty(abspath),
        },
        "timestamp_start": rm._iso8601(now_ms),
        "timestamp_end": None,
        "status": "running",
        "stages": [],
        "file_signatures": {},
        "evidence_tag_counts": {},
        "interview": None,
        "capacity_preflight": None,
    }


def start_stage(manifest, name, fanout=None, now_ms=None):
    from doc_engine.tools import run_manifest as rm

    now_ms = rm._now_ms(now_ms)
    manifest.setdefault("stages", []).append(
        {
            "name": name,
            "status": "running",
            "start_time_ms": now_ms,
            "end_time_ms": None,
            "duration_ms": None,
            "error": None,
            "actual_fanout": fanout,
        }
    )
    return manifest


def end_stage(manifest, name, status, error=None, now_ms=None):
    from doc_engine.tools import run_manifest as rm

    if status not in END_STAGE_STATUSES:
        raise ValueError(
            f"unknown end-stage status {status!r}, must be one of {END_STAGE_STATUSES}"
        )
    now_ms = rm._now_ms(now_ms)
    # Search from the end: retry case (failed then retried — two start/end
    # pairs, same name) resolves to the immediately-preceding still-running
    # start-stage entry, not an earlier already-ended one.
    for stage in reversed(manifest.get("stages", [])):
        if stage["name"] == name and stage["status"] == "running":
            stage["end_time_ms"] = now_ms
            stage["duration_ms"] = now_ms - stage["start_time_ms"]
            stage["status"] = status
            stage["error"] = error
            return manifest
    raise ValueError(
        f"no running stage named {name!r} to end — start-stage was never called "
        f"for it, or it was already ended"
    )
