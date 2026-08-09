"""Shared capacity_preflight test payload factories."""

from __future__ import annotations

import os
import sys
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import (
    build_cross_group_edges,
    capacity_preflight,
    partition_repo,
    spring_signal_scan,
)
SCRIPT_DIR = SCRIPTS_DIR

def _groups_data(num_groups, max_tokens=120000):
    return {
        "repo_path": "/fake/repo",
        "max_tokens_per_group": max_tokens,
        "num_groups": num_groups,
        "groups": [{"id": i, "files": [f"f{i}.java"], "est_tokens": 100} for i in range(num_groups)],
    }


def _edges_data(num_groups, arcs_per_group=0, arc_width=0):
    """Synthetic cross_group_edges.json, shaped like build_report()'s output.

    arc_width pads each arc so a slice can be made large enough to trip the
    token threshold without needing thousands of rows."""
    return {
        "num_groups": num_groups,
        "groups": {
            str(i): {
                "outbound": [
                    {"from": f"f{i}.java", "to": f"g{j}.java", "confidence": "exact",
                     "pad": "x" * arc_width}
                    for j in range(arcs_per_group)
                ],
                "inbound": [],
                "same_package_outside": [],
            }
            for i in range(num_groups)
        },
        "stats": {},
    }


def _pkg(path, package):
    return {"file": path, "line": 1, "match": f"package {package};", "rule_id": "references__package"}


def _imp(path, qualified):
    return {"file": path, "line": 2, "match": f"import {qualified};", "rule_id": "references__import"}
