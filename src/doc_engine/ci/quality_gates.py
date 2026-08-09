"""Hard in-repo quality gates (coverage / duplication / complexity / size / cycles).

Usage:
    doc-engine quality-gates --compare-ref origin/main
    doc-engine quality-gates --compare-ref HEAD~1 --coverage-xml coverage.xml
    python -m doc_engine.ci.quality_gates --compare-ref origin/main

Orchestration only: parse args, schedule gates cheapest→dearest, fail-fast,
summarize. Individual gate strategies live in ``quality_gate_checks``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from doc_engine.ci.gate_tools import REPO_ROOT
from doc_engine.ci.quality_gate_checks import (
    NEW_CODE_COVERAGE_FLOOR,
    PACKAGE_ROOTS,
    baseline_offender_ceiling,
    changed_python_under_packages,
    gate_cognitive_complexity,
    gate_complexity_ratchet,
    gate_duplication,
    gate_import_cycles,
    gate_new_code_coverage,
    gate_size_ratchet,
    report_gap_average,
    resolve_compare_ref,
)

# Re-export check surface for callers/tests that import from this module.
__all__ = (
    "NEW_CODE_COVERAGE_FLOOR",
    "PACKAGE_ROOTS",
    "baseline_offender_ceiling",
    "changed_python_under_packages",
    "gate_cognitive_complexity",
    "gate_complexity_ratchet",
    "gate_duplication",
    "gate_import_cycles",
    "gate_new_code_coverage",
    "gate_size_ratchet",
    "main",
    "resolve_compare_ref",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the quality-gate runner."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compare-ref",
        required=True,
        help="Git ref for new-code baseline (PR base SHA, origin/main, HEAD~1).",
    )
    parser.add_argument(
        "--coverage-xml",
        type=Path,
        default=REPO_ROOT / "coverage.xml",
        help="Cobertura XML from pytest-cov (default: ./coverage.xml).",
    )
    parser.add_argument(
        "--skip-coverage",
        action="store_true",
        help="Skip diff-cover (local debug only).",
    )
    parser.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Run every gate even after a failure (default: stop on first fail).",
    )
    return parser.parse_args(argv)


def _plan_gates(args: argparse.Namespace, compare_ref: str) -> list[tuple[str, object]]:
    """Cheapest → dearest; coverage optional for local debug."""
    planned: list[tuple[str, object]] = [
        ("import-cycles", gate_import_cycles),
        ("size-ratchet", gate_size_ratchet),
        ("duplication", lambda: gate_duplication(compare_ref)),
    ]
    if not args.skip_coverage:
        planned.append(
            (
                "new-code-coverage",
                lambda: gate_new_code_coverage(compare_ref, args.coverage_xml),
            )
        )
    planned.append(("cognitive-complexity", gate_cognitive_complexity))
    planned.append(("complexity-ratchet", gate_complexity_ratchet))
    return planned


def _run_planned(
    planned: list[tuple[str, object]], *, fail_fast: bool
) -> list[tuple[str, int]]:
    results: list[tuple[str, int]] = []
    for name, runner in planned:
        code = int(runner())  # type: ignore[operator]
        results.append((name, code))
        if code != 0 and fail_fast:
            print(
                f"\nfail-fast: stopping after {name} (exit {code}); "
                f"pass --no-fail-fast to run remaining gates.",
                flush=True,
            )
            break
    return results


def _gate_status_line(
    name: str, ran: set[str], results: list[tuple[str, int]]
) -> str:
    if name not in ran:
        return f"- {name}: SKIPPED (fail-fast)"
    code = next(c for n, c in results if n == name)
    status = "PASS" if code == 0 else f"FAIL (exit {code})"
    return f"- {name}: {status}"


def _print_summary(
    planned: list[tuple[str, object]], results: list[tuple[str, int]]
) -> None:
    print("\n=== quality-gates summary ===", flush=True)
    ran = {name for name, _ in results}
    for name, _ in planned:
        print(_gate_status_line(name, ran, results), flush=True)


def _exit_from_results(results: list[tuple[str, int]]) -> int:
    if any(code == 2 for _, code in results):
        return 2
    if any(code != 0 for _, code in results):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run hard gates cheapest→dearest; fail-fast unless --no-fail-fast."""
    args = parse_args(argv)
    compare_ref = resolve_compare_ref(args.compare_ref)
    planned = _plan_gates(args, compare_ref)
    results = _run_planned(planned, fail_fast=not args.no_fail_fast)
    _print_summary(planned, results)
    if not args.skip_coverage:
        report_gap_average(args.coverage_xml)
    return _exit_from_results(results)


if __name__ == "__main__":  # pragma: no cover - CLI entry glue
    raise SystemExit(main())
