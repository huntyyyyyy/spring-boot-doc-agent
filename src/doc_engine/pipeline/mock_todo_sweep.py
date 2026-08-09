"""Stage-0 TODO/FIXME sweep used by mock known_limitations feeds."""

from __future__ import annotations

import os
import re

from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS

TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
TEXTUAL_SUFFIXES = {
    ".java", ".kt", ".xml", ".yml", ".yaml", ".properties", ".sql", ".gradle",
    ".md", ".json", ".sh", ".conf", ".txt", ".dockerfile",
}

def _is_textual_source(name):
    """True when *name* is a source/config extension we sweep for TODO markers."""
    suffix = os.path.splitext(name)[1].lower()
    return suffix in TEXTUAL_SUFFIXES or name.lower() == "dockerfile"


def _prune_walk_dirs(dirs):
    """Mutate os.walk dirs in place to skip excluded / hidden directories."""
    dirs[:] = [
        name for name in dirs
        if name not in DEFAULT_EXCLUDED_DIRS and not name.startswith(".")
    ]


def _scan_todo_lines(handle, relpath, remaining_cap):
    """Collect TODO/FIXME hits from an open text handle, up to *remaining_cap*."""
    hits = []
    for lineno, line in enumerate(handle, 1):
        match = TODO_RE.search(line)
        if match is None:
            continue
        hits.append({
            "file": relpath,
            "line": lineno,
            "marker": match.group(1),
            "text": line.strip()[:200],
        })
        if len(hits) >= remaining_cap:
            break
    return hits


def _todo_hits_in_file(abspath, relpath, remaining_cap):
    """Read one file and return TODO hits, or [] on I/O failure."""
    try:
        with open(abspath, encoding="utf-8", errors="replace") as handle:
            return _scan_todo_lines(handle, relpath, remaining_cap)
    except OSError:
        return []


def _extend_hits_from_name(repo_path, root, name, hits, cap):
    """Append TODO hits from one walk entry when it is a textual source file."""
    if not _is_textual_source(name):
        return hits
    abspath = os.path.join(root, name)
    relpath = os.path.relpath(abspath, repo_path).replace(os.sep, "/")
    remaining = cap - len(hits)
    return hits + _todo_hits_in_file(abspath, relpath, remaining)


def _extend_hits_from_dir(repo_path, root, files, hits, cap):
    """Append TODO hits from every textual file under one walk directory."""
    for name in files:
        hits = _extend_hits_from_name(repo_path, root, name, hits, cap)
        if len(hits) >= cap:
            return hits
    return hits


def _collect_todo_hits_under(repo_path, cap):
    """Walk *repo_path* and gather up to *cap* TODO/FIXME hits."""
    hits = []
    for root, dirs, files in os.walk(repo_path):
        _prune_walk_dirs(dirs)
        hits = _extend_hits_from_dir(repo_path, root, files, hits, cap)
        if len(hits) >= cap:
            return hits
    return hits


def sweep_todos(repo_path, cap=200):
    """SKILL.md Stage 0: 'grep for TODO|FIXME|XXX|HACK yourself (not worth a
    dedicated script) and keep the hits — they feed known_limitations.md as
    candidates, not facts.' Done in-process, honoring the same excluded-dir set
    the scan and partition stages share."""
    return _collect_todo_hits_under(repo_path, cap)

