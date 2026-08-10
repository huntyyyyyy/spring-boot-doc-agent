#!/usr/bin/env python3
"""Pack session-log history into ≤TARGET line shards with dated content slugs.

Run: ``python3 scripts/process/pack_session_log.py``
(``--from-git HEAD:docs/process/session-log.md``, ``--index-only``, ``--dry-run``).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
NEST = REPO_ROOT / "docs" / "process" / "session-log"
STUB = REPO_ROOT / "docs" / "process" / "session-log.md"
ORDER = NEST / ".pack-order"
README_TEMPLATE = Path(__file__).with_name("session_log_readme.template.md")
TARGET_MAX_LINES = 225
SLUG_MAX = 48
ENTRY_HEAD = re.compile(r"^## (\d{4}-\d{2}-\d{2})\b", re.M)
TITLE_LINE = re.compile(
    r"^## (?P<date>\d{4}-\d{2}-\d{2})\s*(?:—|–|-|\?)\s*(?P<title>.+?)\s*$"
)


@dataclass(frozen=True)
class Entry:
    date: str
    text: str

    @property
    def lines(self) -> int:
        return self.text.count("\n") + (0 if self.text.endswith("\n") else 1)

    @property
    def title(self) -> str:
        first = self.text.splitlines()[0] if self.text else ""
        match = TITLE_LINE.match(first)
        if match:
            return match.group("title").strip()
        return first.removeprefix("## ").strip()


def slugify(title: str, *, max_len: int = SLUG_MAX) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        return "entry"
    if len(slug) <= max_len:
        return slug
    cut = slug[:max_len]
    if "-" in cut:
        cut = cut.rsplit("-", 1)[0]
    return cut or slug[:max_len]


def parse_entries(text: str) -> list[Entry]:
    first = text.find("## ")
    if first < 0:
        return []
    parts = re.split(r"(?=^## \d{4}-\d{2}-\d{2}\b)", text[first:], flags=re.M)
    out: list[Entry] = []
    for part in parts:
        if not part.strip():
            continue
        match = ENTRY_HEAD.match(part)
        if not match:
            continue
        body = part if part.endswith("\n") else f"{part}\n"
        out.append(Entry(date=match.group(1), text=body))
    return out


def shard_header(shard: list[Entry], target: int = TARGET_MAX_LINES) -> str:
    start, end = shard[0].date, shard[-1].date
    span = start if start == end else f"{start} → {end}"
    return (
        f"# Session log — {span}\n\n"
        f"Lead: **{shard[0].title}**\n\n"
        f"Packed shard (target ≤{target} lines). "
        f"Index: [`README.md`](README.md).\n\n"
        f"Entries: {len(shard)}. Newest at the bottom of this file.\n\n"
        f"---\n\n"
    )


def header_line_count(shard: list[Entry], target: int = TARGET_MAX_LINES) -> int:
    text = shard_header(shard, target=target)
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _shard_lines(shard: list[Entry], target: int) -> int:
    return header_line_count(shard, target=target) + sum(item.lines for item in shard)


def pack_entries(entries: list[Entry], *, target: int = TARGET_MAX_LINES) -> list[list[Entry]]:
    shards: list[list[Entry]] = []
    current: list[Entry] = []
    for entry in entries:
        trial = current + [entry]
        if current and _shard_lines(trial, target) > target:
            shards.append(current)
            current = [entry]
        else:
            current = trial
        if len(current) == 1 and _shard_lines(current, target) > target:
            shards.append(current)
            current = []
    if current:
        shards.append(current)
    return shards


def shard_sort_key(shard: list[Entry]) -> str:
    """Date-first span + first-entry content slug (filesystem / index key)."""
    start, end = shard[0].date, shard[-1].date
    span = start if start == end else f"{start}__{end}"
    return f"{span}__{slugify(shard[0].title)}"


def shard_filename(shard: list[Entry], used: set[str]) -> str:
    base = shard_sort_key(shard)
    name, suffix = f"{base}.md", 2
    while name in used:
        name = f"{base}-{suffix}.md"
        suffix += 1
    used.add(name)
    return name


def main(argv: list[str] | None = None) -> int:
    if __package__ is None or __package__ == "":
        sys.path.insert(0, str(REPO_ROOT))
    from scripts.process.pack_session_log_io import pack_tree, refresh_index

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-git", default=None)
    parser.add_argument("--target", type=int, default=TARGET_MAX_LINES)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Rebuild README/stub from existing shards (.pack-order); do not re-split",
    )
    args = parser.parse_args(argv)
    if args.index_only:
        return refresh_index(target=args.target)
    return pack_tree(from_git=args.from_git, target=args.target, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
