"""Coverage climb B9: partition GroupsArtifact, markers __main__, dag edges.

Q2 adequacy witness: mutmut_slice on artifacts.partition, markers_apply, dag —
asserts bite groups-length ValueError, __main__ SystemExit, self-cycle path,
and BFS seen-continue.
"""

from __future__ import annotations

import runpy
import sys

import pytest
from pydantic import ValidationError

from doc_engine.ci import test_domain_markers_apply as markers
from doc_engine.pipeline.artifacts.partition import GroupsArtifact
from stf.graph import dag as dag_mod

pytestmark = pytest.mark.domain_climb_sensor

def test_partition_groups_length_mismatch() -> None:
    with pytest.raises(ValidationError, match="groups length"):
        GroupsArtifact.model_validate(
            {
                "repo_path": "/r",
                "max_tokens_per_group": 1,
                "overlap": 0.1,
                "total_files_considered": 0,
                "total_files_skipped": 0,
                "skipped": [],
                "num_groups": 2,
                "groups": [{"id": 0, "files": [], "est_tokens": 0}],
            }
        )

def test_markers_apply_dunder_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(markers, "main", lambda: 0)
    monkeypatch.setattr(sys, "argv", ["test_domain_markers_apply"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_path(markers.__file__, run_name="__main__")
    assert exc.value.code == 0

def test_dag_cycle_self_and_bfs_continue() -> None:
    # node in visiting but not stack → [node, node]
    visiting = {"A"}
    assert dag_mod._dfs_cycle("A", {"A": set()}, visiting, set(), []) == ["A", "A"]
    # BFS continue when revisiting
    reachable = dag_mod._bfs_reachable(["A"], {"A": {"A", "B"}, "B": set()})
    assert "A" in reachable
