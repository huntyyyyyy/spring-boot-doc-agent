"""Map test node ids to mid-suite plateau buckets (E-RUN1 / D2).

Path-prefix labels match research 08 plateau map for ``domain_ci_meta``.

Usage:
    from doc_engine.ci.suite_timing.plateau_buckets import plateau_label_for
"""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

from doc_engine.ci.suite_timing.duration_records import CaseDuration

# Longest-prefix-first: real repo_claims before generic repo_claims tokens.
_PLATEAU_PREFIXES: tuple[tuple[str, str], ...] = (
    ("tests.ci.test_repo_claims_real", "repo_claims_real"),
    ("tests/ci/test_repo_claims_real", "repo_claims_real"),
    ("tests.ci.test_gate_tools", "gate_tools"),
    ("tests/ci/test_gate_tools", "gate_tools"),
    ("tests.ci.test_run_manifest", "run_manifest"),
    ("tests/ci/test_run_manifest", "run_manifest"),
)

OTHER_BUCKET = "other"
KNOWN_BUCKETS: tuple[str, ...] = (
    "gate_tools",
    "repo_claims_real",
    "run_manifest",
    OTHER_BUCKET,
)


def _normalized_node(node_id: str) -> str:
    return node_id.replace("\\", "/")


def plateau_label_for(node_id: str) -> str:
    """Return plateau bucket for a junit classname::name node id."""
    normalized = _normalized_node(node_id)
    for prefix, label in _PLATEAU_PREFIXES:
        if prefix in normalized:
            return label
    return OTHER_BUCKET


def plateau_totals_seconds(
    records: Sequence[CaseDuration],
) -> Mapping[str, float]:
    """Sum duration seconds per plateau bucket (zeros for empty known buckets)."""
    totals: dict[str, float] = defaultdict(float)
    for label in KNOWN_BUCKETS:
        totals[label] = 0.0
    for record in records:
        label = plateau_label_for(record.node_id)
        totals[label] += record.duration_seconds
    return dict(totals)
