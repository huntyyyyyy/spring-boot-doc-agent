"""MeasureMode strategies — how oracle vs climb runs pytest-cov.

Strategies own argv, wipe set, banner, and whether fail_under / gap-report
apply. Artifact *filenames* and gap-inventory refuse live in
``coverage_artifact_policy`` (policy 16-A). Shared wipe + PathCohesion stay
on ``MeasureRun``.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Protocol, Sequence

from doc_engine._compat import StrEnum
from doc_engine.ci.coverage_artifact_policy import (
    CLIMB_BANNER,
    CLIMB_XML_NAME,
    ORACLE_XML_NAME,
)


class MeasureMode(StrEnum):
    """Labeled coverage-measure mode (CLI ``--mode``)."""

    ORACLE = "oracle"
    CLIMB = "climb"


def _pytest_base_argv() -> list[str]:
    return [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=line"]


def _extend_pytest_args(
    cmd: list[str], extra_pytest_args: Sequence[str] | None
) -> list[str]:
    if extra_pytest_args:
        cmd.extend(extra_pytest_args)
    return cmd


class MeasureStrategy(Protocol):
    """Hexagonal port: build pytest-cov argv + wipe set for one mode."""

    mode: MeasureMode

    @property
    def xml_name(self) -> str:
        """Cobertura filename written by this mode."""

    @property
    def wipe_xml_names(self) -> tuple[str, ...]:
        """XML basenames wiped before a fresh run of this mode."""

    def pytest_cov_argv(
        self,
        *,
        fail_under_floor: float | None,
        extra_pytest_args: Sequence[str] | None,
    ) -> list[str]:
        """Full ``python -m pytest ...`` argv for this mode."""

    def emit_banner(self) -> None:
        """Print mode banner to stderr when required."""

    def allows_gap_report(self) -> bool:
        """Whether gap-average may run against this mode's XML."""

    def allows_fail_under(self) -> bool:
        """Whether whole-repo ``fail_under`` may be applied."""


@dataclass(frozen=True)
class OracleMeasureStrategy:
    """Whole-repo CI/release SoT measure."""

    mode: MeasureMode = MeasureMode.ORACLE

    @property
    def xml_name(self) -> str:
        return ORACLE_XML_NAME

    @property
    def wipe_xml_names(self) -> tuple[str, ...]:
        return (ORACLE_XML_NAME, CLIMB_XML_NAME)

    def pytest_cov_argv(
        self,
        *,
        fail_under_floor: float | None,
        extra_pytest_args: Sequence[str] | None,
    ) -> list[str]:
        if fail_under_floor is None:
            raise ValueError("oracle mode requires fail_under_floor")
        cmd = _pytest_base_argv() + [
            "--cov=doc_engine",
            "--cov=stf",
            "--cov-branch",
            "--cov-report=term-missing",
            "--cov-report=xml",
            f"--cov-fail-under={fail_under_floor}",
        ]
        return _extend_pytest_args(cmd, extra_pytest_args)

    def emit_banner(self) -> None:
        return None

    def allows_gap_report(self) -> bool:
        return True

    def allows_fail_under(self) -> bool:
        return True


@dataclass(frozen=True)
class ClimbMeasureStrategy:
    """Scoped climb sensor — never claims the repo floor (policy 16-A)."""

    scope_package: str
    mode: MeasureMode = MeasureMode.CLIMB

    def __post_init__(self) -> None:
        if not self.scope_package.strip():
            raise ValueError("climb mode requires a non-empty scope_package")

    @property
    def xml_name(self) -> str:
        return CLIMB_XML_NAME

    @property
    def wipe_xml_names(self) -> tuple[str, ...]:
        # Never delete oracle SoR coverage.xml during climb wipe.
        return (CLIMB_XML_NAME,)

    def pytest_cov_argv(
        self,
        *,
        fail_under_floor: float | None,
        extra_pytest_args: Sequence[str] | None,
    ) -> list[str]:
        del fail_under_floor  # climb never applies whole-repo fail_under
        cmd = _pytest_base_argv() + [
            f"--cov={self.scope_package}",
            "--cov-branch",
            "--cov-report=term-missing",
            f"--cov-report=xml:{CLIMB_XML_NAME}",
        ]
        return _extend_pytest_args(cmd, extra_pytest_args)

    def emit_banner(self) -> None:
        print(CLIMB_BANNER, file=sys.stderr, flush=True)

    def allows_gap_report(self) -> bool:
        return False

    def allows_fail_under(self) -> bool:
        return False


def strategy_for(
    mode: MeasureMode,
    *,
    scope_package: str | None = None,
) -> MeasureStrategy:
    """Factory: select oracle or climb strategy (no mode-boolean soup)."""
    if mode is MeasureMode.ORACLE:
        return OracleMeasureStrategy()
    if scope_package is None or not scope_package.strip():
        raise ValueError("climb mode requires --scope <package>")
    return ClimbMeasureStrategy(scope_package=scope_package.strip())
