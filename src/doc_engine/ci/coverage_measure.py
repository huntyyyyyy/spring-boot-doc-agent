"""MeasureRun — single-writer coverage measure for one checkout.

Wipes cwd-local ``.coverage*`` / ``coverage.xml``, runs one pytest+cov,
validates path cohesion, then optionally prints gap-average. Never combines
coverage DBs across worktrees.

Usage:
    doc-engine coverage-measure
    python -m doc_engine.ci.coverage_measure --floor 98.7

Exit codes: 0 ok; 1 pytest/fail_under failed; 2 cohesion/missing/bad args
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from doc_engine.ci.coverage_gap_average import DEFAULT_FLOOR, build_report_from_coverage
from doc_engine.ci.coverage_path_cohesion import PathCohesionError, PathCohesionGuard
from doc_engine.ci.coverage_report import load_cobertura_report
from doc_engine.ci.gate_tools import checkout_root


class MeasureRun:
    """Single-writer measure in *cwd* — wipe, one pytest+cov, cohesion check."""

    def __init__(self, cwd: Path | None = None) -> None:
        self.cwd = (cwd or Path.cwd()).resolve()

    def wipe_local_artifacts(self) -> list[Path]:
        """Delete cwd-local coverage artifacts only (not other worktrees)."""
        removed: list[Path] = []
        for path in sorted(self.cwd.glob(".coverage*")):
            if path.is_file():
                path.unlink()
                removed.append(path)
        xml = self.cwd / "coverage.xml"
        if xml.is_file():
            xml.unlink()
            removed.append(xml)
        return removed

    def run_pytest_cov(
        self,
        *,
        fail_under: float = DEFAULT_FLOOR,
        extra_pytest_args: list[str] | None = None,
    ) -> int:
        """One full pytest+cov run; writes ``coverage.xml`` beside *cwd*."""
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-q",
            "--tb=line",
            "--cov=doc_engine",
            "--cov=stf",
            "--cov-branch",
            "--cov-report=term-missing",
            "--cov-report=xml",
            f"--cov-fail-under={fail_under}",
        ]
        if extra_pytest_args:
            cmd.extend(extra_pytest_args)
        return int(subprocess.run(cmd, cwd=str(self.cwd), check=False).returncode)

    def load_and_validate(self) -> Path:
        """Require ``coverage.xml`` in cwd with cohesive source paths."""
        xml_path = self.cwd / "coverage.xml"
        if not xml_path.is_file():
            raise FileNotFoundError(f"missing coverage report: {xml_path}")
        report = load_cobertura_report(xml_path)
        PathCohesionGuard(self.cwd).assert_cohesive(report.source_paths())
        return xml_path

    def execute(
        self,
        *,
        fail_under: float = DEFAULT_FLOOR,
        extra_pytest_args: list[str] | None = None,
        skip_pytest: bool = False,
    ) -> tuple[int, Path | None]:
        """Wipe → (optional) pytest → validate. Returns (exit_code, xml_path)."""
        if skip_pytest:
            for path in sorted(self.cwd.glob(".coverage*")):
                if path.is_file():
                    path.unlink()
        else:
            self.wipe_local_artifacts()
            rc = self.run_pytest_cov(
                fail_under=fail_under, extra_pytest_args=extra_pytest_args
            )
            if rc != 0:
                xml = self.cwd / "coverage.xml"
                return rc, xml if xml.is_file() else None
        try:
            return 0, self.load_and_validate()
        except (FileNotFoundError, PathCohesionError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2, None


# Compat alias used by tests / callers during the rename window.
CleanMeasureFactory = MeasureRun


def run_clean_measure(
    *,
    cwd: Path | None = None,
    fail_under: float = DEFAULT_FLOOR,
    extra_pytest_args: list[str] | None = None,
    skip_pytest: bool = False,
) -> tuple[int, Path | None]:
    """Compat wrapper around :meth:`MeasureRun.execute`."""
    return MeasureRun(cwd).execute(
        fail_under=fail_under,
        extra_pytest_args=extra_pytest_args,
        skip_pytest=skip_pytest,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--floor", type=float, default=DEFAULT_FLOOR)
    p.add_argument("--worst", type=int, default=15)
    p.add_argument("--skip-pytest", action="store_true")
    p.add_argument("--no-gap-report", action="store_true")
    p.add_argument("pytest_args", nargs="*")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.floor < DEFAULT_FLOOR:
        print(
            f"error: refusing to weaken fail_under below {DEFAULT_FLOOR}",
            file=sys.stderr,
        )
        return 2
    root = checkout_root()
    if Path.cwd().resolve() != root.resolve():
        print(
            f"error: run coverage-measure from the checkout root ({root})",
            file=sys.stderr,
        )
        return 2
    rc, xml_path = MeasureRun(root).execute(
        fail_under=args.floor,
        extra_pytest_args=list(args.pytest_args) or None,
        skip_pytest=args.skip_pytest,
    )
    if xml_path is None:
        return rc
    if args.no_gap_report:
        print(f"coverage-measure wrote {xml_path}", flush=True)
        return rc
    try:
        report = build_report_from_coverage(
            load_cobertura_report(xml_path), floor=args.floor, repo_root=root
        )
    except PathCohesionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(report.as_text(worst=args.worst), flush=True)
    return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
