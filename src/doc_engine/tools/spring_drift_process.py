"""Per-file citation processing for drift check (tier-1 status + tier-2)."""

from __future__ import annotations

from doc_engine.tools.spring_drift_common import (
    STATUS_FILE_DELETED,
    STATUS_NO_RULE_FALLBACK,
    STATUS_UNCHANGED,
    STATUS_UNKNOWN_NO_SIGNATURE,
    drift_result,
)
from doc_engine.tools.spring_drift_tier1 import all_citations
from doc_engine.tools.spring_drift_tier2 import tier2_recheck_file
from doc_engine.tools.spring_drift_tier2_rules import _recheck_config_keys


def _unchanged_fast_path_results(signals):
    return [
        drift_result(source, citation, STATUS_UNCHANGED, 1)
        for source, citation in all_citations(signals)
    ]


def _index_fresh_evidence_by_file(fresh_signals):
    fresh_evidence_by_file = {}
    for _bucket_name, entries in fresh_signals.get("evidence", {}).items():
        for entry in entries:
            fresh_evidence_by_file.setdefault(entry.get("file", ""), []).append(entry)
    return fresh_evidence_by_file


def _group_citations_by_file(signals):
    citations_by_file = {}
    for source, citation in all_citations(signals):
        citations_by_file.setdefault(citation["file"], []).append((source, citation))
    return citations_by_file


def _append_uniform_status(results, citations, status, detail=None):
    for source, citation in citations:
        results.append(drift_result(source, citation, status, 1, detail))


def _recheck_citations_without_rule(repo_path, file_rel, without_rule, old_key_set, results):
    for source, citation in without_rule:
        outcome = (
            _recheck_config_keys(repo_path, file_rel, old_key_set)
            if old_key_set is not None
            else None
        )
        if outcome is not None:
            status, detail = outcome
            results.append(drift_result(source, citation, status, 1, detail))
            continue
        results.append(drift_result(
            source, citation, STATUS_NO_RULE_FALLBACK, 1,
            detail=(
                "file content changed and this citation has no rule_id to precisely recheck "
                "(filename-based evidence, e.g. config/deployment/migration match)"
            ),
        ))


def _process_changed_file_citations(
    repo_path,
    file_rel,
    citations,
    signals,
    fresh_evidence_by_file,
    fresh_entity_map,
    results,
    fresh_entity_tables,
):
    with_rule = [
        (source, citation) for source, citation in citations if citation.get("rule_id")
    ]
    without_rule = [
        (source, citation) for source, citation in citations if not citation.get("rule_id")
    ]
    old_key_set = signals.get("config_key_sets", {}).get(file_rel)
    _recheck_citations_without_rule(repo_path, file_rel, without_rule, old_key_set, results)
    if not with_rule:
        return
    file_results, file_fresh_entities = tier2_recheck_file(
        repo_path, file_rel, with_rule, fresh_evidence_by_file, fresh_entity_map
    )
    results.extend(file_results)
    fresh_entity_tables.update(file_fresh_entities)


def _process_file_citations(
    repo_path,
    file_rel,
    citations,
    *,
    deleted_set,
    unchanged_set,
    changed_set,
    signals,
    fresh_evidence_by_file,
    fresh_entity_map,
    results,
    fresh_entity_tables,
):
    if file_rel in deleted_set:
        _append_uniform_status(results, citations, STATUS_FILE_DELETED)
        return
    if file_rel in unchanged_set:
        _append_uniform_status(results, citations, STATUS_UNCHANGED)
        return
    if file_rel not in changed_set:
        # Cited but absent from both prior and fresh signature sets.
        _append_uniform_status(
            results,
            citations,
            STATUS_UNKNOWN_NO_SIGNATURE,
            detail="no prior file_signatures entry for this file to compare against",
        )
        return
    _process_changed_file_citations(
        repo_path,
        file_rel,
        citations,
        signals,
        fresh_evidence_by_file,
        fresh_entity_map,
        results,
        fresh_entity_tables,
    )

