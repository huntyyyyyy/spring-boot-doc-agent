"""Tier-2 citation rechecks for spring_drift_check (SRP: precise per-rule).

Helpers live in ``spring_drift_tier2_rules`` / ``spring_drift_tier2_build``;
this module owns dispatch + ``tier2_recheck_file`` and re-exports helpers for
stable ``from doc_engine.tools import spring_drift_tier2 as t2`` climb tests.
"""

from __future__ import annotations

from doc_engine.tools.spring_drift_tier2_build import (
    _is_build_signal_rule,
    _recheck_build_signals,
)
from doc_engine.tools.spring_drift_tier2_rules import (
    _recheck_entities,
    _recheck_generic,
    _recheck_queries,
    _recheck_repositories,
)


def _private_module_attrs(module) -> dict:
    """Return underscore-prefixed public helpers from a concept module."""
    return {
        name: value
        for name, value in vars(module).items()
        if name.startswith("_") and not name.startswith("__")
    }


def _bind_helper_reexports() -> None:
    """Expose rule/build helpers on this module for characterization imports."""
    from doc_engine.tools import spring_drift_tier2_build as build
    from doc_engine.tools import spring_drift_tier2_rules as rules

    globals().update(_private_module_attrs(rules))
    globals().update(_private_module_attrs(build))


_bind_helper_reexports()


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
