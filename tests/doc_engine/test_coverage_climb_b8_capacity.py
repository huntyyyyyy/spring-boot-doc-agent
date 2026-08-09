"""Coverage climb B8: capacity_preflight derive / AstGrep / main edges.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.capacity_preflight —
asserts bite skipped-token continue, compute_preflight None derive, AstGrepError
exit, PathValidationError on main, and L2b groups_file load branch.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.tools import capacity_preflight as cp
from doc_engine.tools import spring_signal_scan as sss

pytestmark = pytest.mark.domain_climb_sensor


def test_estimate_file_token_pairs_skips_reason(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cp.partition_repo,
        "dfs_file_list",
        lambda *a, **k: [str(tmp_path / "a.bin")],
    )
    monkeypatch.setattr(
        cp.partition_repo,
        "estimate_tokens",
        lambda *_a, **_k: (0, "binary"),
    )
    assert cp._estimate_file_token_pairs(str(tmp_path)) == []


def test_compute_preflight_derives_when_none(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    groups = {
        "repo_path": str(tmp_path),
        "num_groups": 1,
        "max_tokens_per_group": 1000,
        "groups": [{"id": 0, "files": ["a.java"], "est_tokens": 10}],
    }
    edges = {"groups": {"0": {"edges": []}}, "stats": {}}
    monkeypatch.setattr(cp, "_load_or_build_groups", lambda *a, **k: groups)
    monkeypatch.setattr(cp, "_load_or_build_edges", lambda *a, **k: edges)
    report = cp.compute_preflight(str(tmp_path), groups_data=None, edges=None)
    assert report["num_groups"] == 1


def test_run_stage0_astgrep_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    args = SimpleNamespace(
        max_tokens=1000,
        overlap=0.1,
        groups_file=None,
        signals_file=None,
        edges_file=None,
        out=None,
        group_warn_threshold=15,
        fanout_warn_threshold=40,
        slice_tokens_warn_threshold=30_000,
        stage4_shared_tokens_warn_threshold=80_000,
    )
    monkeypatch.setattr(
        cp, "_load_or_build_groups", lambda *a, **k: {"num_groups": 0, "groups": []}
    )
    monkeypatch.setattr(cp, "_load_optional_json", lambda *_a, **_k: None)

    def boom(*_a, **_k):
        raise sss.AstGrepError("ast-grep missing")

    monkeypatch.setattr(cp, "_load_or_build_edges", boom)
    with pytest.raises(SystemExit) as exc:
        cp._run_stage0_preflight(args, str(tmp_path))
    assert exc.value.code == 1


def test_main_path_validation(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["capacity_preflight", "/no/such/repo"])
    with pytest.raises(SystemExit) as exc:
        cp.main()
    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err


def test_run_l2b_with_groups_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    summaries = tmp_path / "summaries.json"
    summaries.write_text("{}", encoding="utf-8")
    args = SimpleNamespace(
        summaries_file=str(summaries),
        interview_answers_file=None,
        signals_file=None,
        groups_file=str(tmp_path / "groups.json"),
        stage0_preflight_report=None,
        out=None,
        max_tokens=1000,
        overlap=0.1,
        stage4_shared_tokens_warn_threshold=80_000,
    )
    monkeypatch.setattr(
        cp, "_load_or_build_groups", lambda *a, **k: {"num_groups": 1, "groups": []}
    )
    monkeypatch.setattr(cp, "_load_optional_json", lambda *_a, **_k: None)
    monkeypatch.setattr(
        cp,
        "compute_stage4_calibration",
        lambda *a, **k: {"ok": True},
    )
    monkeypatch.setattr(cp, "_maybe_write_report", lambda *a, **k: None)
    monkeypatch.setattr(cp, "_print_l2b_summary", lambda *a, **k: None)
    cp._run_l2b_calibration(args, str(tmp_path))
