"""Tier-2 rule rechecks: entity, repository, query, generic, config keys."""

from __future__ import annotations

import os
from collections import Counter

from doc_engine.scanning.support._config_keys import extract_config_keys
from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIG_STRUCTURE_CHANGED,
    STATUS_CONFIG_VALUES_ONLY_CHANGED,
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
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

