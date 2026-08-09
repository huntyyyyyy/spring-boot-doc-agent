"""Ordered classification rules for test module → domain marker (E-TEST).

Chain-of-responsibility over an immutable rule tuple — add a rule to extend
(OCP); first match wins. Spec appendix §11 ownership map.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from doc_engine.ci.test_domain_catalog import require_domain


class ClassificationRule(Protocol):
    """Strategy: maybe map a repo-relative POSIX test path to a marker."""

    def match(self, rel_posix: str, filename: str) -> str | None:
        """Return ``domain_*`` marker or None when this rule does not apply."""


@dataclass(frozen=True)
class DirPrefixRule:
    """Match tests living under a directory prefix (``tests/ci/``)."""

    prefix: str
    marker: str

    def match(self, rel_posix: str, filename: str) -> str | None:
        del filename
        require_domain(self.marker)
        normalized = rel_posix if rel_posix.endswith("/") else rel_posix
        if normalized.startswith(self.prefix.rstrip("/") + "/") or normalized == (
            self.prefix.rstrip("/")
        ):
            return self.marker
        return None


@dataclass(frozen=True)
class FilenamePrefixRule:
    """Match ``test_<prefix>…`` basenames (optionally under a dir prefix)."""

    name_prefix: str
    marker: str
    under: str | None = None

    def match(self, rel_posix: str, filename: str) -> str | None:
        require_domain(self.marker)
        if self.under is not None and not rel_posix.startswith(
            self.under.rstrip("/") + "/"
        ):
            return None
        if filename.startswith(self.name_prefix):
            return self.marker
        return None


@dataclass(frozen=True)
class FilenameContainsRule:
    """Match basename substring (e.g. ``ocs_real_world``, ``schema``)."""

    needle: str
    marker: str
    under: str | None = None

    def match(self, rel_posix: str, filename: str) -> str | None:
        require_domain(self.marker)
        if self.under is not None and not rel_posix.startswith(
            self.under.rstrip("/") + "/"
        ):
            return None
        if self.needle in filename:
            return self.marker
        return None


@dataclass(frozen=True)
class FallbackUnclassified:
    """Terminal rule — every remaining ``test_*.py`` is explicit serial."""

    def match(self, rel_posix: str, filename: str) -> str | None:
        del rel_posix, filename
        return "domain_unclassified"


# Specific → general. Dir rules before loose filename contains.
CLASSIFICATION_RULES: tuple[ClassificationRule, ...] = (
    DirPrefixRule("tests/ci", "domain_ci_meta"),
    DirPrefixRule("tests/ratchets", "domain_ci_meta"),
    DirPrefixRule("tests/coverage", "domain_ci_meta"),
    DirPrefixRule("tests/adapters", "domain_adapters"),
    DirPrefixRule("tests/stf", "domain_stf"),
    DirPrefixRule("tests/spring_signals", "domain_stage0"),
    DirPrefixRule("tests/research", "domain_ci_meta"),
    DirPrefixRule("tests/fixtures", "domain_ci_meta"),
    FilenameContainsRule("ocs_real_world", "domain_live_optin"),
    # Real-repo kitchen-sink lane is opt-in (skipUnless); do not serial-ABI it.
    FilenameContainsRule("kitchen_sink_real_repo", "domain_live_optin"),
    FilenamePrefixRule("test_kitchen_sink", "domain_integration"),
    FilenamePrefixRule("test_enterprise_kitchen", "domain_integration"),
    FilenamePrefixRule("test_local_runner_certified", "domain_integration"),
    FilenamePrefixRule("test_coverage_climb_", "domain_climb_sensor"),
    FilenamePrefixRule("test_artifact_", "domain_schemas"),
    FilenameContainsRule("schema", "domain_schemas", under="tests/doc_engine"),
    FilenamePrefixRule("test_gap_probe", "domain_stage0"),
    FilenamePrefixRule("test_covering", "domain_stage0"),
    FilenamePrefixRule("test_absence_", "domain_stage0"),
    FilenamePrefixRule("test_facts_", "domain_stage0"),
    FilenameContainsRule("etl", "domain_stage0", under="tests/doc_engine"),
    FilenameContainsRule("signal", "domain_stage0", under="tests/doc_engine"),
    FilenamePrefixRule("test_pipeline_", "domain_pipeline"),
    FilenamePrefixRule("test_partition_", "domain_pipeline"),
    FilenamePrefixRule("test_capacity_", "domain_pipeline"),
    FilenamePrefixRule("test_local_runner", "domain_pipeline"),
    FilenamePrefixRule("test_build_cross_group", "domain_pipeline"),
    FilenamePrefixRule("test_context_packet", "domain_pipeline"),
    FilenamePrefixRule("test_compliance", "domain_compliance"),
    FilenameContainsRule("cert", "domain_compliance", under="tests/doc_engine"),
    # Stage-0 / scan surface (doc_engine meeting floor 98.7; debt=unclassified)
    FilenamePrefixRule("test_codeql_", "domain_stage0"),
    FilenamePrefixRule("test_find_codeql", "domain_stage0"),
    FilenamePrefixRule("test_scan_context_", "domain_stage0"),
    FilenamePrefixRule("test_scan_parity", "domain_stage0"),
    FilenamePrefixRule("test_portable_stage0", "domain_stage0"),
    FilenamePrefixRule("test_stage0_", "domain_stage0"),
    FilenamePrefixRule("test_spring_drift_", "domain_stage0"),
    FilenamePrefixRule("test_real_fixture", "domain_stage0"),
    FilenamePrefixRule("test_jpql_", "domain_stage0"),
    FilenamePrefixRule("test_java_extract_", "domain_stage0"),
    FilenamePrefixRule("test_symbol", "domain_stage0"),
    FilenamePrefixRule("test_walk_containment", "domain_stage0"),
    FilenamePrefixRule("test_dependents_", "domain_stage0"),
    FilenamePrefixRule("test_merge_", "domain_stage0"),
    FilenamePrefixRule("test_build_command", "domain_stage0"),
    FilenamePrefixRule("test_secret_heuristics", "domain_stage0"),
    FilenamePrefixRule("test_repo_trust", "domain_stage0"),
    # Pipeline / gates / citations / query surface
    FilenamePrefixRule("test_mock_stages_", "domain_pipeline"),
    FilenamePrefixRule("test_live_gates_", "domain_pipeline"),
    FilenamePrefixRule("test_citation_", "domain_pipeline"),
    FilenamePrefixRule("test_semantic_eval_", "domain_pipeline"),
    FilenamePrefixRule("test_freshness_", "domain_pipeline"),
    FilenamePrefixRule("test_query_", "domain_pipeline"),
    FilenamePrefixRule("test_validate_artifacts_", "domain_schemas"),
    FilenamePrefixRule("test_core_jsonio", "domain_schemas"),
    # Final doc_engine leftovers → named BCs (labeled share floor 98.7)
    FilenamePrefixRule("test_cli_unit", "domain_pipeline"),
    FilenamePrefixRule("test_doc_engine", "domain_pipeline"),
    FilenamePrefixRule("test_config_keys", "domain_pipeline"),
    FilenamePrefixRule("test_search_methodology", "domain_stage0"),
    FilenamePrefixRule("test_paths", "domain_ci_meta"),
    FilenamePrefixRule("test_wave1_complexity_helpers", "domain_ci_meta"),
    FallbackUnclassified(),
)
