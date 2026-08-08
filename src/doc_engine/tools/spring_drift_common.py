"""Shared status constants and result shaping for spring drift check."""

# Every citation ends up with exactly one of these — nothing is ever
# silently dropped from the report.
STATUS_UNCHANGED = "unchanged"
STATUS_CONFIRMED = "confirmed_still_present"
STATUS_DRIFTED = "drifted"
STATUS_FILE_DELETED = "file_deleted"
STATUS_NO_RULE_FALLBACK = "suspected_drift_content_changed_no_rule_to_recheck"
STATUS_UNKNOWN_NO_SIGNATURE = "unknown_no_prior_signature"
# The two config-file-specific outcomes below only apply to files
# spring_signal_scan.py recorded a config_key_sets entry for (schema_version
# >= 5) — everything else with no rule_id still falls back to
# STATUS_NO_RULE_FALLBACK above. See _config_keys.py's module docstring for
# why these two are worth telling apart rather than lumping both under one
# generic "changed, can't precisely recheck" status.
STATUS_CONFIG_STRUCTURE_CHANGED = "config_structure_changed"
STATUS_CONFIG_VALUES_ONLY_CHANGED = "config_values_only_changed_review_needed"

# Wire version for drift_report.json (L5 thin operator schema). Bump only on
# breaking changes; additive fields keep the same version per rel-schema-outlives-writers.
DRIFT_REPORT_SCHEMA_VERSION = 1


def drift_result(source, citation, status, tier, detail=None):
    result = {
        "source": source,
        "file": citation.get("file"),
        "line": citation.get("line"),
        "rule_id": citation.get("rule_id"),
        "match": citation.get("match"),
        "status": status,
        "tier": tier,
    }
    if detail:
        result["detail"] = detail
    return result
