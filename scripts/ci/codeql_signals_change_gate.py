"""CodeQL signals change gate — content fingerprint skip (E-CQL1 / CQ1–CQ3).

Compares HEAD vs base over the CI harness input corpus. Equal → expensive
compile+runtime may skip; missing base / git error → fail-closed run.

Run::

    python3 scripts/ci/codeql_signals_change_gate.py
    python3 scripts/ci/codeql_signals_change_gate.py --base origin/main --write-env
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CORPUS_GLOBS: tuple[str, ...] = (
    "spring-signals/codeql/**",
    "spring-signals/harness/**",
    ".github/workflows/codeql-signals.yml",
    ".github/actions/setup-codeql/**",
    "scripts/ci/setup_codeql.sh",
)

EXCLUDE_NAME_PARTS: tuple[str, ...] = ("__pycache__", ".codeql", "/out/")

_DEFAULT_BUNDLE_URL = (
    "https://github.com/github/codeql-action/releases/download/"
    "codeql-bundle-v2.26.2/codeql-bundle-linux64.tar.gz"
)
_DEFAULT_BUNDLE_SHA = (
    "cb361567fa1bdb9d322da4240f621b36f245e4d7bb97db3c3a2ad7f743c8e8e7"
)


def _git_bytes(args: list[str], cwd: Path) -> bytes | None:
    completed = subprocess.run(args, cwd=cwd, check=False, capture_output=True)
    if completed.returncode != 0:
        return None
    return completed.stdout


def _ref_exists(candidate: str, cwd: Path) -> bool:
    return _git_bytes(["git", "rev-parse", "--verify", candidate], cwd) is not None


def resolve_base_ref(explicit: str | None, cwd: Path) -> str | None:
    """Return a usable base ref, or None (caller must fail-closed → run)."""
    ordered = [explicit, "origin/main", "main", "HEAD~1"]
    for candidate in ordered:
        if candidate and _ref_exists(candidate, cwd):
            return candidate
    return None


def _excluded(rel: str) -> bool:
    return any(part in rel for part in EXCLUDE_NAME_PARTS)


def _collect_glob(root: Path, pattern: str, hits: set[Path]) -> None:
    for path in root.glob(pattern):
        if path.is_file() and not _excluded(path.relative_to(root).as_posix()):
            hits.add(path)


def _iter_corpus_files(root: Path) -> list[Path]:
    hits: set[Path] = set()
    for pattern in CORPUS_GLOBS:
        _collect_glob(root, pattern, hits)
    return sorted(hits, key=lambda p: p.as_posix())


def _digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _accumulate_pin(hasher: hashlib._Hash, bundle_url: str, bundle_sha: str) -> None:
    hasher.update(f"url:{bundle_url}\n".encode())
    hasher.update(f"sha:{bundle_sha}\n".encode())


def fingerprint_tree(root: Path, *, bundle_url: str, bundle_sha: str) -> str:
    """Stable SHA-256 over corpus file digests + bundle pin."""
    hasher = hashlib.sha256()
    _accumulate_pin(hasher, bundle_url, bundle_sha)
    for path in _iter_corpus_files(root):
        rel = path.relative_to(root).as_posix()
        hasher.update(f"{rel}:{_digest_bytes(path.read_bytes())}\n".encode())
    return hasher.hexdigest()


def fingerprint_at_ref(
    root: Path,
    git_ref: str,
    *,
    bundle_url: str,
    bundle_sha: str,
) -> str | None:
    """Fingerprint corpus as of *git_ref*; None when any blob is missing."""
    hasher = hashlib.sha256()
    _accumulate_pin(hasher, bundle_url, bundle_sha)
    for path in _iter_corpus_files(root):
        rel = path.relative_to(root).as_posix()
        blob = _git_bytes(["git", "show", f"{git_ref}:{rel}"], root)
        if blob is None:
            return None
        hasher.update(f"{rel}:{_digest_bytes(blob)}\n".encode())
    return hasher.hexdigest()


def decide_run_expensive(
    root: Path,
    *,
    base_ref: str | None,
    bundle_url: str,
    bundle_sha: str,
) -> tuple[bool, str]:
    """Return (run_expensive, reason). Fail-closed → True when unsure."""
    if base_ref is None:
        return True, "missing_base_ref"
    head_fp = fingerprint_tree(root, bundle_url=bundle_url, bundle_sha=bundle_sha)
    base_fp = fingerprint_at_ref(
        root, base_ref, bundle_url=bundle_url, bundle_sha=bundle_sha
    )
    if base_fp is None:
        return True, "base_fingerprint_unavailable"
    if head_fp == base_fp:
        return False, "fingerprint_unchanged"
    return True, "fingerprint_changed"


def _parse_workflow_pin(text: str) -> tuple[str, str]:
    url, sha = _DEFAULT_BUNDLE_URL, _DEFAULT_BUNDLE_SHA
    for line in text.splitlines():
        if "CODEQL_BUNDLE_URL:" in line:
            url = line.split(":", 1)[1].strip()
        elif "CODEQL_SHA256:" in line:
            sha = line.split(":", 1)[1].strip()
    return url, sha


def _bundle_pin_from_workflow(root: Path) -> tuple[str, str]:
    workflow = root / ".github/workflows/codeql-signals.yml"
    if not workflow.is_file():
        return _DEFAULT_BUNDLE_URL, _DEFAULT_BUNDLE_SHA
    return _parse_workflow_pin(workflow.read_text(encoding="utf-8"))


def bundle_pin(root: Path) -> tuple[str, str]:
    url = os.environ.get("CODEQL_BUNDLE_URL", "").strip()
    sha = os.environ.get("CODEQL_SHA256", "").strip()
    if url and sha:
        return url, sha
    return _bundle_pin_from_workflow(root)


def _write_github_output(run_expensive: bool, reason: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    flag = "true" if run_expensive else "false"
    with open(out, "a", encoding="utf-8") as handle:
        handle.write(f"run_expensive={flag}\n")
        handle.write(f"reason={reason}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=None)
    parser.add_argument("--write-env", action="store_true")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    url, sha = bundle_pin(root)
    base = resolve_base_ref(args.base, root)
    run_expensive, reason = decide_run_expensive(
        root, base_ref=base, bundle_url=url, bundle_sha=sha
    )
    flag = "true" if run_expensive else "false"
    print(f"codeql_signals_change_gate: run_expensive={flag} reason={reason}")
    if args.write_env:
        _write_github_output(run_expensive, reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
