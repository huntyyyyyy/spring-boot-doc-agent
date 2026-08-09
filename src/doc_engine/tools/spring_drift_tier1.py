"""Tier-1 drift: content-hash classify + cheap whole-repo scan."""

from __future__ import annotations

import os
import sys

from doc_engine.tools import spring_signal_scan


def _classify_known_path(rel, old_sig, current_signatures, buckets):
    if rel not in current_signatures:
        buckets["deleted"].append(rel)
        return
    if current_signatures[rel] != old_sig:
        buckets["changed"].append(rel)
        return
    buckets["unchanged"].append(rel)


def classify_files(old_signatures, current_signatures):
    buckets = {"unchanged": [], "changed": [], "deleted": []}
    for rel, old_sig in old_signatures.items():
        _classify_known_path(rel, old_sig, current_signatures, buckets)
    added = sorted(set(current_signatures) - set(old_signatures))
    return {
        "unchanged": sorted(buckets["unchanged"]),
        "changed": sorted(buckets["changed"]),
        "deleted": sorted(buckets["deleted"]),
        "added": added,
    }


def tier1_scan(repo_path, scan_context=None):
    """Fresh sha256 per file currently in repo_path.

    When scan_context is provided, reuses its precomputed signatures (same walk
    as spring_signal_scan) instead of walking the repository again.
    """
    if scan_context is not None:
        return dict(scan_context.file_signatures)

    current = {}
    for full in spring_signal_scan.dfs_walk(repo_path):
        rel = os.path.relpath(full, repo_path).replace("\\", "/")
        try:
            current[rel] = spring_signal_scan.compute_file_signature(full)
        except OSError as exc:
            print(f"warning: could not read '{rel}': {exc}", file=sys.stderr)
    return current


def all_citations(signals):
    """Yield (source, citation) for every evidence-bearing entry in the
    signals JSON — every entry in every `evidence` bucket, plus every
    entity_table_map value, tagged with where it came from so the report
    can point back at it. entity_table_map is keyed by class name, which
    the persistence bucket's parallel entity entry can't see on its own
    (that's why spring_signal_scan.py puts `class_name` directly on the
    bucket entry too) — inject it into the citation dict here from the map
    key so both representations expose the same field uniformly."""
    for bucket_name, entries in signals.get("evidence", {}).items():
        for entry in entries:
            yield ("evidence." + bucket_name, entry)
    for class_name, entry in signals.get("entity_table_map", {}).items():
        citation = dict(entry)
        citation.setdefault("class_name", class_name)
        yield ("entity_table_map." + class_name, citation)

