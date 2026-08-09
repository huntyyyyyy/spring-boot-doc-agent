"""Entity-table map candidates derived from CodeQL persistence__entity rows."""

from __future__ import annotations

from typing import Any, Dict, Optional

from doc_engine.scanning.java_extract import first_line_match, to_snake_case


def inferred_entity_map_entry(rel: str, class_name: str) -> Dict[str, Any]:
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
        return class_name, inferred_entity_map_entry(rel, class_name)
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
    """Build (class_name, map_entry) for a persistence__entity CodeQL row."""
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
    elif extracted is None:
        map_entry = inferred_entity_map_entry(rel, class_name)
    map_entry["rule_id"] = rule_id
    map_entry["match"] = first_line_match(match_text)
    return class_name, map_entry
