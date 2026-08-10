"""ast-grep scan helpers for OCS campaign floor remeasure (E-OCS0 OCS6)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

FLOOR_RULES = (
    "api_surface__controller",
    "api_surface__endpoint",
    "api_surface__path_prefix",
    "persistence__repository_marker",
)


def scan_roots(checkout: Path) -> list[Path]:
    mains = sorted({path.resolve() for path in checkout.glob("**/src/main/java")})
    if mains:
        return mains
    return [checkout.resolve()]


def resolve_astgrep() -> str:
    """Prefer PATH, then the binary next to this interpreter (venv Scripts)."""
    found = shutil.which("ast-grep")
    if found:
        return found
    sibling = Path(sys.executable).resolve().parent / (
        "ast-grep.exe" if os.name == "nt" else "ast-grep"
    )
    if sibling.is_file():
        return str(sibling)
    raise FileNotFoundError(
        "ast-grep not found on PATH or next to Python "
        f"({sys.executable}). Activate .venv or: pip install -r requirements.txt"
    )


def count_rule_ids(stdout: str) -> Counter[str]:
    text = (stdout or "").strip()
    if not text:
        return Counter()
    payload = json.loads(text)
    rows = payload if isinstance(payload, list) else [payload]
    return Counter(
        str(row["ruleId"])
        for row in rows
        if isinstance(row, dict) and row.get("ruleId")
    )


def run_astgrep(roots: Sequence[Path], rules: Path) -> Counter[str]:
    if not roots:
        return Counter()
    completed = subprocess.run(
        [
            resolve_astgrep(),
            "scan",
            "-r",
            str(rules),
            "--json=compact",
            *[str(path) for path in roots],
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            (completed.stderr or completed.stdout or "ast-grep failed")[:500]
        )
    return count_rule_ids(completed.stdout)
