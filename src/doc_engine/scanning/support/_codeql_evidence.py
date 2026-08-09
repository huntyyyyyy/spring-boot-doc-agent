"""Project CodeQL query rows into Stage-0 evidence buckets.

SoR: normalized CodeQL rows from ``_codeql_queries`` / ``_codeql_runner``.
Derived: ``evidence`` map keyed by bucket (``api_surface``, ``persistence``,
``raw_queries``, …).

``entity_table_map`` candidacy is a separate derived view owned by
``_codeql_entity_map``; this module only walks rows and joins that view when
``rule_id`` is ``persistence__entity``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from doc_engine.core.context import ScanContext
from doc_engine.scanning.java_extract import (
    extract_repository,
    first_line_match,
    normalize_repo_path,
    read_source_lines,
)
from doc_engine.scanning.support._codeql_entity_map import record_entity_hit

_ENTITY_RULE = "persistence__entity"
_REPOSITORY_RULE = "persistence__repository"
_RAW_QUERY_RULE = "raw_queries__query"


def _apply_raw_query_fields(entry: Dict[str, Any], row: Dict[str, Any]) -> None:
    query_kind = row.get("query_kind", "jpql")
    query_text = row.get("query_text") or row.get("query")
    entry["query_kind"] = query_kind
    if query_text:
        entry["query"] = query_text


def _apply_repository_fields(
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
    """Build one non-entity evidence entry from a CodeQL result row."""
    entry: Dict[str, Any] = {
        "file": rel,
        "line": row.get("line"),
        "match": first_line_match(match_text),
        "rule_id": rule_id,
    }
    if rule_id == _RAW_QUERY_RULE:
        _apply_raw_query_fields(entry, row)
    elif rule_id == _REPOSITORY_RULE:
        _apply_repository_fields(entry, row, match_text)
    return entry


def project_codeql_row(
    *,
    repo_path: str,
    row: Dict[str, Any],
    java_rels: Optional[set],
    evidence: Dict[str, List[Dict[str, Any]]],
    entity_candidates: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Project one CodeQL row into evidence and/or entity_table_map candidates."""
    rel = normalize_repo_path(repo_path, row.get("file", ""))
    if java_rels is not None and rel not in java_rels:
        return
    row["file"] = rel
    rule_id = row.get("rule_id", "")
    line = row.get("line", 1)
    max_lines = 40 if rule_id in {_ENTITY_RULE, _REPOSITORY_RULE} else 10
    match_text = read_source_lines(repo_path, rel, line, max_lines=max_lines)
    bucket, _, _ = rule_id.partition("__")

    if rule_id == _ENTITY_RULE:
        record_entity_hit(
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


def project_codeql_rows(
    *,
    repo_path: str,
    rows: List[Dict[str, Any]],
    scan_context: Optional[ScanContext],
) -> tuple[Dict[str, List[Dict[str, Any]]], Dict[str, List[Dict[str, Any]]]]:
    """Project all CodeQL rows into evidence buckets + entity_table_map candidates."""
    java_rels: Optional[set] = None
    if scan_context is not None:
        java_rels = {entry.rel_path for entry in scan_context.java_files}

    evidence: Dict[str, List[Dict[str, Any]]] = {}
    entity_candidates: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        project_codeql_row(
            repo_path=repo_path,
            row=row,
            java_rels=java_rels,
            evidence=evidence,
            entity_candidates=entity_candidates,
        )
    for bucket_rows in evidence.values():
        bucket_rows.sort(key=lambda item: (item["file"], item.get("line", 0)))
    return evidence, entity_candidates
