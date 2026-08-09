"""Single-writer coverage measure for one checkout (Factory + Facade).

Wipes local ``.coverage*`` / ``coverage.xml`` in the active tree only, runs one
pytest+cov invocation, validates path cohesion, then optionally prints
gap-average. Never combines coverage DBs across worktrees.

Usage:
    doc-engine coverage-measure
    python -m doc_engine.ci.coverage_measure --floor 98.7

Exit codes:
    0  measure + optional gap report succeeded
    1  pytest / fail_under failed
    2  cohesion / missing report / bad args
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from doc_engine.ci.coverage_gap_average import DEFAULT_FLOOR, build_report_from_coverage
from doc_engine.ci.coverage_gap_format import format_text
from doc_engine.ci.coverage_path_cohesion import PathCohesionError, assert_paths_cohesive
from doc_engine.ci.coverage_report import load_cobertura_report
from doc_engine.ci.gate_tools import checkout_root


class CleanMeasureFactory:
    """Start a clean measure in *cwd* — single writer, no silent combine."""

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
        completed = subprocess.run(cmd, cwd=str(self.cwd), check=False)
        return int(completed.returncode)

    def load_and_validate(self) -> Path:
        """Require ``coverage.xml`` in cwd and cohesive source paths."""
        xml_path = self.cwd / "coverage.xml"
        if not xml_path.is_file():
            raise FileNotFoundError(f"missing coverage report: {xml_path}")
        report = load_cobertura_report(xml_path)
        assert_paths_cohesive(report.source_paths(), self.cwd)
        return xml_path


def run_clean_measure(
    *,
    cwd: Path | None = None,
    fail_under: float = DEFAULT_FLOOR,
    extra_pytest_args: list[str] | None = None,
    skip_pytest: bool = False,
) -> tuple[int, Path | None]:
    """Wipe → (optional) pytest → validate. Returns (exit_code, xml_path)."""
    factory = CleanMeasureFactory(cwd)
    if skip_pytest:
        # Keep coverage.xml; only drop stale SQLite shards that confuse combine.
        for path in sorted(factory.cwd.glob(".coverage*")):
            if path.is_file():
                path.unlink()
    else:
        factory.wipe_local_artifacts()
        rc = factory.run_pytest_cov(
            fail_under=fail_under, extra_pytest_args=extra_pytest_args
        )
        if rc != 0:
            xml = factory.cwd / "coverage.xml"
            return rc, xml if xml.is_file() else None
    try:
        xml_path = factory.load_and_validate()
    except (FileNotFoundError, PathCohesionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2, None
    return 0, xml_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--floor",
        type=float,
        default=DEFAULT_FLOOR,
        help=f"fail_under + gap floor (default: {DEFAULT_FLOOR}; do not weaken)",
    )
    parser.add_argument(
        "--worst",
        type=int,
        default=15,
        help="Worst below-floor files to list after measure",
    )
    parser.add_argument(
        "--skip-pytest",
        action="store_true",
        help="Wipe + validate existing coverage.xml only (debug)",
    )
    parser.add_argument(
        "--no-gap-report",
        action="store_true",
        help="Skip gap-average print after a successful measure",
    )
    parser.add_argument(
        "pytest_args",
        nargs="*",
        help="Extra args forwarded to pytest after the standard cov flags",
    )
    return parser.parse_args(argv)


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
    rc, xml_path = run_clean_measure(
        cwd=root,
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
        loaded = load_cobertura_report(xml_path)
        report = build_report_from_coverage(
            loaded, floor=args.floor, repo_root=root
        )
    except PathCohesionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(format_text(report, worst=args.worst), flush=True)
    return rc


if __name__ == "__main__":  # pragma: no cover - CLI entry glue
    raise SystemExit(main())
