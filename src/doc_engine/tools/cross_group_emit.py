"""Emit cut import arcs and same-package adjacency for cross-group edges."""

from __future__ import annotations

import collections
from typing import Dict, List, Set, Tuple

from doc_engine.tools.cross_group_resolve import is_cut, resolve_targets

SCHEMA_VERSION = 1


def empty_per_group_buckets(group_ids: List[int]) -> Dict[int, dict]:
    return {
        group_id: {"outbound": [], "inbound": [], "same_package_outside": []}
        for group_id in group_ids
    }


def append_cut_edge(
    per_group: Dict[int, dict],
    memb: Dict[str, Set[int]],
    edge: dict,
) -> None:
    for group_id in memb.get(edge["from"], ()):
        per_group[group_id]["outbound"].append(edge)
    for group_id in memb.get(edge["to"], ()):
        per_group[group_id]["inbound"].append(edge)


def maybe_emit_cut_arc(
    source_path: str,
    destination_path: str,
    qualified: str,
    confidence: str,
    is_static: bool,
    memb: Dict[str, Set[int]],
    per_group: Dict[int, dict],
    seen: Set[Tuple[str, str, str]],
    counts: collections.Counter,
) -> None:
    if destination_path == source_path or not is_cut(memb, source_path, destination_path):
        return
    edge_key = (source_path, destination_path, qualified)
    if edge_key in seen:
        return
    seen.add(edge_key)
    counts["cut_arcs"] += 1
    counts[f"confidence_{confidence}"] += 1
    edge = {
        "from": source_path,
        "to": destination_path,
        "via": qualified,
        "confidence": confidence,
        "static_import": is_static,
    }
    append_cut_edge(per_group, memb, edge)


def emit_targets_for_import(
    source_path: str,
    qualified: str,
    is_static: bool,
    decl_files,
    stem_index,
    memb: Dict[str, Set[int]],
    per_group: Dict[int, dict],
    seen: Set[Tuple[str, str, str]],
    counts: collections.Counter,
) -> None:
    targets, confidence = resolve_targets(qualified, decl_files, stem_index)
    if confidence == "unresolved":
        counts["unresolved_imports"] += 1
        return
    for destination_path in targets:
        maybe_emit_cut_arc(
            source_path,
            destination_path,
            qualified,
            confidence,
            is_static,
            memb,
            per_group,
            seen,
            counts,
        )


def record_resolved_import_arcs(
    imports: Dict[str, List[Tuple[str, bool]]],
    decl_files,
    stem_index,
    memb: Dict[str, Set[int]],
    per_group: Dict[int, dict],
    counts: collections.Counter,
) -> None:
    """Emit cut import arcs into per-group outbound/inbound buckets."""
    seen: Set[Tuple[str, str, str]] = set()
    for source_path, entries in imports.items():
        for qualified, is_static in entries:
            emit_targets_for_import(
                source_path,
                qualified,
                is_static,
                decl_files,
                stem_index,
                memb,
                per_group,
                seen,
                counts,
            )


def adjacency_outside_group(
    members: Set[str],
    group_id: int,
    files_of: Dict[int, Set[str]],
    memb: Dict[str, Set[int]],
) -> Tuple[List[str], List[str]]:
    inside = sorted(members & files_of[group_id])
    outside = sorted(
        path for path in members if group_id not in memb.get(path, set())
    )
    return inside, outside


def record_package_group_adjacency(
    package_name: str,
    members: Set[str],
    group_id: int,
    files_of: Dict[int, Set[str]],
    memb: Dict[str, Set[int]],
    per_group: Dict[int, dict],
    counts: collections.Counter,
) -> None:
    inside, outside = adjacency_outside_group(members, group_id, files_of, memb)
    if not inside or not outside:
        return
    per_group[group_id]["same_package_outside"].append(
        {
            "package": package_name,
            "files_in_group": inside,
            "files_outside_group": outside,
        }
    )
    counts["same_package_adjacency_rows"] += len(outside)


def record_same_package_adjacency(
    decl_files: Dict[str, Set[str]],
    group_ids: List[int],
    files_of: Dict[int, Set[str]],
    memb: Dict[str, Set[int]],
    per_group: Dict[int, dict],
    counts: collections.Counter,
) -> None:
    """Same-package neighbours as adjacency, never a materialized clique."""
    for package_name, members in sorted(decl_files.items()):
        if len(members) < 2:
            continue
        for group_id in group_ids:
            record_package_group_adjacency(
                package_name, members, group_id, files_of, memb, per_group, counts
            )


def shipping_stats(
    references: List[dict],
    groups: List[dict],
    per_group: Dict[int, dict],
    counts: collections.Counter,
) -> dict:
    broadcast_rows = len(references) * len(groups)
    shipped_rows = (
        sum(
            len(bucket["outbound"]) + len(bucket["inbound"])
            for bucket in per_group.values()
        )
        + counts["same_package_adjacency_rows"]
    )
    reduction_factor = (
        round(broadcast_rows / shipped_rows, 1) if shipped_rows else None
    )
    return {
        "broadcast_rows_avoided": broadcast_rows,
        "rows_shipped": shipped_rows,
        "reduction_factor": reduction_factor,
        **dict(counts),
    }


def build_report(groups_data: dict, signals_data: dict) -> dict:
    from doc_engine.tools.cross_group_resolve import build_membership, parse_references

    groups = groups_data["groups"]
    references = signals_data.get("evidence", {}).get("references", [])
    decl_files, stem_index, imports = parse_references(references)
    memb = build_membership(groups)
    group_ids = [group["id"] for group in groups]
    files_of = {group["id"]: set(group["files"]) for group in groups}
    per_group = empty_per_group_buckets(group_ids)
    counts: collections.Counter = collections.Counter()

    record_resolved_import_arcs(
        imports, decl_files, stem_index, memb, per_group, counts
    )
    record_same_package_adjacency(
        decl_files, group_ids, files_of, memb, per_group, counts
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "repo_path": groups_data.get("repo_path"),
        "num_groups": len(groups),
        "references_rows": len(references),
        "stats": shipping_stats(references, groups, per_group, counts),
        "groups": {str(group_id): per_group[group_id] for group_id in group_ids},
    }
