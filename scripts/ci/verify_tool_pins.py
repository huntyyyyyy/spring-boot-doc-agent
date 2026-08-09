#!/usr/bin/env python3
"""Fail closed when PATH binaries diverge from requirements.txt pins.

Presence on PATH is not enough: a differently versioned system install can
shadow the venv pin (see docs/process/tool-quirks.md). Reads major.minor from the
requirements pin and from ``--version`` output; mismatches exit 1.

Usage:
    python3 scripts/ci/verify_tool_pins.py
    python3 scripts/ci/verify_tool_pins.py --requirements requirements.txt

Run with:
    python3 scripts/ci/verify_tool_pins.py
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Tuple

from doc_engine.paths import repo_root

# (requirements package name, PATH binary name)
_PINNED_TOOLS: Tuple[Tuple[str, str], ...] = (
    ("ast-grep-cli", "ast-grep"),
    ("semgrep", "semgrep"),
)

_PIN_RE_TMPL = r"^{pkg}~=(\d+)\.(\d+)\."
_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def _pin_major_minor(requirements: Path, package: str) -> Tuple[str, str]:
    text = requirements.read_text(encoding="utf-8")
    match = re.search(_PIN_RE_TMPL.format(pkg=re.escape(package)), text, re.M)
    if not match:
        raise SystemExit(f"{requirements} does not pin {package}")
    return match.group(1), match.group(2)


def _resolved_major_minor(binary: str) -> Tuple[str, str, str, str]:
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"{binary} is not on PATH")
    out = subprocess.run(
        [path, "--version"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    got = _VERSION_RE.search(out)
    if not got:
        raise SystemExit(f"could not parse a version from {out!r}")
    return got.group(1), got.group(2), out, path


def verify_one(requirements: Path, package: str, binary: str) -> None:
    want = _pin_major_minor(requirements, package)
    major, minor, out, path = _resolved_major_minor(binary)
    have = (major, minor)
    print(f"{binary}: pin={'.'.join(want)}.x  resolved={out}  at {path}")
    if want != have:
        raise SystemExit(
            f"{binary} on PATH is {out}, but {requirements.name} pins "
            f"{'.'.join(want)}.x. Two installs are shadowing each other; "
            f"run `which -a {binary}`."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--requirements",
        type=Path,
        default=repo_root() / "requirements.txt",
        help="requirements file carrying ~= pins (default: repo requirements.txt)",
    )
    args = parser.parse_args(argv)
    requirements = args.requirements
    if not requirements.is_file():
        print(f"error: missing {requirements}", file=sys.stderr)
        return 2
    for package, binary in _PINNED_TOOLS:
        verify_one(requirements, package, binary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
