#!/usr/bin/env python3
"""Install repo pre-push hooks so local quality runs on every push.

Usage:
    python3 scripts/ci/install_git_hooks.py
    python3 scripts/ci/install_git_hooks.py --check

Sets ``core.hooksPath`` to ``.githooks`` when safe. When another tool (e.g.
Cursor agent-hooks) already owns hooksPath, installs a chaining ``pre-push``
into that directory that execs ``.githooks/pre-push`` — force-push included.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CHAIN_MARKER = "# doc-engine-pre-push-chain"
CHAIN_BODY = """#!/usr/bin/env bash
# doc-engine-pre-push-chain
# Chains Cursor/external hooksPath to the repo SoT pre-push (force-push too).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
exec "$ROOT/.githooks/pre-push" "$@"
"""


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def repo_root() -> Path:
    completed = _git("rev-parse", "--show-toplevel")
    if completed.returncode != 0:
        raise SystemExit(f"install_git_hooks: not a git repo: {completed.stderr}")
    return Path(completed.stdout.strip())


def current_hooks_path(root: Path) -> str:
    completed = _git("config", "--get", "core.hooksPath")
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _resolve_hooks_dir(root: Path, hooks_path: str) -> Path:
    path = Path(hooks_path)
    return path if path.is_absolute() else (root / path)


def install_chain(hooks_dir: Path) -> Path:
    hooks_dir.mkdir(parents=True, exist_ok=True)
    target = hooks_dir / "pre-push"
    target.write_text(CHAIN_BODY, encoding="utf-8")
    target.chmod(target.stat().st_mode | 0o111)
    return target


def hooks_healthy(root: Path) -> tuple[bool, str]:
    """Return (ok, detail) for --check."""
    sot = root / ".githooks" / "pre-push"
    if not sot.is_file():
        return False, "missing .githooks/pre-push"
    hooks_path = current_hooks_path(root)
    if not hooks_path:
        return False, "core.hooksPath unset (run install_git_hooks.py)"
    resolved = _resolve_hooks_dir(root, hooks_path)
    if resolved.resolve() == (root / ".githooks").resolve():
        return True, f"core.hooksPath={hooks_path}"
    chain = resolved / "pre-push"
    if chain.is_file() and CHAIN_MARKER in chain.read_text(encoding="utf-8"):
        return True, f"chained pre-push in {resolved}"
    return False, f"external hooksPath={hooks_path} without doc-engine chain"


def install(root: Path) -> int:
    sot = root / ".githooks"
    if not (sot / "pre-push").is_file():
        print("error: missing .githooks/pre-push", file=sys.stderr)
        return 1
    hooks_path = current_hooks_path(root)
    sot_rel = ".githooks"
    if not hooks_path or Path(hooks_path).name == "githooks":
        completed = _git("config", "core.hooksPath", sot_rel)
        if completed.returncode != 0:
            print(completed.stderr, file=sys.stderr)
            return 1
        print(f"installed: core.hooksPath={sot_rel}")
        return 0
    resolved = _resolve_hooks_dir(root, hooks_path)
    if resolved.resolve() == sot.resolve():
        print(f"ok: core.hooksPath already {hooks_path}")
        return 0
    target = install_chain(resolved)
    print(f"chained: {target} -> .githooks/pre-push (kept hooksPath={hooks_path})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 0 when pre-push SoT is reachable; else 1",
    )
    args = parser.parse_args(argv)
    root = repo_root()
    if args.check:
        ok, detail = hooks_healthy(root)
        print(detail)
        return 0 if ok else 1
    return install(root)


if __name__ == "__main__":
    raise SystemExit(main())
