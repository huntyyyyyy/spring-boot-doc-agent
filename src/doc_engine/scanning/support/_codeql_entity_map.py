"""Derived ``entity_table_map`` candidates from CodeQL persistence__entity hits.

SoR: one CodeQL row with ``rule_id=persistence__entity`` plus local Java source.
Derived: ``(class_name, map_entry)`` candidates (inferred vs explicit ``@Table``).
Persistence *evidence* rows for the same hit are appended here because the
entity finding is the shared SoR for both derived views.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from doc_engine.scanning.java_extract import (
    extract_entity,
    first_line_match,
    read_source_lines,
    to_snake_case,
)


def inferred_map_entry(rel: str, class_name: str) -> Dict[str, Any]:
    return {
        "file": rel,
        "table": to_snake_case(class_name),
        "table_name_source": "inferred-default-naming",
        "fqcn": class_name,
    }


def explicit_table_map_entry(
    *,
    rel: str,
    class_name: str,
    codeql_table: str,
    map_entry: Dict[str, Any],
) -> Dict[str, Any]:
    preserved_package = map_entry.get("package")
    preserved_fqcn = map_entry.get("fqcn")
    out = {
        "file": rel,
        "table": codeql_table,
        "table_name_source": "explicit",
        "fqcn": preserved_fqcn or class_name,
    }
    if preserved_package is not None:
        out["package"] = preserved_package
    return out


def base_entity_map_entry(
    *,
    rel: str,
    class_name: str,
    extracted: Optional[tuple],
) -> Optional[tuple[str, Dict[str, Any]]]:
    if extracted is None:
        if not class_name:
            return None
        return class_name, inferred_map_entry(rel, class_name)
    return extracted


def entity_map_entry(
    *,
    rel: str,
    class_name: str,
    match_text: str,
    rule_id: str,
    extracted: Optional[tuple],
    codeql_table: Optional[str],
) -> Optional[tuple[str, Dict[str, Any]]]:
    """Build ``(class_name, map_entry)`` for a persistence__entity CodeQL row."""
    built = base_entity_map_entry(
        rel=rel, class_name=class_name, extracted=extracted
    )
    if built is None:
        return None
    class_name, map_entry = built
    if codeql_table:
        map_entry = explicit_table_map_entry(
            rel=rel,
            class_name=class_name,
            codeql_table=codeql_table,
            map_entry=map_entry,
        )
    map_entry["rule_id"] = rule_id
    map_entry["match"] = first_line_match(match_text)
    return class_name, map_entry


def record_entity_hit(
    *,
    repo_path: str,
    rel: str,
    row: Dict[str, Any],
    match_text: str,
    rule_id: str,
    entity_candidates: Dict[str, List[Dict[str, Any]]],
    evidence: Dict[str, List[Dict[str, Any]]],
) -> None:
    """Append entity_table_map candidate + persistence evidence for one hit."""
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
