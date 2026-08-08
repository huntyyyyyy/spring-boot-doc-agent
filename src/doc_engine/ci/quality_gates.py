"""Hard in-repo quality gates (coverage / duplication / complexity / size / cycles).

Usage:
    doc-engine quality-gates --compare-ref origin/main
    doc-engine quality-gates --compare-ref HEAD~1 --coverage-xml coverage.xml
    python -m doc_engine.ci.quality_gates --compare-ref origin/main

Same command on Mac, Windows, and Linux (CI uses this entry point too).
Requires: ``pip install -r requirements-dev.txt && pip install -e .`` and
``npm ci`` (pins jscpd; see CONTRIBUTING.md "Quality gates (all OS)").

Efficiency (aligned with SoR-vs-derived + fail-fast):
    Gates run cheapest → dearest and stop on the first failure. jscpd/diff-cover
    are merge-base scoped; whole-repo complexipy ``--failed`` is the complexity
    SoR. When the committed ratchet baseline is already 0, the second complexipy
    scan (offender-count ratchet) is skipped as a redundant derived check.
    Size ratchet (file LOC / function statements) is a cheap AST walk.

Exit codes:
    0  all hard gates passed
    1  one or more hard gates failed
    2  usage / missing prerequisite
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from doc_engine.ci.gate_tools import (
    JSCPD_VERSION,
    REPO_ROOT,
    jscpd_command,
    python_module_command,
    validate_git_rev,
)

PACKAGE_ROOTS = ("src/doc_engine", "src/stf")
NEW_CODE_COVERAGE_FLOOR = 98.7
COMPLEXITY_MAX = 5
DUPLICATION_MAX_PERCENT = 3
COMPLEXITY_BASELINE = REPO_ROOT / "scripts" / "ratchets" / "complexipy_baseline.json"


def _run(command: list[str], *, label: str) -> int:
    """Run *command* as an argv list (no shell); return the process exit code."""
    print(f"\n=== {label} ===", flush=True)
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    return int(completed.returncode)


def resolve_compare_ref(explicit: str | None) -> str:
    """Return the git ref used as the new-code baseline."""
    if explicit:
        return validate_git_rev(explicit)
    print("error: --compare-ref is required", file=sys.stderr)
    raise SystemExit(2)


def changed_python_under_packages(compare_ref: str) -> list[str]:
    """List ACMR Python paths under package roots vs *compare_ref*."""
    completed = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{compare_ref}...HEAD",
            "--",
            *PACKAGE_ROOTS,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        print(completed.stderr, file=sys.stderr)
        print("error: git diff for changed Python files failed", file=sys.stderr)
        raise SystemExit(2)
    paths = []
    for line in completed.stdout.splitlines():
        path = line.strip()
        if path.endswith(".py") and Path(REPO_ROOT, path).is_file():
            paths.append(path)
    return paths


def gate_new_code_coverage(compare_ref: str, coverage_xml: Path) -> int:
    """Fail when covered lines on the diff are below NEW_CODE_COVERAGE_FLOOR."""
    if not coverage_xml.is_file():
        print(f"error: missing coverage report: {coverage_xml}", file=sys.stderr)
        return 2
    coverage_xml = coverage_xml if coverage_xml.is_absolute() else REPO_ROOT / coverage_xml
    return _run(
        python_module_command(
            "diff_cover.diff_cover_tool",
            str(coverage_xml),
            f"--compare-branch={compare_ref}",
            f"--fail-under={NEW_CODE_COVERAGE_FLOOR}",
            "--include=src/doc_engine/*",
            "--include=src/stf/*",
        ),
        label=f"diff-cover new-code coverage >= {NEW_CODE_COVERAGE_FLOOR}%",
    )


def gate_duplication(compare_ref: str) -> int:
    """Fail when jscpd duplication among changed package files exceeds 3%."""
    changed = changed_python_under_packages(compare_ref)
    if not changed:
        print(
            "\n=== jscpd duplication <= 3% ===\n"
            "No changed Python under src/doc_engine or src/stf; skipping.",
            flush=True,
        )
        return 0
    if len(changed) == 1:
        print(
            "\n=== jscpd duplication <= 3% ===\n"
            f"Single changed file ({changed[0]}); intra-diff duplication N/A - pass.",
            flush=True,
        )
        return 0
    return _run(
        jscpd_command(
            f"--threshold={DUPLICATION_MAX_PERCENT}",
            "--min-lines=5",
            "--format=python",
            *changed,
        ),
        label=(
            f"jscpd@{JSCPD_VERSION} duplication <= {DUPLICATION_MAX_PERCENT}% "
            "(changed files; local node_modules)"
        ),
    )


def gate_cognitive_complexity() -> int:
    """Fail when any function in package roots exceeds COMPLEXITY_MAX."""
    from doc_engine.ci.gate_tools import require_on_path

    complexipy = require_on_path("complexipy")
    return _run(
        [
            complexipy,
            *PACKAGE_ROOTS,
            f"--max-complexity-allowed={COMPLEXITY_MAX}",
            "--failed",
        ],
        label=f"complexipy cognitive complexity <= {COMPLEXITY_MAX} (whole-repo)",
    )


def baseline_offender_ceiling(path: Path = COMPLEXITY_BASELINE) -> int | None:
    """Return committed ratchet ceiling, or None if missing/unreadable."""
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data["offender_count"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def gate_complexity_ratchet() -> int:
    """Fail when the count of >COMPLEXITY_MAX functions rises vs baseline.

    When the baseline ceiling is already 0, ``complexipy --failed`` is the SoR
    for the ≤5 property and a second whole-repo scan is redundant — skip it.
    """
    ceiling = baseline_offender_ceiling()
    if ceiling == 0:
        print(
            "\n=== complexipy offender-count ratchet ===\n"
            "baseline offender_count=0; whole-repo --failed is the SoR — "
            "skipping duplicate complexipy scan.",
            flush=True,
        )
        return 0
    return _run(
        python_module_command("doc_engine.ci.complexipy_ratchet"),
        label="complexipy offender-count ratchet (must not rise; target 0)",
    )


def gate_import_cycles() -> int:
    """Fail when tach finds circular imports among configured modules."""
    return _run(
        python_module_command("tach", "check"),
        label="tach forbid circular dependencies",
    )


def gate_size_ratchet() -> int:
    """Fail when file LOC / function statement hard offenders rise or grow."""
    return _run(
        python_module_command("doc_engine.ci.size_ratchet"),
        label="size ratchet (file LOC / function statements; must not rise)",
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


def _report_gap_average(coverage_xml: Path) -> None:
    """Advisory climb inventory (does not affect exit code)."""
    resolved = coverage_xml if coverage_xml.is_absolute() else REPO_ROOT / coverage_xml
    if not resolved.is_file():
        return
    _run(
        python_module_command(
            "doc_engine.ci.coverage_gap_average",
            "--coverage-xml",
            str(resolved),
            "--floor",
            str(NEW_CODE_COVERAGE_FLOOR),
            "--worst",
            "15",
        ),
        label=(
            f"coverage gap-average "
            f"(below-floor files only; floor={NEW_CODE_COVERAGE_FLOOR:g}%)"
        ),
    )


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
        _report_gap_average(args.coverage_xml)
    return _exit_from_results(results)


if __name__ == "__main__":  # pragma: no cover - CLI entry glue
    raise SystemExit(main())
