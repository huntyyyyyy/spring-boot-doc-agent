"""Filesystem helpers for session-log packing (kept separate for LOC/complexity)."""

from __future__ import annotations

from pathlib import Path

from scripts.process.pack_session_log import (
    NEST,
    ORDER,
    README_TEMPLATE,
    STUB,
    TARGET_MAX_LINES,
    pack_entries,
    parse_entries,
    shard_filename,
    shard_header,
)


def nest_shard_paths() -> list[Path]:
    """Prefer `.pack-order` so re-reads keep append chronology."""
    if not ORDER.is_file():
        return sorted(path for path in NEST.glob("*.md") if path.name != "README.md")
    names = [line.strip() for line in ORDER.read_text(encoding="utf-8").splitlines()]
    return [NEST / name for name in names if name and (NEST / name).is_file()]


def load_source_text(*, from_git: str | None) -> str:
    if from_git:
        import subprocess

        raw = subprocess.check_output(["git", "show", from_git], cwd=NEST.parents[2])
        return raw.decode("utf-8", errors="replace")
    if STUB.is_file() and STUB.read_text(encoding="utf-8").count("\n") > 100:
        return STUB.read_text(encoding="utf-8")
    chunks: list[str] = []
    for path in nest_shard_paths():
        text = path.read_text(encoding="utf-8")
        index = text.find("## ")
        if index >= 0:
            chunks.append(text[index:])
    return "".join(chunks)


def write_readme(
    manifest: list[tuple[str, str, int, int, str, str]],
    *,
    entry_count: int,
    target: int,
) -> None:
    rows = "\n".join(
        f"| [`{name}`]({name}) | {start} → {end} | {lead} | {entries} | {lines} |"
        for name, lead, entries, lines, start, end in manifest
    )
    max_lines = max((row[3] for row in manifest), default=0)
    over = sum(1 for row in manifest if row[3] > target)
    filled = (
        README_TEMPLATE.read_text(encoding="utf-8")
        .replace("{target}", str(target))
        .replace("{rows}", rows)
        .replace("{entry_count}", str(entry_count))
        .replace("{shard_count}", str(len(manifest)))
        .replace("{max_lines}", str(max_lines))
        .replace("{over}", str(over))
    )
    (NEST / "README.md").write_text(filled, encoding="utf-8")


def write_stub() -> None:
    STUB.write_text(
        "# Session log — steering prompt impact\n\n"
        "**Nested.** See [`session-log/README.md`](session-log/README.md) "
        "(LOC pack + `START__slug` names). Do not append to this stub.\n",
        encoding="utf-8",
    )


def manifest_from_nest() -> tuple[list[tuple[str, str, int, int, str, str]], int]:
    manifest: list[tuple[str, str, int, int, str, str]] = []
    entry_count = 0
    for path in nest_shard_paths():
        text = path.read_text(encoding="utf-8")
        entries = parse_entries(text)
        entry_count += len(entries)
        lead = entries[0].title if entries else path.stem
        start = entries[0].date if entries else "?"
        end = entries[-1].date if entries else "?"
        manifest.append((path.name, lead, len(entries), text.count("\n") + 1, start, end))
    return manifest, entry_count


def refresh_index(*, target: int = TARGET_MAX_LINES) -> int:
    manifest, entry_count = manifest_from_nest()
    write_readme(manifest, entry_count=entry_count, target=target)
    write_stub()
    for name, _lead, count, lines, _a, _b in manifest:
        print(f"{name}  n={count}  L={lines}")
    return 0


def pack_tree(*, from_git: str | None, target: int, dry_run: bool) -> int:
    entries = parse_entries(load_source_text(from_git=from_git))
    shards = pack_entries(entries, target=target)
    used: set[str] = set()
    manifest: list[tuple[str, str, int, int, str, str]] = []
    planned: list[tuple[str, str]] = []
    for shard in shards:
        name = shard_filename(shard, used)
        body = shard_header(shard, target=target) + "".join(item.text for item in shard)
        lines = body.count("\n") + 1
        manifest.append(
            (name, shard[0].title, len(shard), lines, shard[0].date, shard[-1].date)
        )
        planned.append((name, body))
        print(f"{name}  n={len(shard)}  L={lines}{' OVER' if lines > target else ''}")
    if dry_run:
        return 0
    NEST.mkdir(parents=True, exist_ok=True)
    for path in NEST.glob("*.md"):
        path.unlink()
    for name, body in planned:
        (NEST / name).write_text(body, encoding="utf-8")
    ORDER.write_text("\n".join(name for name, _body in planned) + "\n", encoding="utf-8")
    write_readme(manifest, entry_count=len(entries), target=target)
    write_stub()
    return 0
