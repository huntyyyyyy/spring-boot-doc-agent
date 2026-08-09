"""Quality-gate strategies: coverage, duplication, complexity, size, cycles.

Each ``gate_*`` function is one pluggable strategy (command construction +
exit mapping). ``quality_gates`` owns scheduling / fail-fast / summary only.
"""

from __future__ import annotations

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
        label="size ratchet (file LOC hard>225; fn stmts; must not rise)",
    )


def report_gap_average(coverage_xml: Path) -> None:
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
