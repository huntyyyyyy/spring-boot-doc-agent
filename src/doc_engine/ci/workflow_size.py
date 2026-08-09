"""Workflow file size and heredoc SoT (E-CI policy C4 / C3).

Boolean predicates for ``scripts/ci/check_workflow_yaml.py``:

* advisory when any workflow exceeds ``ADVISORY_LOC`` (225)
* hard fail when ``ci.yml`` exceeds ``CI_CALLER_MAX_LOC`` (200)
* hard fail when any workflow exceeds ``WORKFLOW_HARD_LOC`` (300)
* hard fail on inline ``python <<'PY'`` (or ``<<PY``) heredocs (C3)
* hard fail when a job that ``uses:`` a reusable workflow also sets
  ``continue-on-error`` (Actions rejects the caller workflow with 0 jobs)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - same pin as check_workflow_yaml
    yaml = None  # type: ignore[assignment]

ADVISORY_LOC = 225
CI_CALLER_MAX_LOC = 200
WORKFLOW_HARD_LOC = 300

_HEREDOC_MARKERS = ("<<'PY'", '<<"PY"', "<<PY")


def workflow_paths(workflows_dir: Path) -> List[Path]:
    return sorted(workflows_dir.glob("*.yml")) + sorted(workflows_dir.glob("*.yaml"))


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _ci_caller_hard_message(path: Path, loc: int, label: str) -> Optional[str]:
    if path.name != "ci.yml":
        return None
    if loc <= CI_CALLER_MAX_LOC:
        return None
    return (
        f"{label}: {loc} lines exceeds ci.yml caller max "
        f"{CI_CALLER_MAX_LOC} (policy C-A / C4)"
    )


def _workflow_hard_message(loc: int, label: str) -> Optional[str]:
    if loc <= WORKFLOW_HARD_LOC:
        return None
    return (
        f"{label}: {loc} lines exceeds workflow hard max "
        f"{WORKFLOW_HARD_LOC} (policy C4)"
    )


def _workflow_advisory_message(loc: int, label: str) -> Optional[str]:
    if loc <= ADVISORY_LOC:
        return None
    return (
        f"{label}: {loc} lines exceeds advisory {ADVISORY_LOC} "
        f"(policy C4; hard max {WORKFLOW_HARD_LOC})"
    )


def _loc_messages_for_path(
    path: Path, loc: int, label: str
) -> Tuple[Optional[str], Optional[str]]:
    hard = _ci_caller_hard_message(path, loc, label) or _workflow_hard_message(
        loc, label
    )
    if hard is not None:
        return hard, None
    return None, _workflow_advisory_message(loc, label)


def check_workflow_loc(
    workflows_dir: Path,
    *,
    label_fn,
) -> Tuple[List[str], List[str]]:
    """Return (hard_errors, advisory_messages) for workflow LOC predicates."""
    hard: List[str] = []
    advisory: List[str] = []
    for path in workflow_paths(workflows_dir):
        hard_msg, advisory_msg = _loc_messages_for_path(
            path, line_count(path), label_fn(path)
        )
        if hard_msg is not None:
            hard.append(hard_msg)
        if advisory_msg is not None:
            advisory.append(advisory_msg)
    return hard, advisory


def _first_heredoc_marker(text: str) -> Optional[str]:
    for marker in _HEREDOC_MARKERS:
        if marker in text:
            return marker
    return None


def check_no_python_heredocs(
    workflows_dir: Path,
    *,
    label_fn,
) -> List[str]:
    """Hard-fail strings for inline python heredocs (policy C3)."""
    errors: List[str] = []
    for path in workflow_paths(workflows_dir):
        marker = _first_heredoc_marker(path.read_text(encoding="utf-8"))
        if marker is not None:
            errors.append(
                f"{label_fn(path)}: inline python heredoc {marker} "
                f"forbidden (policy C3); use scripts/ci instead"
            )
    return errors


def _jobs_mapping(doc: Any) -> dict:
    if not isinstance(doc, dict):
        return {}
    jobs = doc.get("jobs")
    return jobs if isinstance(jobs, dict) else {}


def _reusable_caller_continue_on_error_message(
    path: Path,
    job_id: str,
    job: Any,
    *,
    label_fn,
) -> Optional[str]:
    if not isinstance(job, dict):
        return None
    if "uses" not in job:
        return None
    if "continue-on-error" not in job:
        return None
    return (
        f"{label_fn(path)} job '{job_id}': continue-on-error is "
        f"invalid on a reusable-workflow caller; put it on the "
        f"called job instead (Actions rejects the workflow)"
    )


def _continue_on_error_errors_in_doc(
    path: Path,
    doc: Any,
    *,
    label_fn,
) -> List[str]:
    errors: List[str] = []
    for job_id, job in _jobs_mapping(doc).items():
        message = _reusable_caller_continue_on_error_message(
            path, job_id, job, label_fn=label_fn
        )
        if message is not None:
            errors.append(message)
    return errors


def check_no_continue_on_error_on_reusable_call(
    workflows_dir: Path,
    *,
    label_fn,
) -> List[str]:
    """Hard-fail continue-on-error on jobs that call reusable workflows."""
    if yaml is None:
        return ["PyYAML required to scan continue-on-error on reusable calls"]
    errors: List[str] = []
    for path in workflow_paths(workflows_dir):
        text = path.read_text(encoding="utf-8")
        for doc in yaml.safe_load_all(text):
            errors.extend(
                _continue_on_error_errors_in_doc(path, doc, label_fn=label_fn)
            )
    return errors
