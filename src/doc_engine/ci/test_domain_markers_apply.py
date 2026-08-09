"""Apply classifier-owned ``pytestmark`` lines to test modules (E-TEST1-2).

Usage:
    python -m doc_engine.ci.test_domain_markers_apply --dry-run
    python -m doc_engine.ci.test_domain_markers_apply
"""

from __future__ import annotations

import argparse
from pathlib import Path

from doc_engine.ci.test_domain_classify import (
    classify_test_path,
    ensure_pytestmark,
    iter_test_modules,
)
from doc_engine.paths import repo_root

USAGE = """\
Write domain_* pytestmark from the ownership classifier onto each test module.

  python -m doc_engine.ci.test_domain_markers_apply --dry-run
  python -m doc_engine.ci.test_domain_markers_apply
"""


def apply_markers(repo: Path, *, dry_run: bool) -> tuple[int, int]:
    """Return ``(changed, total)`` after aligning markers to the classifier."""
    changed = 0
    modules = iter_test_modules(repo)
    for path in modules:
        marker = classify_test_path(repo, path)
        original = path.read_text(encoding="utf-8")
        updated = ensure_pytestmark(original, marker)
        if updated == original:
            continue
        changed += 1
        rel = path.relative_to(repo).as_posix()
        print(f"{'dry-run' if dry_run else 'write'} {rel} -> {marker}")
        if not dry_run:
            path.write_text(updated, encoding="utf-8", newline="\n")
    return changed, len(modules)


def main(argv: list[str] | None = None) -> int:
    """CLI entry to bulk-label test modules."""
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
        "--dry-run",
        action="store_true",
        help="Print planned writes without modifying files",
    )
    args = parser.parse_args(argv)
    root = (args.repo_root or repo_root()).resolve()
    changed, total = apply_markers(root, dry_run=args.dry_run)
    print(f"{'would change' if args.dry_run else 'changed'} {changed}/{total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
