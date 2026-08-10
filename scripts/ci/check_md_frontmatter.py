#!/usr/bin/env python3
"""E-MD0 closed frontmatter gate — walk corpus C kinds and fail on hard findings.

Usage:
  python3 scripts/ci/check_md_frontmatter.py
  python3 scripts/ci/check_md_frontmatter.py --fix
  python3 scripts/ci/check_md_frontmatter.py --write-index
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

_SCRIPTS_CI = Path(__file__).resolve().parent
if str(_SCRIPTS_CI) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_CI))

from md_frontmatter_validate import Finding, validate_doc  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
INDEX_REL = Path("docs/research/_frontmatter_index.yaml")


def iter_markdown(repo: Path) -> List[Path]:
    skip_dirs = {".git", ".venv", "node_modules", "__pycache__", ".tox"}
    out: List[Path] = []
    for path in sorted(repo.rglob("*.md")):
        if any(part in skip_dirs for part in path.parts):
            continue
        out.append(path)
    return out


def collect(
    repo: Path, *, fix: bool
) -> Tuple[List[Finding], List[Finding], List[Dict[str, Any]]]:
    hard: List[Finding] = []
    soft: List[Finding] = []
    index_rows: List[Dict[str, Any]] = []
    for path in iter_markdown(repo):
        result = validate_doc(repo, path, fix=fix)
        if result.skipped:
            continue
        if fix and result.fixed_text is not None and result.fixed_text != path.read_text(
            encoding="utf-8"
        ):
            path.write_text(result.fixed_text, encoding="utf-8")
            result = validate_doc(repo, path, fix=False)
        for finding in result.findings:
            (hard if finding.level == "hard" else soft).append(finding)
        if result.kind in {"research_memo", "design_epic"} and result.data:
            rel = path.relative_to(repo).as_posix()
            related = result.data.get("related") or []
            index_rows.append(
                {
                    "path": rel,
                    "title": result.data.get("title"),
                    "status": result.data.get("status"),
                    "date": str(result.data.get("date")),
                    "epic": result.data.get("epic"),
                    "related_count": len(related) if isinstance(related, list) else 0,
                }
            )
    return hard, soft, index_rows


def write_index(repo: Path, rows: List[Dict[str, Any]]) -> None:
    payload = {"schema_version": 1, "entries": rows}
    target = repo / INDEX_REL
    target.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="rewrite deprecated keys")
    parser.add_argument("--write-index", action="store_true")
    parser.add_argument("--root", type=Path, default=REPO)
    args = parser.parse_args(argv)
    hard, soft, rows = collect(args.root, fix=args.fix)
    if args.write_index or args.fix:
        write_index(args.root, rows)
    for finding in soft:
        print(f"soft: {finding.path}: {finding.message}", file=sys.stderr)
    for finding in hard:
        print(f"hard: {finding.path}: {finding.message}", file=sys.stderr)
    if hard:
        print(f"FAIL: {len(hard)} hard frontmatter finding(s)", file=sys.stderr)
        return 1
    print(f"OK: markdown frontmatter ({len(rows)} indexed epic memos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
