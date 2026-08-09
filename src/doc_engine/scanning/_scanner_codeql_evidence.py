"""CodeQL row → evidence buckets / entity_table_map candidates.

SoR: CodeQL result rows. Derived: evidence map entries + entity map candidates.
Entity-map builders live in ``_scanner_codeql_entity_map`` (LOC split).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from doc_engine.core.context import ScanContext
from doc_engine.scanning._scanner_codeql_entity_map import entity_map_entry
from doc_engine.scanning.java_extract import (
    extract_entity,
    extract_repository,
    first_line_match,
    normalize_repo_path,
    read_source_lines,
)


def acked_java_paths(
    scan_context: Optional[ScanContext],
    expected_paths: List[str],
) -> List[str]:
    if scan_context is None:
        return expected_paths
    return sorted({entry.rel_path for entry in scan_context.java_files})


def apply_raw_query_fields(entry: Dict[str, Any], row: Dict[str, Any]) -> None:
    query_kind = row.get("query_kind", "jpql")
    query_text = row.get("query_text") or row.get("query")
    entry["query_kind"] = query_kind
    if query_text:
        entry["query"] = query_text


def apply_repository_fields(
    entry: Dict[str, Any],
    row: Dict[str, Any],
    match_text: str,
) -> None:
    entry.update(extract_repository(match_text))
    if not entry.get("entity") and row.get("entity_name"):
        entry["entity"] = row.get("entity_name")


def evidence_entry_from_codeql_row(
    *,
    rel: str,
    row: Dict[str, Any],
    match_text: str,
    rule_id: str,
) -> Dict[str, Any]:
    """Build a non-entity evidence entry from one CodeQL result row."""
    entry: Dict[str, Any] = {
        "file": rel,
        "line": row.get("line"),
        "match": first_line_match(match_text),
        "rule_id": rule_id,
    }
    if rule_id == "raw_queries__query":
        apply_raw_query_fields(entry, row)
    elif rule_id == "persistence__repository":
        apply_repository_fields(entry, row, match_text)
    return entry


def ingest_entity_row(
    *,
    repo_path: str,
    rel: str,
    row: Dict[str, Any],
    match_text: str,
    rule_id: str,
    entity_candidates: Dict[str, List[Dict[str, Any]]],
    evidence: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Record entity_table_map candidate + persistence evidence for one entity hit."""
    header = read_source_lines(repo_path, rel, 1, max_lines=40)
    extracted = extract_entity(rel, match_text, package_source=header or None)
    class_name = row.get("class_name") if extracted is None else None
    built = entity_map_entry(
        rel=rel,
        class_name=class_name or "",
        match_text=match_text,
        rule_id=rule_id,
        extracted=extracted,
        codeql_table=row.get("table_name"),
    )
    if built is None:
        return
    class_name, map_entry = built
    entity_candidates.setdefault(class_name, []).append(map_entry)
    evidence.setdefault("persistence", []).append(
        {
            "file": rel,
            "line": row.get("line"),
            "match": first_line_match(match_text),
            "rule_id": rule_id,
            "class_name": class_name,
        }
    )


def ingest_codeql_row(
    *,
    repo_path: str,
    row: Dict[str, Any],
    java_rels: Optional[set],
    evidence: Dict[str, List[Dict[str, Any]]],
    entity_candidates: Dict[str, List[Dict[str, Any]]],
) -> None:
    rel = normalize_repo_path(repo_path, row.get("file", ""))
    if java_rels is not None and rel not in java_rels:
        return
    row["file"] = rel
    rule_id = row.get("rule_id", "")
    line = row.get("line", 1)
    max_lines = 40 if rule_id in {"persistence__entity", "persistence__repository"} else 10
    match_text = read_source_lines(repo_path, rel, line, max_lines=max_lines)
    bucket, _, _ = rule_id.partition("__")

    if rule_id == "persistence__entity":
        ingest_entity_row(
            repo_path=repo_path,
            rel=rel,
            row=row,
            match_text=match_text,
            rule_id=rule_id,
            entity_candidates=entity_candidates,
            evidence=evidence,
        )
        return

    entry = evidence_entry_from_codeql_row(
        rel=rel,
        row=row,
        match_text=match_text,
        rule_id=rule_id,
    )
    evidence.setdefault(bucket, []).append(entry)


def bucket_codeql_rows(
    *,
    repo_path: str,
    rows: List[Dict[str, Any]],
    scan_context: Optional[ScanContext],
) -> tuple[Dict[str, List[Dict[str, Any]]], Dict[str, List[Dict[str, Any]]]]:
    java_rels: Optional[set] = None
    if scan_context is not None:
        java_rels = {entry.rel_path for entry in scan_context.java_files}

    evidence: Dict[str, List[Dict[str, Any]]] = {}
    entity_candidates: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        ingest_codeql_row(
            repo_path=repo_path,
            row=row,
            java_rels=java_rels,
            evidence=evidence,
            entity_candidates=entity_candidates,
        )
    for bucket_rows in evidence.values():
        bucket_rows.sort(key=lambda item: (item["file"], item.get("line", 0)))
    return evidence, entity_candidates
