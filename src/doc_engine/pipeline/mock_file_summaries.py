"""Mock Stage 1 — file summaries from partition groups + citation pool."""

from __future__ import annotations

import json
import os

from doc_engine.pipeline.mock_stage_constants import SPRING_ROLE_BY_BUCKET
from doc_engine.pipeline.mock_stage_io import _write_json


def _index_pool_by_file(pool):
    """Invert citation pool into relpath -> [(bucket, line, match), ...]."""
    by_file = {}
    for bucket, rows in pool.items():
        for relpath, line, match in rows:
            by_file.setdefault(relpath, []).append((bucket, line, match))
    return by_file


def _arc_list(group_edges, key):
    """Return a list value for *key*, or an empty list when missing/wrong type."""
    if not isinstance(group_edges, dict):
        return []
    value = group_edges.get(key)
    return value if isinstance(value, list) else []


def _cross_group_arc_snippets(group_edges):
    """Serialize a few outbound / same-package arcs for mock summary entries."""
    snippets = []
    outbound = _arc_list(group_edges, "outbound")
    same = _arc_list(group_edges, "same_package_outside")
    for index in range(min(5, len(outbound))):
        snippets.append(json.dumps(outbound[index], sort_keys=True)[:200])
    for index in range(min(5, len(same))):
        snippets.append(json.dumps(same[index], sort_keys=True)[:200])
    return snippets


def _spring_role_for_signals(signals_for_file):
    """Map the first recognized signal bucket to a spring_role enum value."""
    for bucket, _line, _match in signals_for_file:
        if bucket in SPRING_ROLE_BY_BUCKET:
            return SPRING_ROLE_BY_BUCKET[bucket]
    return "other"


def _summary_entry(relpath, group_id, group_files, signals_for_file, cross):
    """Build one file-summarizer entry in the contract shape."""
    siblings = [path for path in group_files if path != relpath][:4]
    return {
        "file": relpath,
        "cluster": siblings,
        "summary": (
            f"MOCK SUMMARY (no model produced this): {relpath} was placed in "
            f"group {group_id} and carries {len(signals_for_file)} deterministic "
            f"signal-scan hit(s)."
        ),
        "relationships": siblings[:2],
        "cross_group_relationships": cross,
        "group_function": f"MOCK group function for group {group_id}",
        "spring_role": _spring_role_for_signals(signals_for_file),
        "evidence": [
            {"line": line, "what": f"signal-scan hit: {match}"}
            for _bucket, line, match in signals_for_file[:4]
        ],
    }


def _write_group_summaries(out_dir, groups, by_file, edges, log):
    """Write per-group summaries_group_<id>.json files; return their paths."""
    written = []
    for group in groups["groups"]:
        group_id = group["id"]
        group_edges = (edges.get("groups") or {}).get(str(group_id), {})
        cross = _cross_group_arc_snippets(group_edges)
        entries = [
            _summary_entry(
                relpath,
                group_id,
                group["files"],
                by_file.get(relpath, []),
                cross,
            )
            for relpath in group["files"]
        ]
        path = os.path.join(out_dir, f"summaries_group_{group_id}.json")
        _write_json(path, entries)
        written.append(path)
        log(
            f"  wrote {os.path.basename(path)} ({len(entries)} file entries, "
            f"{len(cross)} cross-group arc(s) attached)"
        )
    return written


def _combine_summary_files(out_dir, written, log):
    """Concatenate group summary files into summaries.json."""
    combined = []
    for path in written:
        with open(path, encoding="utf-8") as handle:
            combined.extend(json.load(handle))
    _write_json(os.path.join(out_dir, "summaries.json"), combined)
    log(
        f"  wrote summaries.json ({len(combined)} entries from "
        f"{len(written)} group file(s))"
    )
    return combined


def mock_file_summaries(out_dir, groups, pool, edges, log):
    """One summaries_group_<id>.json per group, in agents/file-summarizer.md's
    documented shape, then the concatenation into summaries.json that SKILL.md
    does with a one-liner.

    Shape is enforced by test_pipeline_stages.py's
    validate_file_summarizer_entries() — required keys, spring_role from the
    enumerated list, and the {"line": int, "what": str} evidence anchors. That
    suite runs against this output at the end of the run, so a drift between
    this mock and the real contract shows up as a test failure rather than
    quietly producing artifacts nothing would accept.
    """
    by_file = _index_pool_by_file(pool)
    written = _write_group_summaries(out_dir, groups, by_file, edges, log)
    combined = _combine_summary_files(out_dir, written, log)
    return f"{len(written)} group file(s), {len(combined)} file summaries"

