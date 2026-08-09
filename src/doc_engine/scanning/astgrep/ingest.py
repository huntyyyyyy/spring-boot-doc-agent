"""Ingest ast-grep matches into evidence buckets and entity-map candidates."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Set

from doc_engine.scanning.astgrep.errors import AstGrepError
from doc_engine.scanning.java_extract import (
    extract_query_from_astgrep_args,
    extract_repository,
    first_line_match,
)

EVIDENCE_BUCKETS = {
    "api_surface", "outbound_clients", "messaging", "persistence",
    "raw_queries", "security", "configuration", "error_handling",
    "observability", "deployment", "testing", "references",
}


def enrich_query_entry(entry: Dict[str, Any], match: Dict[str, Any]) -> None:
    """Attach query_kind / query text extracted from ast-grep metaVariables."""
    multi_args = match.get("metaVariables", {}).get("multi", {}).get("ARGS", [])
    query_kind, query_text = extract_query_from_astgrep_args(multi_args)
    entry["query_kind"] = query_kind
    if query_text is not None:
        entry["query"] = query_text


def record_entity_match(
    *,
    repo_path: str,
    rel: str,
    line: int,
    text: str,
    match_str: str,
    rule_id: str,
    evidence: Dict[str, List[Dict[str, Any]]],
    entity_table_map_candidates: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Record one persistence__entity match into evidence + map candidates."""
    from doc_engine.scanning import _scanner_astgrep as facade

    header = facade.read_source_lines(repo_path, rel, 1, max_lines=40)
    extracted = facade.extract_entity(rel, text, package_source=header or None)
    if extracted is None:
        raise AstGrepError(
            f"persistence__entity match at {rel}:{line} failed extract_entity "
            "(annotation-induced extract failure — STRUCTURAL)"
        )
    class_name, map_entry = extracted
    map_entry["rule_id"] = rule_id
    map_entry["match"] = match_str
    entity_table_map_candidates.setdefault(class_name, []).append(map_entry)
    evidence.setdefault("persistence", []).append({
        "file": rel, "line": line, "match": match_str,
        "rule_id": rule_id, "class_name": class_name,
    })


def record_bucket_match(
    *,
    match: Dict[str, Any],
    rel: str,
    line: int,
    text: str,
    match_str: str,
    rule_id: str,
    evidence: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Record a non-entity rule hit into its evidence bucket."""
    bucket, _, _ = rule_id.partition("__")
    if bucket not in EVIDENCE_BUCKETS:
        raise AstGrepError(
            f"ast-grep rule id '{rule_id}' has no matching evidence bucket"
        )
    entry: Dict[str, Any] = {
        "file": rel, "line": line, "match": match_str, "rule_id": rule_id
    }
    if rule_id == "raw_queries__query":
        enrich_query_entry(entry, match)
    elif rule_id == "persistence__repository":
        entry.update(extract_repository(text))
    evidence.setdefault(bucket, []).append(entry)


def ingest_ast_grep_match(
    *,
    match: Dict[str, Any],
    repo_path: str,
    gitignore_spec: Any,
    evidence: Dict[str, List[Dict[str, Any]]],
    entity_table_map_candidates: Dict[str, List[Dict[str, Any]]],
    seen: Set,
) -> None:
    """Filter, dedupe, and record one ast-grep match into evidence maps."""
    file_path = match.get("file", "")
    rel = os.path.relpath(file_path, repo_path).replace(os.sep, "/")
    if gitignore_spec is not None and gitignore_spec.match_file(rel):
        return
    line = match.get("range", {}).get("start", {}).get("line", 0) + 1
    text = match.get("text", "")
    rule_id = match.get("ruleId", "")
    match_str = first_line_match(text)
    dedup_key = (rel, line, rule_id)
    if dedup_key in seen:
        return
    seen.add(dedup_key)
    if rule_id == "persistence__entity":
        record_entity_match(
            repo_path=repo_path,
            rel=rel,
            line=line,
            text=text,
            match_str=match_str,
            rule_id=rule_id,
            evidence=evidence,
            entity_table_map_candidates=entity_table_map_candidates,
        )
        return
    record_bucket_match(
        match=match,
        rel=rel,
        line=line,
        text=text,
        match_str=match_str,
        rule_id=rule_id,
        evidence=evidence,
    )
