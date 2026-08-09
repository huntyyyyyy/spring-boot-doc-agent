"""Citation pool loading and evidence-tag helpers for mock stages."""

from __future__ import annotations

import os
import re

from doc_engine.pipeline.mock_stage_constants import EM


def _file_line_count(repo_path, relpath, cache):
    """Return cached line count for *relpath*, or 0 when unreadable."""
    if relpath in cache:
        return cache[relpath]
    abspath = os.path.join(repo_path, relpath)
    if not os.path.isfile(abspath):
        cache[relpath] = 0
        return 0
    try:
        with open(abspath, encoding="utf-8", errors="replace") as handle:
            cache[relpath] = sum(1 for _ in handle)
    except OSError:
        cache[relpath] = 0
    return cache[relpath]


def _citation_resolves(repo_path, relpath, line, cache):
    """True when *relpath* exists and *line* is in range (or line is None)."""
    count = _file_line_count(repo_path, relpath, cache)
    if count <= 0:
        return False
    if line is None:
        return True
    return 1 <= line <= count


def _normalize_match_text(raw_match, bucket):
    """Collapse whitespace and strip backticks so phrasing templates stay valid."""
    match = (raw_match or "").strip().replace("\n", " ")
    match = re.sub(r"\s+", " ", match)[:60] or bucket
    return match.replace("`", "'")


def _try_keep_citation_row(row, repo_path, bucket, line_counts):
    """Return (relpath, line, match) when the row cites a resolvable location."""
    relpath = row.get("file")
    line = row.get("line")
    if not relpath or not isinstance(line, int) or line < 1:
        return None
    if not _citation_resolves(repo_path, relpath, line, line_counts):
        return None
    return (relpath, line, _normalize_match_text(row.get("match"), bucket))


def _kept_citations_for_bucket(rows, repo_path, bucket, line_counts):
    """Filter one evidence bucket to resolvable citations."""
    kept = []
    for row in rows:
        citation = _try_keep_citation_row(row, repo_path, bucket, line_counts)
        if citation is not None:
            kept.append(citation)
    return kept


def load_citations(signals, repo_path):
    """Build a bucket -> [(file, line, match)] pool of citations that actually
    resolve.

    Every candidate is checked against the file on disk the same way
    doc_tag_utils.resolve_evidenced_citations() will check it later, so the
    mock docs cannot emit a citation the gate would reject. A scan is normally
    self-consistent with the repo it just scanned; this filter matters when the
    repo changed under the run, and it's cheap.
    """
    line_counts = {}
    pool = {}
    for bucket, rows in (signals.get("evidence") or {}).items():
        pool[bucket] = _kept_citations_for_bucket(
            rows, repo_path, bucket, line_counts
        )
    return pool


def _take_one_round(buckets, queues, round_index, selected, limit):
    """Append one round-robin slice; return True if anything was added."""
    added_any = False
    for bucket, queue in zip(buckets, queues, strict=True):
        if round_index >= len(queue):
            continue
        selected.append((bucket, queue[round_index]))
        added_any = True
        if len(selected) >= limit:
            return True
    return added_any


def pick(pool, buckets, limit):
    """Take up to `limit` citations spread across `buckets`, round-robin, so a
    doc fed by three buckets doesn't get `limit` rows of the first one."""
    queues = [list(pool.get(bucket) or []) for bucket in buckets]
    selected = []
    round_index = 0
    while len(selected) < limit:
        added = _take_one_round(buckets, queues, round_index, selected, limit)
        if not added:
            break
        round_index += 1
    return selected


def evidenced(relpath, line):
    """A well-formed [Evidenced — path:line] tag.

    Paths go out with forward slashes: the tag is read back by
    resolve_evidenced_citations(), which os.path.join()s it onto the repo root,
    and a Windows backslash in a document is both wrong-looking and needlessly
    platform-specific.
    """
    return f"[Evidenced {EM} {relpath.replace(os.sep, '/')}:{line}]"


def unknown_tag():
    return f"[Unknown {EM} not evidenced in code, not covered in interview]"


def confirmed_tag(date):
    return f"[Confirmed {EM} interview, {date}]"


def per_existing_docs_tag(filename):
    return f"[Per existing docs {EM} {filename}, unverified against code]"

