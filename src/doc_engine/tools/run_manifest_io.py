"""Clocks, atomic JSON writes, and git identity helpers for run_manifest.

``os`` / ``subprocess`` are resolved via the ``run_manifest`` façade so climb
tests can monkeypatch the public module surface.
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
from datetime import datetime, timezone


def _now_ms(override=None):
    return int(override) if override is not None else int(time.time() * 1000)


def _iso8601(now_ms):
    return datetime.fromtimestamp(now_ms / 1000, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _write_json_atomic(path, data):
    from doc_engine.tools import run_manifest as rm

    directory = rm.os.path.dirname(rm.os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(
        prefix=rm.os.path.basename(path) + ".tmp-", dir=directory
    )
    try:
        with rm.os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        rm.os.replace(tmp_path, path)
    except BaseException:
        try:
            rm.os.remove(tmp_path)
        except OSError:
            pass
        raise


def _run_git(repo_path, args, label):
    from doc_engine.tools import run_manifest as rm

    try:
        result = rm.subprocess.run(
            ["git", "-C", repo_path] + args,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, rm.subprocess.TimeoutExpired) as e:
        print(
            f"warning: could not run 'git {label}' for '{repo_path}': {e}",
            file=sys.stderr,
        )
        return None
    if result.returncode != 0:
        print(
            f"warning: 'git {label}' failed for '{repo_path}': {result.stderr.strip()}",
            file=sys.stderr,
        )
        return None
    return result.stdout


def git_commit_hash(repo_path):
    """None (with a stderr warning) if repo_path isn't a git repo or ``git``
    isn't on PATH — not an abort, same graceful-degrade posture as
    spring_signal_scan's compute_file_signature for one unreadable file."""
    from doc_engine.tools import run_manifest as rm

    out = rm._run_git(repo_path, ["rev-parse", "HEAD"], "rev-parse HEAD")
    return out.strip() if out is not None else None


def git_is_dirty(repo_path):
    """True if ``git status --porcelain`` reports anything, False if clean,
    None (with a stderr warning) if it couldn't be determined."""
    from doc_engine.tools import run_manifest as rm

    out = rm._run_git(repo_path, ["status", "--porcelain"], "status --porcelain")
    return bool(out.strip()) if out is not None else None


def make_run_id(now_ms):
    """Uniqueness suffix only — not a git hash, not otherwise meaningful."""
    from doc_engine.tools import run_manifest as rm

    return f"{rm._iso8601(now_ms)}-{rm.os.urandom(4).hex()}"
