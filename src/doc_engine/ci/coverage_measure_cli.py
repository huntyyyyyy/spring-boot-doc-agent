"""CLI for ``coverage-measure`` (oracle SoT vs climb sensor)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR
from doc_engine.ci.coverage_gap_average import build_report_from_coverage
from doc_engine.ci.coverage_measure import MeasureRun
from doc_engine.ci.coverage_measure_modes import (
    MeasureMode,
    MeasureStrategy,
    strategy_for,
)
from doc_engine.ci.coverage_path_cohesion import PathCohesionError
from doc_engine.ci.coverage_report import load_cobertura_report
from doc_engine.ci.gate_tools import checkout_root


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Single-writer coverage measure: oracle → coverage.xml; "
            "climb → coverage.climb.xml (policy 16-A)."
        )
    )
    p.add_argument(
        "--mode",
        choices=[m.value for m in MeasureMode],
        default=MeasureMode.ORACLE.value,
        help="oracle=whole-repo SoT (default); climb=scoped sensor (not CI floor)",
    )
    p.add_argument(
        "--scope",
        default=None,
        help="Package/module for climb --cov=<scope> (required when --mode climb)",
    )
    p.add_argument("--floor", type=float, default=DEFAULT_FLOOR)
    p.add_argument("--worst", type=int, default=15)
    p.add_argument("--skip-pytest", action="store_true")
    p.add_argument("--no-gap-report", action="store_true")
    p.add_argument("pytest_args", nargs="*")
    return p.parse_args(argv)


def _build_strategy(args: argparse.Namespace) -> MeasureStrategy | None:
    try:
        return strategy_for(MeasureMode(args.mode), scope_package=args.scope)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return None


def _validate_cli_args(
    args: argparse.Namespace, strategy: MeasureStrategy
) -> int | None:
    """Return exit 2 on bad args; None when OK."""
    if strategy.allows_fail_under() and args.floor < DEFAULT_FLOOR:
        print(
            f"error: refusing to weaken fail_under below {DEFAULT_FLOOR}",
            file=sys.stderr,
        )
        return 2
    if not strategy.allows_fail_under() and args.floor != DEFAULT_FLOOR:
        print(
            "error: climb mode refuses --floor (no whole-repo fail_under)",
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
    return None


def _print_oracle_gap(xml_path: Path, args: argparse.Namespace, root: Path) -> int:
    try:
        report = build_report_from_coverage(
            load_cobertura_report(xml_path), floor=args.floor, repo_root=root
        )
    except PathCohesionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(report.as_text(worst=args.worst), flush=True)
    return 0


def _finish_report(
    *,
    rc: int,
    xml_path: Path | None,
    args: argparse.Namespace,
    strategy: MeasureStrategy,
    root: Path,
) -> int:
    if xml_path is None:
        return rc
    if args.no_gap_report or not strategy.allows_gap_report():
        print(f"coverage-measure wrote {xml_path}", flush=True)
        return rc
    gap_rc = _print_oracle_gap(xml_path, args, root)
    return rc if gap_rc == 0 else gap_rc


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    strategy = _build_strategy(args)
    if strategy is None:
        return 2
    bad = _validate_cli_args(args, strategy)
    if bad is not None:
        return bad
    root = checkout_root()
    rc, xml_path = MeasureRun(root, strategy=strategy).execute(
        fail_under=args.floor,
        extra_pytest_args=list(args.pytest_args) or None,
        skip_pytest=args.skip_pytest,
    )
    return _finish_report(
        rc=rc, xml_path=xml_path, args=args, strategy=strategy, root=root
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
