"""Hermetic ratchet: every ``tests/**/test_*.py`` declares one domain marker.

Usage:
    python -m doc_engine.ci.test_domain_markers_check
    python -m doc_engine.ci.test_domain_markers_check --require-classifier-match
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from doc_engine.ci.test_domain_catalog import known_markers
from doc_engine.ci.test_domain_classify import (
    classify_test_path,
    declared_domain_markers,
    iter_test_modules,
)
from doc_engine.ci.test_domain_inventory import (
    DocEngineDomainInventory,
    build_doc_engine_inventory,
)
from doc_engine.ci.test_path_shards import domain_path_matrix, orphan_parallel_modules
from doc_engine.paths import repo_root

USAGE = """\
Verify each test module declares exactly one catalog domain_* pytestmark.
Also enforce doc_engine meeting rate >= 98.7 (debt = domain_unclassified only).

  python -m doc_engine.ci.test_domain_markers_check
  python -m doc_engine.ci.test_domain_markers_check --require-classifier-match
"""


def evaluate_module(
    repo: Path,
    path: Path,
    *,
    require_classifier_match: bool,
) -> list[str]:
    """Return human-readable issues for one test module (empty = OK)."""
    text = path.read_text(encoding="utf-8")
    declared = declared_domain_markers(text)
    rel = path.relative_to(repo).as_posix()
    count_issue = _declared_count_issue(rel, declared)
    if count_issue is not None:
        return [count_issue]
    return _single_marker_issues(
        repo,
        path,
        rel,
        declared[0],
        require_classifier_match=require_classifier_match,
    )


def _declared_count_issue(rel: str, declared: list[str]) -> str | None:
    if len(declared) == 0:
        return f"{rel}: missing domain_* pytestmark"
    if len(declared) > 1:
        return (
            f"{rel}: multiple domain markers {declared!r} (want exactly one)"
        )
    return None


def _single_marker_issues(
    repo: Path,
    path: Path,
    rel: str,
    marker: str,
    *,
    require_classifier_match: bool,
) -> list[str]:
    if marker not in known_markers():
        return [f"{rel}: unknown marker {marker!r}"]
    if not require_classifier_match:
        return []
    return _classifier_mismatch_issues(repo, path, rel, marker)


def _classifier_mismatch_issues(
    repo: Path, path: Path, rel: str, marker: str
) -> list[str]:
    expected = classify_test_path(repo, path)
    if marker == expected:
        return []
    return [f"{rel}: declared {marker} but classifier expects {expected}"]


def run_check(
    repo: Path,
    *,
    require_classifier_match: bool = True,
) -> int:
    """Exit 0 when the suite satisfies the domain-marker ratchet."""
    modules = iter_test_modules(repo)
    if not modules:
        print("error: no tests/**/test_*.py found", file=sys.stderr)
        return 2
    inventory = build_doc_engine_inventory(repo)
    issues = _collect_check_issues(
        repo, modules, require_classifier_match=require_classifier_match
    )
    issues.extend(_inventory_floor_issues(inventory))
    if issues:
        _print_check_failures(issues)
        return 1
    _print_check_success(
        repo,
        modules,
        inventory,
        require_classifier_match=require_classifier_match,
    )
    return 0


def _collect_check_issues(
    repo: Path,
    modules: list[Path],
    *,
    require_classifier_match: bool,
) -> list[str]:
    issues: list[str] = []
    for path in modules:
        issues.extend(
            evaluate_module(
                repo, path, require_classifier_match=require_classifier_match
            )
        )
    issues.extend(_orphan_parallel_issues(repo))
    if not domain_path_matrix(repo):
        issues.append("domain_path_matrix produced zero parallel groups")
    return issues


def _orphan_parallel_issues(repo: Path) -> list[str]:
    return [
        f"{orphan}: parallel module outside discovered domain path matrix"
        for orphan in orphan_parallel_modules(repo)
    ]


def _inventory_floor_issues(inventory: DocEngineDomainInventory) -> list[str]:
    if inventory.meets_floor:
        return []
    return [
        "tests/doc_engine meeting rate "
        f"{inventory.meeting_pct:.3f}% < floor {inventory.floor:g}% "
        f"(debt={len(inventory.debt)} still domain_unclassified; "
        "meeting modules are excluded from debt inventory)"
    ]


def _print_check_failures(issues: list[str]) -> None:
    print(
        f"test domain marker check failed ({len(issues)} issue(s)):",
        file=sys.stderr,
    )
    for issue in issues[:50]:
        print(f"  - {issue}", file=sys.stderr)
    if len(issues) > 50:
        print(f"  … and {len(issues) - 50} more", file=sys.stderr)


def _print_check_success(
    repo: Path,
    modules: list[Path],
    inventory: DocEngineDomainInventory,
    *,
    require_classifier_match: bool,
) -> None:
    aligned = " (classifier-aligned)" if require_classifier_match else ""
    print(
        f"OK: {len(modules)} test modules each declare one domain_* marker{aligned}"
    )
    print(
        f"OK: tests/doc_engine meeting={len(inventory.meeting)}/"
        f"{inventory.total} ({inventory.meeting_pct:.3f}% >= {inventory.floor:g}%); "
        f"debt={len(inventory.debt)} (unclassified only)"
    )
    groups = domain_path_matrix(repo)
    print(
        f"OK: domain path matrix {len(groups)} parallel groups "
        f"({sum(len(group.paths) for group in groups)} collection dirs)"
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry for the domain-marker ratchet."""
    parser = argparse.ArgumentParser(
        description=USAGE.splitlines()[0],
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: doc_engine.paths.repo_root())",
    )
    parser.add_argument(
        "--require-classifier-match",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Also require pytestmark to match the ownership classifier",
    )
    args = parser.parse_args(argv)
    root = args.repo_root or repo_root()
    return run_check(
        root.resolve(),
        require_classifier_match=args.require_classifier_match,
    )


if __name__ == "__main__":
    raise SystemExit(main())
