"""MeasureRun — single-writer coverage measure for one checkout.

Wipes cwd-local ``.coverage*`` and mode XML artifacts, runs one pytest+cov,
validates path cohesion. Never combines coverage DBs across worktrees.
Modes: oracle (SoR → ``coverage.xml``) vs climb (``coverage.climb.xml``, 16-A).

Usage:
    doc-engine coverage-measure
    python -m doc_engine.ci.coverage_measure --floor 98.7

Exit codes: 0 ok; 1 pytest/fail_under failed; 2 cohesion/missing/bad args
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR
from doc_engine.ci.coverage_measure_modes import (
    MeasureStrategy,
    OracleMeasureStrategy,
)
from doc_engine.ci.coverage_path_cohesion import PathCohesionError, PathCohesionGuard
from doc_engine.ci.coverage_report import load_cobertura_report


def _unlink_coverage_dbs(cwd: Path) -> list[Path]:
    removed: list[Path] = []
    for path in sorted(cwd.glob(".coverage*")):
        if path.is_file():
            path.unlink()
            removed.append(path)
    return removed


def _unlink_named_xml(cwd: Path, names: tuple[str, ...]) -> list[Path]:
    removed: list[Path] = []
    for name in names:
        xml = cwd / name
        if xml.is_file():
            xml.unlink()
            removed.append(xml)
    return removed


class MeasureRun:
    """Single-writer measure in *cwd* — wipe, one pytest+cov, cohesion check."""

    def __init__(
        self,
        cwd: Path | None = None,
        *,
        strategy: MeasureStrategy | None = None,
    ) -> None:
        self.cwd = (cwd or Path.cwd()).resolve()
        self.strategy = strategy or OracleMeasureStrategy()

    def wipe_local_artifacts(self) -> list[Path]:
        """Delete cwd-local coverage DB + this mode's XML artifacts only."""
        return _unlink_coverage_dbs(self.cwd) + _unlink_named_xml(
            self.cwd, self.strategy.wipe_xml_names
        )

    def run_pytest_cov(
        self,
        *,
        fail_under: float = DEFAULT_FLOOR,
        extra_pytest_args: list[str] | None = None,
    ) -> int:
        """One pytest+cov run; XML path comes from the active strategy."""
        floor = fail_under if self.strategy.allows_fail_under() else None
        cmd = self.strategy.pytest_cov_argv(
            fail_under_floor=floor,
            extra_pytest_args=extra_pytest_args,
        )
        return int(subprocess.run(cmd, cwd=str(self.cwd), check=False).returncode)

    def load_and_validate(self) -> Path:
        """Require this mode's XML in cwd with cohesive source paths."""
        xml_path = self.cwd / self.strategy.xml_name
        if not xml_path.is_file():
            raise FileNotFoundError(f"missing coverage report: {xml_path}")
        report = load_cobertura_report(xml_path)
        PathCohesionGuard(self.cwd).assert_cohesive(report.source_paths())
        return xml_path

    def _run_then_validate(
        self,
        *,
        fail_under: float,
        extra_pytest_args: list[str] | None,
    ) -> tuple[int, Path | None]:
        self.wipe_local_artifacts()
        rc = self.run_pytest_cov(
            fail_under=fail_under, extra_pytest_args=extra_pytest_args
        )
        if rc != 0:
            xml = self.cwd / self.strategy.xml_name
            return rc, xml if xml.is_file() else None
        return self._validated_ok()

    def _validated_ok(self) -> tuple[int, Path | None]:
        try:
            return 0, self.load_and_validate()
        except (FileNotFoundError, PathCohesionError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2, None

    def execute(
        self,
        *,
        fail_under: float = DEFAULT_FLOOR,
        extra_pytest_args: list[str] | None = None,
        skip_pytest: bool = False,
    ) -> tuple[int, Path | None]:
        """Wipe → (optional) pytest → validate. Returns (exit_code, xml_path)."""
        self.strategy.emit_banner()
        if skip_pytest:
            _unlink_coverage_dbs(self.cwd)
            return self._validated_ok()
        return self._run_then_validate(
            fail_under=fail_under, extra_pytest_args=extra_pytest_args
        )


# Compat alias used by tests / callers during the rename window.
CleanMeasureFactory = MeasureRun


def run_clean_measure(
    *,
    cwd: Path | None = None,
    fail_under: float = DEFAULT_FLOOR,
    extra_pytest_args: list[str] | None = None,
    skip_pytest: bool = False,
    strategy: MeasureStrategy | None = None,
) -> tuple[int, Path | None]:
    """Compat wrapper around :meth:`MeasureRun.execute`."""
    return MeasureRun(cwd, strategy=strategy).execute(
        fail_under=fail_under,
        extra_pytest_args=extra_pytest_args,
        skip_pytest=skip_pytest,
    )


def main(argv: list[str] | None = None) -> int:
    """Facade kept for ``python -m doc_engine.ci.coverage_measure``."""
    from doc_engine.ci.coverage_measure_cli import main as cli_main

    return cli_main(argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
