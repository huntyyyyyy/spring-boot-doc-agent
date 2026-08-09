"""Compliance profile resolution and stage-graph subset selection."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from doc_engine.pipeline.compliance_models import ComplianceProfile
from doc_engine.pipeline.context import StageKind, StageSpec


def resolve_compliance_profile(
    config: Any,
    args: Any,
) -> ComplianceProfile:
    """Merge CLI flags and repo config into one compliance profile."""
    explicit = getattr(args, "compliance_profile", None)
    if explicit:
        return ComplianceProfile(explicit)
    if getattr(args, "deterministic_only", False):
        return ComplianceProfile.DETERMINISTIC_ONLY
    if config is not None:
        profile = config.compliance_profile
        if isinstance(profile, ComplianceProfile):
            return profile
        return ComplianceProfile(profile)
    return ComplianceProfile.CERTIFIED


def citations_are_strict(
    profile: ComplianceProfile,
    *,
    force_strict: bool = False,
) -> bool:
    """Whether citation_coverage findings should fail the run.

    Same rule as ``local_runner``: certified profile always strict; otherwise
    only when the caller passes ``--strict-citations``.
    """
    return profile == ComplianceProfile.CERTIFIED or force_strict


def scan_only_specs(all_specs: list[StageSpec]) -> list[StageSpec]:
    """Stages allowed under the scan_only compliance profile."""
    allowed = {"init_manifest", "signal_scan"}
    return [spec for spec in all_specs if spec.name in allowed]


def specs_for_profile(profile: ComplianceProfile, all_specs: list[StageSpec]) -> list[StageSpec]:
    """Select the stage subset for a compliance profile (before filters)."""
    if profile == ComplianceProfile.CERTIFIED:
        return list(all_specs)
    if profile == ComplianceProfile.DETERMINISTIC_ONLY:
        return [spec for spec in all_specs if spec.kind == StageKind.DETERMINISTIC]
    return scan_only_specs(all_specs)


def truncate_until_stage(
    specs: list[StageSpec],
    until_stage: str,
    all_specs: list[StageSpec],
) -> list[StageSpec]:
    """Keep stages through *until_stage* inclusive; raise on unknown name."""
    names = [spec.name for spec in specs]
    if until_stage not in names:
        known = ", ".join(spec.name for spec in all_specs)
        raise ValueError(
            f"unknown --until stage {until_stage!r}; "
            f"known stage names: {known}"
        )
    cut = names.index(until_stage) + 1
    return specs[:cut]


def stages_for_profile(
    profile: ComplianceProfile,
    all_specs: list[StageSpec],
    *,
    skip_signal_scan: bool = False,
    until_stage: str | None = None,
) -> list[StageSpec]:
    """Return the stage graph subset required by a compliance profile.

    If ``until_stage`` is set, truncate after that stage name (inclusive).
    Stage names come from ``build_stage_specs()`` — the single SoT for the graph.
    """
    specs = specs_for_profile(profile, all_specs)
    if skip_signal_scan:
        specs = [spec for spec in specs if spec.name != "signal_scan"]
    if until_stage:
        specs = truncate_until_stage(specs, until_stage, all_specs)
    return specs


@lru_cache(maxsize=1)
def deterministic_stage_names() -> frozenset[str]:
    """Names of StageKind.DETERMINISTIC stages from ``build_stage_specs()``."""
    from doc_engine.pipeline.stages import build_stage_specs

    return frozenset(
        spec.name
        for spec in build_stage_specs()
        if spec.kind == StageKind.DETERMINISTIC
    )


@lru_cache(maxsize=1)
def generative_stage_names() -> frozenset[str]:
    """Names of StageKind.GENERATIVE stages from ``build_stage_specs()``."""
    from doc_engine.pipeline.stages import build_stage_specs

    return frozenset(
        spec.name for spec in build_stage_specs() if spec.kind == StageKind.GENERATIVE
    )


def required_stage_names_for_profile(profile: ComplianceProfile) -> frozenset[str]:
    """Stage names the profile expects to have run (skips of these fail cert)."""
    from doc_engine.pipeline.stages import build_stage_specs

    return frozenset(
        spec.name for spec in stages_for_profile(profile, build_stage_specs())
    )
