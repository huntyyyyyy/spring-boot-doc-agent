"""MAPS_TO fact projection from entity_table_map (settled + contested)."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from doc_engine.scanning.facts_core import fact, type_symbol_quals


def maps_to_fact_from_source(
    class_name: str,
    source: Mapping[str, Any],
    *,
    base_quals: Dict[str, Any],
    default_scanner: Optional[str],
    fallback_rule_id: Optional[Any] = None,
) -> Dict[str, Any]:
    """Build one MAPS_TO fact from a contested candidate or settled map entry."""
    subject, quals = type_symbol_quals(str(class_name), source, base_quals=base_quals)
    return fact(
        predicate="MAPS_TO",
        subject=subject,
        object_=None if source.get("table") is None else str(source.get("table")),
        qualifiers=quals,
        file=None if source.get("file") is None else str(source.get("file")),
        line=source.get("line") if isinstance(source.get("line"), int) else None,
        rule_id=source.get("rule_id") or fallback_rule_id,
        scanner=source.get("scanner") or default_scanner,
    )


def contested_table_name_source(
    candidate: Mapping[str, Any],
    entry: Mapping[str, Any],
) -> Any:
    if candidate.get("table_name_source") is not None:
        return candidate.get("table_name_source")
    return entry.get("table_name_source")


def maps_to_from_contested_entry(
    class_name: str,
    entry: Mapping[str, Any],
    candidates: list,
    default_scanner: Optional[str],
) -> List[Dict[str, Any]]:
    """One MAPS_TO per contested table candidate."""
    facts: List[Dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        quals: Dict[str, Any] = {"status": "contested"}
        table_name_source = contested_table_name_source(candidate, entry)
        if table_name_source is not None:
            quals["table_name_source"] = table_name_source
        facts.append(
            maps_to_fact_from_source(
                class_name,
                candidate,
                base_quals=quals,
                default_scanner=default_scanner,
                fallback_rule_id=entry.get("rule_id"),
            )
        )
    return facts


def maps_to_from_settled_entry(
    class_name: str,
    entry: Mapping[str, Any],
    default_scanner: Optional[str],
) -> Dict[str, Any]:
    """One MAPS_TO for a non-contested entity_table_map entry."""
    quals: Dict[str, Any] = {}
    if entry.get("status") is not None:
        quals["status"] = entry.get("status")
    if entry.get("table_name_source") is not None:
        quals["table_name_source"] = entry.get("table_name_source")
    return maps_to_fact_from_source(
        class_name,
        entry,
        base_quals=quals,
        default_scanner=default_scanner,
    )


def is_contested_entry(entry: Mapping[str, Any]) -> bool:
    candidates = entry.get("candidates")
    return entry.get("status") == "contested" and isinstance(candidates, list) and bool(candidates)


def maps_to_from_one_entry(
    class_name: str,
    entry: Any,
    default_scanner: Optional[str],
) -> List[Dict[str, Any]]:
    if not isinstance(entry, Mapping):
        return []
    if is_contested_entry(entry):
        return maps_to_from_contested_entry(
            class_name, entry, entry.get("candidates"), default_scanner,
        )
    return [maps_to_from_settled_entry(class_name, entry, default_scanner)]


def maps_to_from_entity_table_map(
    entity_table_map: Mapping[str, Any],
    default_scanner: Optional[str],
) -> List[Dict[str, Any]]:
    """Derived stub: contested entries become one MAPS_TO per candidate.

    Each MAPS_TO subject is a type-level claim-symbol (distinct across packages).
    """
    facts: List[Dict[str, Any]] = []
    for class_name, entry in entity_table_map.items():
        facts.extend(maps_to_from_one_entry(class_name, entry, default_scanner))
    return facts
