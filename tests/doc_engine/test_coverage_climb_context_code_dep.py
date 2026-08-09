"""Coverage climb: local_runner context wiring + R_code|dep helpers."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.pipeline.local_runner_phases import context as ctx_mod
from doc_engine.scanning.gap_probe import code_dep as dep

pytestmark = pytest.mark.domain_climb_sensor

def test_ensure_citation_pool_and_todos(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = tmp_path / "out"
    out.mkdir()
    ctx = SimpleNamespace(
        pool=None,
        signals={"evidence": {}},
        repo_path=repo,
        out_dir=out,
        todos=None,
        groups=[],
        edges={},
        today="2026-01-01",
        docs_dir=out / "docs",
        existing_readme=None,
    )
    monkeypatch.setattr(ctx_mod, "load_citations", lambda *a, **k: ["c1"])
    assert ctx_mod._ensure_citation_pool(ctx) == ["c1"]
    assert ctx.pool == ["c1"]
    # Second call reuses pool.
    assert ctx_mod._ensure_citation_pool(ctx) == ["c1"]

    monkeypatch.setattr(ctx_mod, "sweep_todos", lambda *_a, **_k: [{"todo": 1}])
    monkeypatch.setattr(ctx_mod, "_write_json", lambda *_a, **_k: None)
    ctx_mod._ensure_todos(ctx)
    assert ctx.todos == [{"todo": 1}]
    ctx_mod._ensure_todos(ctx)  # early return

def test_handlers_and_partition(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    calls: list[str] = []
    ctx = SimpleNamespace(
        pool=["p"],
        signals={},
        repo_path=tmp_path,
        out_dir=tmp_path,
        groups=[],
        edges={},
        todos=[],
        today="t",
        docs_dir=tmp_path / "docs",
        existing_readme=None,
    )
    monkeypatch.setattr(ctx_mod, "_ensure_citation_pool", lambda c: c.pool)
    monkeypatch.setattr(ctx_mod, "_ensure_todos", lambda c: None)
    monkeypatch.setattr(
        ctx_mod, "mock_file_summaries", lambda *a, **k: calls.append("sum") or "ok"
    )
    monkeypatch.setattr(
        ctx_mod, "mock_architecture", lambda *a, **k: calls.append("arch") or "ok"
    )
    monkeypatch.setattr(
        ctx_mod, "mock_gap_and_interview", lambda *a, **k: calls.append("gap") or "ok"
    )
    monkeypatch.setattr(ctx_mod, "_read_json", lambda *_a, **_k: {})
    monkeypatch.setattr(ctx_mod, "find_existing_readme", lambda *_a, **_k: None)
    monkeypatch.setattr(
        ctx_mod, "mock_docs", lambda *a, **k: calls.append("docs") or "ok"
    )
    log = lambda *a, **k: None
    assert ctx_mod._handler_file_summarize(ctx, log) == "ok"
    assert ctx_mod._handler_architect(ctx, log) == "ok"
    assert ctx_mod._handler_gap(ctx, log) == "ok"
    assert ctx_mod._handler_doc_writer(ctx, log) == "ok"
    assert set(calls) == {"sum", "arch", "gap", "docs"}

    from doc_engine.pipeline.context import StageKind

    specs = [
        SimpleNamespace(kind=StageKind.DETERMINISTIC, name="d"),
        SimpleNamespace(kind=StageKind.GENERATIVE, name="g"),
    ]
    det, gen = ctx_mod._partition_specs_by_kind(specs)
    assert len(det) == 1 and len(gen) == 1

    state = SimpleNamespace(
        skip_signal_scan=True,
        runner=SimpleNamespace(record=lambda *a, **k: calls.append("rec")),
        args=SimpleNamespace(signals_file="signals.json"),
    )
    ctx_mod._record_reused_signal_scan(state)
    assert "rec" in calls
    state.skip_signal_scan = False
    ctx_mod._record_reused_signal_scan(state)

def test_select_specs_error_and_mock_executor(monkeypatch: pytest.MonkeyPatch) -> None:
    state = SimpleNamespace(
        profile="certified",
        skip_signal_scan=False,
        until_stage=None,
    )
    monkeypatch.setattr(
        ctx_mod,
        "stages_for_profile",
        lambda *a, **k: (_ for _ in ()).throw(ValueError("bad profile")),
    )
    assert ctx_mod._select_specs_for_state(state) == 2
    ex = ctx_mod._build_mock_executor(lambda *a, **k: None)
    assert "file_summarize" in ex._handlers

def test_phase_build_context_wires_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from doc_engine.pipeline.context import StageKind

    specs = [SimpleNamespace(kind=StageKind.DETERMINISTIC, name="d")]
    state = SimpleNamespace(
        args=SimpleNamespace(respect_gitignore=False, max_tokens=1000, signals_file=None),
        log=lambda *a, **k: None,
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out"),
        manifest=str(tmp_path / "m.json"),
        docs_dir=str(tmp_path / "docs"),
        py="python",
        today="2026-01-01",
        profile="certified",
        skip_signal_scan=False,
        until_stage=None,
        runner=SimpleNamespace(record=lambda *a, **k: None),
    )
    (tmp_path / "out").mkdir()
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(ctx_mod, "find_existing_readme", lambda *_a, **_k: None)
    monkeypatch.setattr(ctx_mod, "_select_specs_for_state", lambda _s: specs)
    assert ctx_mod.phase_build_context(state) is None
    assert state.selected_specs == specs
    assert state.deterministic_specs == specs

def test_code_dep_family_coverage_and_measure() -> None:
    assert dep._row_text({"match": "a", "rule_id": "r"}, ("match", "rule_id")) == "a r"
    counts = dep._count_deployment_families(
        [
            {"match": "redis client", "rule_id": "deployment__x"},
            {"match": "kafka topic", "file": "m.java"},
            "skip",
        ]
    )
    assert counts.get("redis", 0) >= 1
    assert counts.get("messaging", 0) >= 1
    covered, row, failure = dep._family_coverage("redis", 2, 0)
    assert covered == 0 and failure is not None
    covered2, _, failure2 = dep._family_coverage("redis", 2, 3)
    assert covered2 == 2 and failure2 is None
    block = dep.measure_r_code_dep(
        {
            "evidence": {
                "deployment": [{"match": "redis"}],
                "observability": [{"match": "redis cache"}],
                "configuration": [],
                "outbound_clients": [],
            }
        }
    )
    assert block["rate"] == 1.0
    assert "redis" in block["per_family"]
