"""JPQL dual-input provenance doors for spring_drift_check.

SoR: raw_queries entries whose lineage was resolved via an entity.
Derived: provenance reverify when that entity's file changed/deleted.

Door policy (both stamps required at every door):
- ``available`` — lineage resolution succeeded
- ``resolved_via_entity`` — which entity provided the table mapping

The writer (``resolve_jpql_to_lineage``) only sets the entity stamp when
available is true. Selector and actor both re-check both stamps so a stale
entity key on an unavailable lineage cannot open reverify.
"""

from __future__ import annotations

from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
    STATUS_UNCHANGED,
)


def _jpql_lineage_is_entity_resolved(lineage) -> bool:
    """True when lineage carries both guest-badge stamps for provenance."""
    return bool(
        lineage and lineage.get("available") and lineage.get("resolved_via_entity")
    )


def _raw_query_entries_with_resolved_entity(signals):
    """Yield raw_queries entries eligible for entity-provenance reverify."""
    for entry in signals.get("evidence", {}).get("raw_queries", []):
        if _jpql_lineage_is_entity_resolved(entry.get("lineage")):
            yield entry


def _jpql_lineage_needs_reverify(result) -> bool:
    return result is not None and result["status"] in (STATUS_UNCHANGED, STATUS_CONFIRMED)


def _apply_jpql_lineage_verdict(
    result, entity, entity_file, entity_meta, fresh, entity_file_deleted
):
    if fresh is None:
        result["status"] = STATUS_DRIFTED
        result["tier"] = 2
        if entity_file_deleted:
            result["detail"] = (
                f"JPQL lineage for this query was resolved via entity '{entity}', whose "
                f"defining file ({entity_file}) was deleted — lineage cannot be confirmed"
            )
        else:
            result["detail"] = (
                f"JPQL lineage for this query was resolved via entity '{entity}', which "
                f"persistence__entity no longer matches in its file ({entity_file}) — "
                f"lineage cannot be confirmed"
            )
        return
    if fresh.get("table") == entity_meta.get("table"):
        result["status"] = STATUS_CONFIRMED
        result["tier"] = 2
        result["detail"] = (
            f"own file unchanged; provenance entity '{entity}' ({entity_file}) changed but its "
            f"table mapping did not, so this query's lineage is still accurate"
        )
        return
    result["status"] = STATUS_DRIFTED
    result["tier"] = 2
    result["detail"] = (
        f"JPQL lineage for this query was resolved via entity '{entity}', whose table mapping "
        f"changed in a different file ({entity_file}): "
        f"{entity_meta.get('table')!r} -> {fresh.get('table')!r}"
    )


def _reverify_one_jpql_entry(
    entry,
    signals,
    fresh_entity_tables,
    changed_set,
    deleted_set,
    results_by_file_line,
) -> None:
    """Actor door: re-check both badge stamps before applying a verdict."""
    lineage = entry.get("lineage")
    if not _jpql_lineage_is_entity_resolved(lineage):
        return
    entity = lineage["resolved_via_entity"]
    entity_meta = signals.get("entity_table_map", {}).get(entity)
    if entity_meta is None:
        return
    entity_file = entity_meta.get("file")
    entity_file_deleted = entity_file in deleted_set
    if entity_file not in changed_set and not entity_file_deleted:
        return
    result = results_by_file_line.get((entry.get("file"), entry.get("line")))
    if not _jpql_lineage_needs_reverify(result):
        return
    fresh = fresh_entity_tables.get(entity)
    _apply_jpql_lineage_verdict(
        result, entity, entity_file, entity_meta, fresh, entity_file_deleted
    )


def _reverify_jpql_lineage_provenance(
    results, signals, fresh_entity_tables, changed_set, deleted_set
):
    """Reverify JPQL citations when their provenance entity file changed/deleted.

    Mutates ``results`` in place after the main per-file tier-2 loop.
    """
    results_by_file_line = {(row["file"], row["line"]): row for row in results}
    for entry in _raw_query_entries_with_resolved_entity(signals):
        _reverify_one_jpql_entry(
            entry,
            signals,
            fresh_entity_tables,
            changed_set,
            deleted_set,
            results_by_file_line,
        )
