"""Workflow file size and heredoc SoT (E-CI policy C4 / C3).

Boolean predicates for ``scripts/ci/check_workflow_yaml.py``:

* advisory when any workflow exceeds ``ADVISORY_LOC`` (225)
* hard fail when ``ci.yml`` exceeds ``CI_CALLER_MAX_LOC`` (200)
* hard fail when any workflow exceeds ``WORKFLOW_HARD_LOC`` (300)
* hard fail on inline ``python <<'PY'`` (or ``<<PY``) heredocs (C3)
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

ADVISORY_LOC = 225
CI_CALLER_MAX_LOC = 200
WORKFLOW_HARD_LOC = 300

_HEREDOC_MARKERS = ("<<'PY'", '<<"PY"', "<<PY")


def workflow_paths(workflows_dir: Path) -> List[Path]:
    return sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def check_workflow_loc(
    workflows_dir: Path,
    *,
    label_fn,
) -> Tuple[List[str], List[str]]:
    """Return (hard_errors, advisory_messages) for workflow LOC predicates."""
    hard: List[str] = []
    advisory: List[str] = []
    for path in workflow_paths(workflows_dir):
        loc = line_count(path)
        label = label_fn(path)
        if path.name == "ci.yml" and loc > CI_CALLER_MAX_LOC:
            hard.append(
                f"{label}: {loc} lines exceeds ci.yml caller max "
                f"{CI_CALLER_MAX_LOC} (policy C-A / C4)"
            )
        elif loc > WORKFLOW_HARD_LOC:
            hard.append(
                f"{label}: {loc} lines exceeds workflow hard max "
                f"{WORKFLOW_HARD_LOC} (policy C4)"
            )
        elif loc > ADVISORY_LOC:
            advisory.append(
                f"{label}: {loc} lines exceeds advisory {ADVISORY_LOC} "
                f"(policy C4; hard max {WORKFLOW_HARD_LOC})"
            )
    return hard, advisory


def check_no_python_heredocs(
    workflows_dir: Path,
    *,
    label_fn,
) -> List[str]:
    """Hard-fail strings for inline python heredocs (policy C3)."""
    errors: List[str] = []
    for path in workflow_paths(workflows_dir):
        text = path.read_text(encoding="utf-8")
        for marker in _HEREDOC_MARKERS:
            if marker in text:
                errors.append(
                    f"{label_fn(path)}: inline python heredoc {marker} "
                    f"forbidden (policy C3); use scripts/ci instead"
                )
                break
    return errors
