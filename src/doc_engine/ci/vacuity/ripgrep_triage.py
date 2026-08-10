"""ripgrep triage — inventory candidates; never sole fail-closed SoT.

2026 practice (lgtm/ai-skills, vacuous, falsegreen): bare text search false-hits
docstrings/comments. rg is used only to *learn* candidate lines that structural
engines (ast-grep / vacuous) confirm or refute.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

# Patterns are deliberately simple — confirmation is structural.
_TRIAGE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("rg_triage__assert_true", r"^\s*assert\s+True\b"),
    ("rg_triage__assert_true_msg", r"^\s*assert\s+True\s*,"),
    ("rg_triage__pass_only_line", r"^\s*pass\s*$"),
)


@dataclass(frozen=True)
class RgTriageHit:
    """One ripgrep candidate line (not a merge proof by itself)."""

    kind: str
    path: str
    line: int
    text: str


def run_rg_triage(
    repo: Path,
    roots: Sequence[str],
    *,
    rg_bin: str = "rg",
) -> list[RgTriageHit]:
    """Collect candidate lines under test roots; empty if rg missing."""
    if shutil.which(rg_bin) is None:
        return []
    hits: list[RgTriageHit] = []
    for root in roots:
        target = repo / root
        if target.is_dir():
            hits.extend(_triage_root(target, rg_bin=rg_bin))
    return hits


def _triage_root(target: Path, *, rg_bin: str) -> list[RgTriageHit]:
    hits: list[RgTriageHit] = []
    for kind, pattern in _TRIAGE_PATTERNS:
        hits.extend(_triage_pattern(target, kind, pattern, rg_bin=rg_bin))
    return hits


def _triage_pattern(
    target: Path,
    kind: str,
    pattern: str,
    *,
    rg_bin: str,
) -> list[RgTriageHit]:
    completed = subprocess.run(
        [
            rg_bin,
            "--line-number",
            "--no-heading",
            "--glob",
            "test_*.py",
            "--glob",
            "*_test.py",
            "-e",
            pattern,
            str(target),
        ],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        return []
    out: list[RgTriageHit] = []
    for raw in (completed.stdout or "").splitlines():
        parsed = _parse_rg_line(raw, kind)
        if parsed is not None:
            out.append(parsed)
    return out


def _parse_rg_line(raw: str, kind: str) -> RgTriageHit | None:
    # path:line:text
    parts = raw.split(":", 2)
    if len(parts) < 3:
        return None
    path, line_s, text = parts[0], parts[1], parts[2]
    try:
        line = int(line_s)
    except ValueError:
        return None
    return RgTriageHit(kind=kind, path=path, line=line, text=text.strip()[:200])
