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
from doc_engine.ci.test_domain_inventory import build_doc_engine_inventory
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
    issues: list[str] = []
    if len(declared) == 0:
        issues.append(f"{rel}: missing domain_* pytestmark")
        return issues
    if len(declared) > 1:
        issues.append(
            f"{rel}: multiple domain markers {declared!r} (want exactly one)"
        )
        return issues
    marker = declared[0]
    if marker not in known_markers():
        issues.append(f"{rel}: unknown marker {marker!r}")
        return issues
    if require_classifier_match:
        expected = classify_test_path(repo, path)
        if marker != expected:
            issues.append(
                f"{rel}: declared {marker} but classifier expects {expected}"
            )
    return issues


def run_check(
    repo: Path,
    *,
    require_classifier_match: bool = True,
) -> int:
    """Exit 0 when the suite satisfies the domain-marker ratchet."""
    issues: list[str] = []
    modules = iter_test_modules(repo)
    if not modules:
        print("error: no tests/**/test_*.py found", file=sys.stderr)
        return 2
    for path in modules:
        issues.extend(
            evaluate_module(
                repo, path, require_classifier_match=require_classifier_match
            )
        )
    inventory = build_doc_engine_inventory(repo)
    if not inventory.meets_floor:
        issues.append(
            "tests/doc_engine meeting rate "
            f"{inventory.meeting_pct:.3f}% < floor {inventory.floor:g}% "
            f"(debt={len(inventory.debt)} still domain_unclassified; "
            "meeting modules are excluded from debt inventory)"
        )
    if issues:
        print(
            f"test domain marker check failed ({len(issues)} issue(s)):",
            file=sys.stderr,
        )
        for issue in issues[:50]:
            print(f"  - {issue}", file=sys.stderr)
        if len(issues) > 50:
            print(f"  … and {len(issues) - 50} more", file=sys.stderr)
        return 1
    print(
        f"OK: {len(modules)} test modules each declare one domain_* marker"
        + (" (classifier-aligned)" if require_classifier_match else "")
    )
    print(
        f"OK: tests/doc_engine meeting={len(inventory.meeting)}/"
        f"{inventory.total} ({inventory.meeting_pct:.3f}% >= {inventory.floor:g}%); "
        f"debt={len(inventory.debt)} (unclassified only)"
    )
    return 0


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
