"""Local in-repo quality-gates suite helper for pre_pr (E-HOOK1).

Keeps compare-ref resolution and argv construction out of the oversized
``pre_pr`` orchestrator.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import List


def resolve_compare_ref(repo_root: Path) -> str:
    """Prefer PRE_PR_COMPARE_REF, else origin/main, else HEAD~1."""
    explicit = (os.environ.get("PRE_PR_COMPARE_REF") or "").strip()
    if explicit:
        return explicit
    for candidate in ("origin/main", "main", "origin/master", "master"):
        probe = subprocess.run(
            ["git", "rev-parse", "--verify", candidate],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            return candidate
    return "HEAD~1"


def quality_gates_argv(repo_root: Path, *, skip_coverage: bool = True) -> List[str]:
    """Build ``doc-engine quality-gates`` argv for the local push path."""
    argv = [
        "quality-gates",
        "--compare-ref",
        resolve_compare_ref(repo_root),
    ]
    if skip_coverage:
        argv.append("--skip-coverage")
    coverage = repo_root / "coverage.xml"
    if coverage.is_file() and not skip_coverage:
        argv.extend(["--coverage-xml", str(coverage)])
    return argv
