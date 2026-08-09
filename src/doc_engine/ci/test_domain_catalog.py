"""Test-suite bounded-context catalog (E-TEST Spec T1 / policy T-A).

Closed registry of ``domain_*`` markers. Extend by adding a
:class:`TestDomain` entry — do not sprinkle marker strings through CI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR

ParallelDefault = Literal["parallel", "serial", "optin"]

# Same setpoint as Cover% / gap-average: meeting rate floor for doc_engine
# classification. Modules in domain_unclassified are the debt inventory;
# once reclassified they leave that inventory (gap-average analogy).
DOC_ENGINE_MEETING_FLOOR = DEFAULT_FLOOR
UNCLASSIFIED_MARKER = "domain_unclassified"


@dataclass(frozen=True)
class TestDomain:
    """One bounded test context (pytest marker + CI shard policy)."""

    marker: str
    parallel_default: ParallelDefault
    description: str


# Closed vocabulary — Spec T1 + explicit unclassified bucket (T3 machine form).
DOMAIN_CATALOG: tuple[TestDomain, ...] = (
    TestDomain(
        "domain_schemas",
        "parallel",
        "Artifact schemas, serde, and shape validators",
    ),
    TestDomain(
        "domain_stage0",
        "parallel",
        "Stage-0 signals, covering, gap_probe, facts/ETL",
    ),
    TestDomain(
        "domain_pipeline",
        "parallel",
        "Partition, capacity, pipeline stages, local_runner units",
    ),
    TestDomain(
        "domain_compliance",
        "parallel",
        "Compliance profiles and certification report units",
    ),
    TestDomain(
        "domain_ci_meta",
        "parallel",
        "CI scripts, ratchets, coverage meta tests",
    ),
    TestDomain(
        "domain_adapters",
        "parallel",
        "Adapter package tests",
    ),
    TestDomain(
        "domain_stf",
        "parallel",
        "STF package tests",
    ),
    TestDomain(
        "domain_climb_sensor",
        "parallel",
        "Coverage climb sensor suites (not oracle SoT)",
    ),
    TestDomain(
        "domain_integration",
        "serial",
        "Kitchen-sink / certified e2e / shared artifact env",
    ),
    TestDomain(
        "domain_live_optin",
        "optin",
        "Live OCS / real-world scans (skip-gated)",
    ),
    TestDomain(
        "domain_unclassified",
        "serial",
        "Debt inventory until reclassified (excluded once meeting; floor 98.7)",
    ),
)

_BY_MARKER = {domain.marker: domain for domain in DOMAIN_CATALOG}


def known_markers() -> frozenset[str]:
    """All registered ``domain_*`` marker names."""
    return frozenset(_BY_MARKER)


def require_domain(marker: str) -> TestDomain:
    """Lookup or raise — OCP extension point stays the catalog tuple."""
    try:
        return _BY_MARKER[marker]
    except KeyError as exc:
        known = ", ".join(sorted(_BY_MARKER))
        raise KeyError(f"unknown test domain {marker!r}; known: {known}") from exc


def parallel_shard_markers() -> tuple[str, ...]:
    """Markers safe for concurrent ABI CI jobs (policy T-A)."""
    return tuple(
        domain.marker
        for domain in DOMAIN_CATALOG
        if domain.parallel_default == "parallel"
    )


def serial_expression() -> str:
    """pytest ``-m`` expression for the serial ABI job."""
    serial = [
        domain.marker
        for domain in DOMAIN_CATALOG
        if domain.parallel_default in ("serial", "optin")
    ]
    return " or ".join(serial)


def pytest_marker_lines() -> tuple[str, ...]:
    """Lines for ``[tool.pytest.ini_options] markers`` registration."""
    return tuple(
        f"{domain.marker}: {domain.description}" for domain in DOMAIN_CATALOG
    )
