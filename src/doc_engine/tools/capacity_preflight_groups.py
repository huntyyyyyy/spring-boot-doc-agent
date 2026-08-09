"""Load or build partition groups / edges and Stage-1 slice estimates."""

from __future__ import annotations

import json
import os

from doc_engine.tools import partition_repo


def _estimate_file_token_pairs(repo_path):
    """Walk repo_path via partition_repo helpers; return [(rel, tokens), ...]."""
    all_files = partition_repo.dfs_file_list(
        repo_path,
        partition_repo.DEFAULT_EXCLUDED_DIRS,
        partition_repo.DEFAULT_EXCLUDED_EXTS,
        partition_repo.DEFAULT_EXCLUDED_FILES,
    )
    file_tokens = []
    for full in all_files:
        # Via partition_repo's shared helper, not an inline .replace(). This
        # was the third site of the same bug -- partition_repo.relpath_posix()
        # carries the full history -- and it became load-bearing when this
        # function started feeding its groups to build_report(), which joins
        # them by path against spring_signals.json's forward-slash paths. On
        # Windows that join matched nothing and the preflight silently
        # under-reported the fan-out it exists to estimate.
        rel = partition_repo.relpath_posix(full, repo_path)
        tokens, reason = partition_repo.estimate_tokens(full, 2_000_000)
        if reason:
            continue
        file_tokens.append((rel, tokens))
    return file_tokens


def _groups_payload(repo_path, max_tokens, overlap, file_tokens, groups_raw):
    """Shape the on-disk/groups.json-compatible partition payload."""
    return {
        "repo_path": os.path.abspath(repo_path),
        "max_tokens_per_group": max_tokens,
        "overlap": overlap,
        "total_files_considered": len(file_tokens),
        "num_groups": len(groups_raw),
        "groups": [
            {"id": idx, "files": [f for f, _ in g], "est_tokens": sum(t for _, t in g)}
            for idx, g in enumerate(groups_raw)
        ],
    }


def _load_or_build_groups(repo_path, max_tokens, overlap, groups_file):
    """Read an existing groups.json if given, otherwise run
    partition_repo.py's own dfs_file_list()/estimate_tokens()/build_groups()
    against repo_path — never a re-implementation of that arithmetic."""
    if groups_file:
        with open(groups_file, encoding="utf-8") as f:
            return json.load(f)

    file_tokens = _estimate_file_token_pairs(repo_path)
    groups_raw = partition_repo.build_groups(file_tokens, max_tokens, overlap)
    return _groups_payload(repo_path, max_tokens, overlap, file_tokens, groups_raw)


def _load_or_build_edges(repo_path, signals_file, groups_data, edges_file):
    """Read an existing cross_group_edges.json if given, otherwise build it
    via build_cross_group_edges.build_report() — never a re-implementation
    of that join.

    Unlike the groups/references pair this replaced, this one is *order
    dependent*: the join takes both the partition and the signals, so
    groups_data must already exist before this is called. SKILL.md's Stage 0
    writes this file, so --edges-file is the common path on a real run and
    the scan below is the fallback.

    scan()'s return shape (and spring_signal_scan.py main()'s on-disk JSON,
    which mirrors it exactly) nests every evidence bucket under a top-level
    `evidence` key rather than at the document root; build_report() knows
    that and reads it itself."""
    from doc_engine.tools import capacity_preflight as cap

    if edges_file:
        with open(edges_file, encoding="utf-8") as f:
            return json.load(f)

    if signals_file:
        with open(signals_file, encoding="utf-8") as f:
            signals_data = json.load(f)
    else:
        signals_data = cap.spring_signal_scan.scan(
            repo_path, scanners=["filesystem", "ast-grep"],
        )
    return cap.build_cross_group_edges.build_report(groups_data, signals_data)


def estimate_stage1_slice_tokens(edges):
    """Estimate the per-group Stage-1 edge slice, serialized the way it will
    actually be handed to the dispatch (as JSON text), with the same chars/N
    heuristic partition_repo.py uses for everything else — so the number is
    directly comparable to a group's own est_tokens.

    Returns a distribution rather than a scalar, because the broadcast model
    this replaced had only one meaningful number and the partitioned one has
    two. `total` is what the old references-times-groups product was trying
    to approximate: whole-run cost. `max` is the one that actually bounds
    risk — it is the largest single Stage-1 dispatch, and a context limit is
    breached by one dispatch, not by a sum."""
    per_group = {
        gid: max(1, len(json.dumps(slice_)) // partition_repo.CHARS_PER_TOKEN_DEFAULT)
        for gid, slice_ in edges.get("groups", {}).items()
    }
    values = list(per_group.values()) or [0]
    return {
        "per_group": per_group,
        "max": max(values),
        "mean": sum(values) // len(values),
        "total": sum(values),
    }

