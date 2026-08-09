"""Coverage climb: capacity preflight groups/edges/compute/stage4 paths."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from doc_engine.tools import capacity_preflight as cap
from doc_engine.tools import spring_drift_check as drift

pytestmark = pytest.mark.domain_climb_sensor

def test_groups_payload_and_load_or_build(tmp_path: Path) -> None:
    groups_file = tmp_path / "groups.json"
    payload = {
        "num_groups": 1,
        "groups": [{"id": 0, "files": ["a.java"], "est_tokens": 10}],
        "max_tokens_per_group": 100,
        "repo_path": str(tmp_path),
    }
    groups_file.write_text(json.dumps(payload), encoding="utf-8")
    assert cap._load_or_build_groups(str(tmp_path), 100, 0.1, str(groups_file)) == payload

    shaped = cap._groups_payload(
        str(tmp_path),
        50,
        0.2,
        [("a.java", 3), ("b.java", 4)],
        [[("a.java", 3)], [("b.java", 4)]],
    )
    assert shaped["num_groups"] == 2
    assert shaped["groups"][0]["est_tokens"] == 3

    edges_file = tmp_path / "edges.json"
    edges_file.write_text(json.dumps({"groups": {}, "stats": {"x": 1}}), encoding="utf-8")
    edges = cap._load_or_build_edges(str(tmp_path), None, payload, str(edges_file))
    assert edges["stats"]["x"] == 1

    signals_file = tmp_path / "signals.json"
    signals_file.write_text(json.dumps({"evidence": {}}), encoding="utf-8")

    def fake_build(groups_data, signals_data):
        return {"groups": {"g0": {}}, "stats": {"from": "build"}}

    monkey_mod = cap.build_cross_group_edges
    original = monkey_mod.build_report
    monkey_mod.build_report = fake_build
    try:
        built = cap._load_or_build_edges(
            str(tmp_path), str(signals_file), payload, None
        )
        assert built["stats"]["from"] == "build"
    finally:
        monkey_mod.build_report = original

def test_compute_preflight_and_warnings() -> None:
    groups = {
        "repo_path": "/r",
        "num_groups": 20,
        "max_tokens_per_group": 1000,
        "groups": [{"id": i, "files": [f"{i}.java"], "est_tokens": 5000} for i in range(20)],
    }
    edges = {
        "groups": {str(i): {"edges": list(range(200))} for i in range(20)},
        "stats": {"reduction_factor": 2},
    }
    report = cap.compute_preflight(
        "/r",
        groups_data=groups,
        edges=edges,
        signals_data={"n": 1},
        group_warn_threshold=5,
        fanout_warn_threshold=10,
        slice_tokens_warn_threshold=1,
        stage4_shared_tokens_warn_threshold=1,
    )
    assert report["num_groups"] == 20
    assert report["total_fanout"] > 10
    dims = {w["dimension"] for w in report["warnings"]}
    assert "num_groups" in dims
    assert "total_fanout" in dims
    assert report["edge_join_stats"]["reduction_factor"] == 2

def test_stage4_calibration_and_proxy_resolve() -> None:
    groups = {
        "repo_path": "/r",
        "groups": [{"est_tokens": 100}],
        "num_groups": 1,
    }
    stage0 = {
        "repo_path": "/r",
        "stage4_metric_kind": "partial_proxy_pre_stage4",
        "stage4_summaries_est_tokens": 80,
        "stage4_interview_answers_est_tokens": 0,
        "stage4_signals_est_tokens": 5,
        "stage4_shared_pool_upper_bound_est_tokens": 85,
    }
    warnings: list = []
    pool, src = cap._resolve_stage4_proxy(stage0, groups, warnings)
    assert src == "stage0_preflight_report"
    assert pool["shared_pool_upper_bound_est_tokens"] == 85
    assert warnings  # both sources → warning
    pool2, src2 = cap._resolve_stage4_proxy(None, groups, [])
    assert src2 == "groups_est_tokens_proxy"
    assert pool2 is not None
    assert cap._resolve_stage4_proxy(None, None, []) == (None, None)

    cal = cap.compute_stage4_calibration(
        "/r",
        summaries_data={"s": 1},
        interview_answers={"q": "a"},
        signals_data={"e": []},
        groups_data=groups,
        stage0_preflight_report=stage0,
        stage4_shared_tokens_warn_threshold=1,
    )
    assert cal["mode"] == "stage4_calibration"
    assert cal["stage4_proxy_comparison"]["proxy_source"] == "stage0_preflight_report"

def test_run_l2b_and_stage0_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    summaries = tmp_path / "summaries.json"
    summaries.write_text("{}", encoding="utf-8")
    out = tmp_path / "out.json"
    args = SimpleNamespace(
        summaries_file=str(summaries),
        interview_answers_file=None,
        signals_file=None,
        groups_file=None,
        stage0_preflight_report=None,
        stage4_shared_tokens_warn_threshold=80_000,
        out=str(out),
        max_tokens=100,
        overlap=0.1,
    )
    monkeypatch.setattr(cap, "checked_path", lambda p, want=None: Path(p))
    monkeypatch.setattr(cap, "checked_output_path", lambda p: Path(p))
    monkeypatch.setattr(
        cap,
        "compute_stage4_calibration",
        lambda *a, **k: {
            "mode": "stage4_calibration",
            "warnings": [],
            "stage4_shared_pool_upper_bound_est_tokens": 1,
            "stage4_summaries_est_tokens": 1,
            "stage4_interview_answers_est_tokens": 0,
            "stage4_interview_answers_omitted": True,
            "stage4_signals_est_tokens": 0,
            "stage4_signals_omitted": True,
            "stage4_omitted_not_estimated": [],
            "stage4_proxy_comparison": None,
        },
    )
    cap._run_l2b_calibration(args, str(tmp_path))
    assert out.is_file()

    report = {
        "num_groups": 1,
        "total_fanout": 2,
        "stage1_slice_est_tokens_max": 1,
        "stage1_slice_est_tokens_total": 1,
        "edge_join_stats": {"reduction_factor": 2},
        "stage4_shared_pool_upper_bound_est_tokens": 1,
        "stage4_omitted_not_estimated": [],
        "stage4_signals_omitted": True,
        "warnings": [],
    }
    monkeypatch.setattr(
        cap,
        "_load_or_build_groups",
        lambda *a, **k: {"num_groups": 1, "groups": []},
    )
    monkeypatch.setattr(
        cap,
        "_load_or_build_edges",
        lambda *a, **k: {"groups": {}, "stats": {}},
    )
    monkeypatch.setattr(cap, "compute_preflight", lambda *a, **k: report)
    monkeypatch.setattr(cap, "_maybe_write_report", lambda *a, **k: None)
    args2 = SimpleNamespace(
        max_tokens=100,
        overlap=0.1,
        groups_file=None,
        signals_file=None,
        edges_file=None,
        group_warn_threshold=15,
        fanout_warn_threshold=40,
        slice_tokens_warn_threshold=30_000,
        stage4_shared_tokens_warn_threshold=80_000,
        out=None,
    )
    cap._run_stage0_preflight(args2, str(tmp_path))
    assert "capacity-preflight" in capsys.readouterr().out
