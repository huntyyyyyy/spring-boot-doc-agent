"""Tier-2 citation rechecks for spring_drift_check (SRP: precise per-rule)."""

from __future__ import annotations

import os
from collections import Counter

from doc_engine.paths import PathValidationError, join_under
from doc_engine.scanning.support._build_signal_extract import extract_build_signals
from doc_engine.scanning.support._config_keys import extract_config_keys
from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIG_STRUCTURE_CHANGED,
    STATUS_CONFIG_VALUES_ONLY_CHANGED,
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
    STATUS_UNCHANGED,
    drift_result,
)


def _entity_missing_detail(class_name):
    if class_name:
        return f"class '{class_name}' no longer matched by persistence__entity"
    return (
        "citation has no class_name to re-verify against "
        "(unexpected — treating conservatively as drift)"
    )


def _entity_table_fields_changed(citation, fresh) -> bool:
    table_changed = "table" in citation and fresh.get("table") != citation.get("table")
    source_changed = (
        "table_name_source" in citation
        and fresh.get("table_name_source") != citation.get("table_name_source")
    )
    return table_changed or source_changed


def _entity_citation_verdict(citation, fresh_entities):
    class_name = citation.get("class_name")
    fresh = fresh_entities.get(class_name) if class_name else None
    if fresh is None:
        return STATUS_DRIFTED, _entity_missing_detail(class_name)
    if _entity_table_fields_changed(citation, fresh):
        detail = f"table mapping changed: {citation.get('table')!r} -> {fresh.get('table')!r}"
        return STATUS_DRIFTED, detail
    return STATUS_CONFIRMED, None


def _recheck_entities(fresh_entity_map, group):
    """group: citations whose rule_id is persistence__entity.

    fresh_entity_map: the current entity_table_map from a fresh
    spring_signal_scan.scan() of the repo (class_name -> entry).

    Returns (results, fresh_entities): fresh_entities is the class_name ->
    {"table", "table_name_source"} map used for comparison — exposed to the
    caller so JPQL lineage provenance (_reverify_jpql_lineage_provenance) can
    reuse it without a second scan."""
    fresh_entities = dict(fresh_entity_map) if fresh_entity_map else {}
    results = []
    for source, citation in group:
        status, detail = _entity_citation_verdict(citation, fresh_entities)
        results.append(drift_result(source, citation, status, 2, detail))
    return results, fresh_entities


def _repository_missing_detail(repository_name):
    if repository_name:
        return f"repository '{repository_name}' no longer matched by persistence__repository"
    return (
        "citation has no repository name to re-verify against "
        "(unexpected — treating conservatively as drift)"
    )


def _repository_type_args_changed(citation, fresh) -> bool:
    return (
        fresh.get("entity") != citation.get("entity")
        or fresh.get("id_type") != citation.get("id_type")
    )


def _repository_citation_verdict(citation, fresh_repos):
    repository_name = citation.get("repository")
    fresh = fresh_repos.get(repository_name) if repository_name else None
    if fresh is None:
        return STATUS_DRIFTED, _repository_missing_detail(repository_name)
    if _repository_type_args_changed(citation, fresh):
        detail = (
            f"repository type args changed: <{citation.get('entity')}, {citation.get('id_type')}> "
            f"-> <{fresh.get('entity')}, {fresh.get('id_type')}>"
        )
        return STATUS_DRIFTED, detail
    return STATUS_CONFIRMED, None


def _recheck_repositories(fresh_repo_entries, group):
    """fresh_repo_entries: current persistence__repository evidence entries
    from a fresh scan. Each entry is expected to carry repository, entity, and
    id_type fields (spring_signal_scan.py adds them for persistence__repository)."""
    fresh_repos = {}
    for entry in fresh_repo_entries:
        repository_name = entry.get("repository")
        if repository_name:
            fresh_repos[repository_name] = entry

    results = []
    for source, citation in group:
        status, detail = _repository_citation_verdict(citation, fresh_repos)
        results.append(drift_result(source, citation, status, 2, detail))
    return results


def _recheck_queries(fresh_query_entries, group):
    """fresh_query_entries: current raw_queries__query evidence entries from a
    fresh scan. Each entry carries query_kind and query (spring_signal_scan.py
    extracts both from @Query annotations)."""
    fresh_counts = Counter()
    for entry in fresh_query_entries:
        fresh_counts[(entry.get("query_kind"), entry.get("query"))] += 1

    budget = dict(fresh_counts)
    results = []
    for source, citation in group:
        key = (citation.get("query_kind"), citation.get("query"))
        if budget.get(key, 0) > 0:
            budget[key] -= 1
            results.append(drift_result(source, citation, STATUS_CONFIRMED, 2))
        else:
            detail = "no fresh @Query match with the same query text and kind found in this file"
            results.append(drift_result(source, citation, STATUS_DRIFTED, 2, detail))
    return results


def _recheck_generic(fresh_entries, group):
    """Fallback for every rule type without a specialized extractor. Most
    of these are single-line annotation matches (api_surface, security,
    messaging, observability, ...) where the stored `match` field is a
    meaningful shape comparison, so we compare it against the fresh scan's
    match values for the same rule in the same file."""
    fresh_counts = Counter(e.get("match") for e in fresh_entries)
    budget = dict(fresh_counts)
    results = []
    for source, citation in group:
        key = citation.get("match")
        if budget.get(key, 0) > 0:
            budget[key] -= 1
            results.append(drift_result(source, citation, STATUS_CONFIRMED, 2))
        else:
            detail = "no fresh match with the same text found for this rule in this file"
            results.append(drift_result(source, citation, STATUS_DRIFTED, 2, detail))
    return results


def _raw_query_entries_with_resolved_entity(signals):
    """Single responsibility: yield every raw_queries entry whose JPQL
    lineage was resolved through an entity (lineage.resolved_via_entity,
    spring_signal_scan.py schema_version >= 6) — the only citations with a
    second provenance input beyond their own file. Native-query entries and
    out-of-scope/unavailable JPQL entries (no resolved_via_entity key at
    all — see resolve_jpql_to_lineage()) are silently skipped, not an
    oversight: they have exactly one input (their own file), already
    covered by the ordinary per-file tier-1/tier-2 loop."""
    for entry in signals.get("evidence", {}).get("raw_queries", []):
        lineage = entry.get("lineage")
        if lineage and lineage.get("resolved_via_entity"):
            yield entry


def _jpql_lineage_needs_reverify(result) -> bool:
    return result is not None and result["status"] in (STATUS_UNCHANGED, STATUS_CONFIRMED)


def _apply_jpql_lineage_verdict(result, entity, entity_file, entity_meta, fresh, entity_file_deleted):
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
                f"persistence__entity no longer matches in its file ({entity_file}) — lineage cannot be confirmed"
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
        f"changed in a different file ({entity_file}): {entity_meta.get('table')!r} -> {fresh.get('table')!r}"
    )


def _reverify_one_jpql_entry(
    entry,
    signals,
    fresh_entity_tables,
    changed_set,
    deleted_set,
    results_by_file_line,
) -> None:
    entity = entry["lineage"]["resolved_via_entity"]
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


def _reverify_jpql_lineage_provenance(results, signals, fresh_entity_tables, changed_set, deleted_set):
    """A JPQL citation's lineage is DERIVED from two inputs, not one: the
    query text (its own file, already handled by the per-file loop that
    produced `results`) and the entity->table mapping (a different file,
    entity_table_map[entity]["file"]). This citation is fresh only if BOTH
    inputs are unchanged — the same freshness rule every other,
    single-input citation already follows, just honestly widened for the
    one citation type that actually has a second input, rather than a
    special-cased "dependent entity" status. Mutates `results` in place;
    runs once, after the main per-file loop, so it doesn't depend on
    whether the query's file or the entity's file happened to be processed
    first (ast-grep's per-repo match order isn't guaranteed stable either —
    see spring_signal_scan.py's own JPQL-resolution pass for the same
    reasoning).

    A "changed" input file is not the only way the second input can go
    stale: DELETING (or moving, which classify_files() reports as a delete
    of the old path) the entity's file also invalidates the mapping. So the
    entity-provenance gate fires for changed_set OR deleted_set — a deleted
    entity file simply has no fresh scan, so it flows into the fresh-is-None
    -> DRIFTED branch below with a delete-specific detail. Without this, a
    JPQL query whose entity class file was deleted would come back
    "unchanged" with silently stale lineage — the exact miss this whole
    provenance pass exists to prevent, in its deletion variant.

    fresh_entity_tables: class_name -> fresh {"table", ...} dict, built as
    a side effect of the main loop's own ast-grep re-run on entity files
    already in changed_set (see _recheck_entities) — reused here rather
    than triggering a second ast-grep invocation against the same file. A
    deleted entity file is never tier-2 rechecked, so it never appears here,
    which is exactly why fresh-is-None is the correct deletion signal."""
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


def _recheck_config_keys(repo_path, file_rel, old_keys):
    """Compares a config/deployment file's stored key set (from a prior
    scan's config_key_sets) against a fresh extraction of the file as it
    exists now. Returns (status, detail), or None if the file can't be
    read (caller falls back to the generic no-rule status in that case).
    """
    full_path = os.path.join(repo_path, file_rel)
    try:
        with open(full_path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except OSError:
        return None

    new_keys = set(extract_config_keys(text, os.path.basename(file_rel)))
    old_keys = set(old_keys)

    if new_keys != old_keys:
        added = sorted(new_keys - old_keys)
        removed = sorted(old_keys - new_keys)
        detail = f"config key set changed: added {added or '[]'}, removed {removed or '[]'}"
        return STATUS_CONFIG_STRUCTURE_CHANGED, detail

    detail = (
        "file content changed but the config key set did not — a value changed under an "
        "unchanged key, worth a human look rather than treating as routine"
    )
    return STATUS_CONFIG_VALUES_ONLY_CHANGED, detail


def _identity_build_plugin(row):
    return (row.get("rule_id"), row.get("plugin_id"), row.get("plugin_version"))


def _identity_build_dependency(row):
    coordinate = row.get("coordinate") or {}
    return (
        row.get("rule_id"),
        row.get("configuration"),
        coordinate.get("group"),
        coordinate.get("name"),
        coordinate.get("version"),
    )


def _identity_build_module(row):
    return (row.get("rule_id"), row.get("module"))


def _identity_build_toolchain(row):
    return (row.get("rule_id"), row.get("toolchain_kind"), row.get("toolchain_value"))


def _identity_version_catalog(row):
    return (row.get("rule_id"), row.get("catalog_kind"), row.get("catalog_key"))


def _identity_fallback_match(row):
    return (row.get("rule_id"), row.get("match"))


_BUILD_SIGNAL_IDENTITY = {
    "deployment__build_plugin": _identity_build_plugin,
    "deployment__build_dependency": _identity_build_dependency,
    "deployment__build_module": _identity_build_module,
    "deployment__build_toolchain": _identity_build_toolchain,
    "deployment__version_catalog": _identity_version_catalog,
}


def _build_signal_identity(row):
    builder = _BUILD_SIGNAL_IDENTITY.get(row.get("rule_id"), _identity_fallback_match)
    return builder(row)


def _consume_identity_budget(budget, key, source, citation, missing_detail):
    if budget.get(key, 0) > 0:
        budget[key] -= 1
        return drift_result(source, citation, STATUS_CONFIRMED, 2)
    return drift_result(source, citation, STATUS_DRIFTED, 2, missing_detail)


def _drifted_group(group, detail: str):
    return [
        drift_result(source, citation, STATUS_DRIFTED, 2, detail)
        for source, citation in group
    ]


def _read_build_file_text(repo_path, file_rel, group):
    try:
        full_path = join_under(repo_path, file_rel)
    except PathValidationError as exc:
        return None, _drifted_group(
            group, f"could not read build file for re-verification: {exc}"
        )
    try:
        with open(full_path, encoding="utf-8-sig", errors="replace") as handle:
            return handle.read(), None
    except OSError as exc:
        return None, _drifted_group(
            group, f"could not read build file for re-verification: {exc}"
        )


def _recheck_build_signals(repo_path, file_rel, group):
    """Tier-2 for the synthetic build-file rule ids produced by
    _build_signal_extract.py. Reads the file, re-runs the extractor, and
    compares by structured identity (plugin_id, coordinate, module,
    toolchain, catalog key) rather than by raw match text, since the same
    line can match multiple rules and the match text is not distinctive."""
    text, err_results = _read_build_file_text(repo_path, file_rel, group)
    if err_results is not None:
        return err_results

    fresh = extract_build_signals(file_rel, text)
    budget = dict(Counter(_build_signal_identity(row) for row in fresh))
    results = []
    for source, citation in group:
        key = _build_signal_identity(citation)
        detail = f"no fresh build signal match for {citation.get('rule_id')} identity {key}"
        results.append(_consume_identity_budget(budget, key, source, citation, detail))
    return results


def _is_build_signal_rule(rule_id: str) -> bool:
    return rule_id.startswith("deployment__build_") or rule_id == "deployment__version_catalog"


def _dispatch_tier2_rule(
    rule_id,
    group,
    *,
    repo_path,
    file_rel,
    fresh_by_rule,
    fresh_entity_map,
    results,
    fresh_entity_tables,
):
    if _is_build_signal_rule(rule_id):
        results.extend(_recheck_build_signals(repo_path, file_rel, group))
        return fresh_entity_tables
    fresh = fresh_by_rule.get(rule_id, [])
    if rule_id == "persistence__entity":
        entity_results, fresh_entity_tables = _recheck_entities(fresh_entity_map, group)
        results.extend(entity_results)
        return fresh_entity_tables
    if rule_id == "persistence__repository":
        results.extend(_recheck_repositories(fresh, group))
        return fresh_entity_tables
    if rule_id == "raw_queries__query":
        results.extend(_recheck_queries(fresh, group))
        return fresh_entity_tables
    results.extend(_recheck_generic(fresh, group))
    return fresh_entity_tables


def tier2_recheck_file(repo_path, file_rel, citations_for_file, fresh_evidence_by_file, fresh_entity_map):
    """citations_for_file: list of (source, citation), all sharing file_rel,
    all with a rule_id (caller filters out the no-rule_id ones first).

    fresh_evidence_by_file: file_rel -> list of fresh evidence entries from a
    current spring_signal_scan.scan() of the repo.

    fresh_entity_map: the fresh entity_table_map from the same scan.

    Returns (results, fresh_entity_tables) — the latter is {} unless this
    file actually has persistence__entity citations, in which case it's
    _recheck_entities' fresh_entities map passed straight through."""
    fresh_by_rule = {}
    for entry in fresh_evidence_by_file.get(file_rel, []):
        fresh_by_rule.setdefault(entry.get("rule_id"), []).append(entry)

    old_by_rule = {}
    for source, citation in citations_for_file:
        old_by_rule.setdefault(citation["rule_id"], []).append((source, citation))

    results = []
    fresh_entity_tables = {}
    for rule_id, group in old_by_rule.items():
        fresh_entity_tables = _dispatch_tier2_rule(
            rule_id,
            group,
            repo_path=repo_path,
            file_rel=file_rel,
            fresh_by_rule=fresh_by_rule,
            fresh_entity_map=fresh_entity_map,
            results=results,
            fresh_entity_tables=fresh_entity_tables,
        )
    return results, fresh_entity_tables
