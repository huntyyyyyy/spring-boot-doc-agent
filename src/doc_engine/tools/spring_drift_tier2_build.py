"""Tier-2 rechecks for build-system signal citations."""

from __future__ import annotations

from collections import Counter

from doc_engine.paths import PathValidationError, join_under
from doc_engine.scanning.support._build_signal_extract import extract_build_signals
from doc_engine.tools.spring_drift_common import STATUS_CONFIRMED, STATUS_DRIFTED, drift_result


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

