"""Coverage climb: query load/packet/schema + spring scan + support/stf gaps.

Distinct from capacity_preflight / CodeQL-runner climb slices.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from doc_engine.pipeline.local_runner_phases import support as phase_support
from doc_engine.query import kinds as kinds_mod
from doc_engine.query import load as load_mod
from doc_engine.query import packet as packet_mod
from doc_engine.query import schema_check as schema_mod
from doc_engine.query.handlers import dependents as dep_mod
from doc_engine.query.handlers import facts as facts_mod
from doc_engine.scanning import spring as spring_mod
from stf.runners import implement as implement_mod
from stf.runners.store import TasksStore
from stf.schemas.blockers import BlockerClass
from stf.validators import lint_tasks as lint_mod
from tests.stf.conftest import build_minimal_valid_tasks


# --- query/load.py ----------------------------------------------------------


def test_require_server_root_env_and_blank(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("DOC_ENGINE_ROOT", raising=False)
    monkeypatch.delenv("DOC_ENGINE_RUN_DIR", raising=False)
    with pytest.raises(load_mod.QueryPathError, match="must be set"):
        load_mod.require_server_root()
    monkeypatch.setenv("DOC_ENGINE_ROOT", "   ")
    with pytest.raises(load_mod.QueryPathError, match="must be set"):
        load_mod.require_server_root()
    monkeypatch.setenv("DOC_ENGINE_ROOT", str(tmp_path))
    assert load_mod.require_server_root() == tmp_path.resolve()


def test_resolve_oserror_and_escape(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(load_mod.QueryPathError, match="containment root is required"):
        load_mod._resolve(tmp_path / "a.json", root=None)

    target = tmp_path / "a.json"
    target.write_text("{}", encoding="utf-8")
    real_resolve = Path.resolve

    def _boom(self, *a, **k):
        if self.name == "a.json":
            raise OSError("boom")
        return real_resolve(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", _boom)
    with pytest.raises(load_mod.QueryPathError, match="cannot resolve path"):
        load_mod._resolve(target, root=tmp_path)
    monkeypatch.setattr(Path, "resolve", real_resolve)

    outside = tmp_path.parent / "outside-artifact.json"
    outside.write_text("{}", encoding="utf-8")
    with pytest.raises(load_mod.QueryPathError, match="escapes root"):
        load_mod._resolve(outside, root=tmp_path)


def test_read_artifact_nul_and_missing(tmp_path: Path) -> None:
    nul = tmp_path / "bad.json"
    nul.write_bytes(b'{"a":1}\x00')
    with pytest.raises(load_mod.QueryError, match="NUL"):
        load_mod._read_artifact_text(nul, kind="JSON")
    missing = tmp_path / "gone.jsonl"
    with pytest.raises(load_mod.QueryMissingError):
        load_mod.load_jsonl(missing, root=tmp_path)


def test_jsonl_rejects_non_object_row(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"
    path.write_text("[1]\n", encoding="utf-8")
    with pytest.raises(load_mod.QueryError, match="must be object"):
        load_mod.load_jsonl(path, root=tmp_path)


# --- query/schema_check.py --------------------------------------------------


def test_schema_path_unknown_and_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(load_mod.QueryError, match="unknown envelope"):
        schema_mod.schema_path("nope")
    monkeypatch.setattr(schema_mod, "_SCHEMA_DIR", tmp_path)
    with pytest.raises(load_mod.QueryError, match="schema missing"):
        schema_mod.schema_path("query_result")


def test_validate_envelope_kind_mismatches() -> None:
    with pytest.raises(load_mod.QueryError, match="context-packet"):
        schema_mod._check_kind_specific(
            "context_packet", {"kind": "wrong", "schema_version": 1}
        )
    with pytest.raises(load_mod.QueryError, match="must be a list"):
        schema_mod._check_kind_specific("query_result", {"rows": {}})


# --- query/kinds.py ---------------------------------------------------------


def test_list_mcp_tools_and_unknown_kind() -> None:
    names = kinds_mod.list_mcp_tool_names()
    assert "doc_engine_help" in names
    assert "query_evidence" in names
    with pytest.raises(KeyError, match="unknown query kind"):
        kinds_mod.get_query_kind_spec("not-a-kind")


# --- query/packet.py --------------------------------------------------------


def test_clamp_budget_edges() -> None:
    assert packet_mod._clamp_budget(None) == packet_mod.DEFAULT_BUDGET_TOKENS
    assert packet_mod._clamp_budget(-5) == 0
    assert packet_mod._clamp_budget(packet_mod.MAX_BUDGET_TOKENS + 99) == packet_mod.MAX_BUDGET_TOKENS


def test_resolve_run_missing_and_escape(tmp_path: Path) -> None:
    with pytest.raises(load_mod.QueryMissingError, match="missing run dir"):
        packet_mod._resolve_run_under_root(tmp_path / "nope", tmp_path)
    run = tmp_path / "run"
    run.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(load_mod.QueryPathError, match="escapes root"):
        packet_mod._resolve_run_under_root(run, other)


def test_load_run_artifacts_rejects_non_object(tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    (run / "spring_signals.json").write_text("[]", encoding="utf-8")
    with pytest.raises(load_mod.QueryError, match="must be an object"):
        packet_mod._load_run_artifacts(run, tmp_path)


def test_file_signature_and_freshness_helpers(tmp_path: Path) -> None:
    assert packet_mod._normalized_rel_path(r"a\b.java") == "a/b.java"
    assert packet_mod._file_signature_matches(tmp_path / "missing.java", "sig") is False
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature

    sig = compute_file_signature(str(src))
    assert packet_mod._file_signature_matches(src, sig) is True
    assert packet_mod._file_signature_matches(src, None) is False
    live = packet_mod._live_paths_matching_signatures(
        tmp_path, {"A.java": sig}, {"A.java", "missing.java"}
    )
    assert "A.java" in live
    assert "missing.java" not in live


def test_build_freshness_policy_assume_and_drift(tmp_path: Path) -> None:
    policy = packet_mod._build_freshness_policy(
        repo_path=None,
        signals={},
        primary=[],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy.__class__.__name__ == "UnknownFreshnessWhenNoRepo"
    drift = tmp_path / "drift.json"
    drift.write_text("[]", encoding="utf-8")
    wrapped = packet_mod._wrap_freshness_with_drift_report(
        SimpleNamespace(), drift, tmp_path
    )
    assert wrapped.__class__.__name__ != "DriftReportFreshness"
    report = tmp_path / "ok.json"
    report.write_text(json.dumps({"changed_files": ["a.java"]}), encoding="utf-8")
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature
    from doc_engine.query.freshness import SignatureFreshness

    sig = compute_file_signature(str(src))
    inner = SignatureFreshness(
        repo_root=tmp_path, signatures={"A.java": sig}, live_paths=set()
    )
    drifted = packet_mod._wrap_freshness_with_drift_report(inner, report, tmp_path)
    assert drifted.__class__.__name__ == "DriftReportFreshness"
    labeled = packet_mod._label_items(policy, [{"path": "A.java"}, {"path": 1}])
    assert labeled[0]["freshness"] == "unknown"


def test_score_partition_and_assemble() -> None:
    scored = packet_mod._score_raw(
        "auth",
        {
            "provider": "facts",
            "path": "a.java",
            "match": "sec",
            "bucket": "security",
            "contested": True,
        },
    )
    assert scored["provider"] == "facts"
    findings, risks, rest = packet_mod._partition_by_provider(
        [
            {"provider": "facts", "score": 1},
            {"provider": "redaction", "score": 1},
            {"provider": "other", "score": 1},
        ]
    )
    assert len(findings) == 1 and len(risks) == 1 and len(rest) == 1
    packet = packet_mod._assemble_packet(
        request="r",
        budget=10,
        tokens_used=1,
        truncated=False,
        primary=[],
        related=[],
        findings=[],
        risks=[],
        providers_used=["facts"],
    )
    assert packet["empty"] is True
    assert packet["kind"] == "context-packet"


def test_build_freshness_with_repo(tmp_path: Path) -> None:
    src = tmp_path / "A.java"
    src.write_text("class A {}", encoding="utf-8")
    from doc_engine.core.walk import compute_file_signature

    sig = compute_file_signature(str(src))
    policy = packet_mod._build_freshness_policy(
        repo_path=tmp_path,
        signals={"file_signatures": {"A.java": sig, "bad": 1}},
        primary=[{"path": "A.java"}],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy.__class__.__name__ == "SignatureFreshness"
    # non-mapping signatures coerced to empty
    policy2 = packet_mod._build_freshness_policy(
        repo_path=tmp_path,
        signals={"file_signatures": ["nope"]},
        primary=[],
        drift_report_path=None,
        root_path=tmp_path,
    )
    assert policy2.__class__.__name__ == "SignatureFreshness"


# --- query/handlers ---------------------------------------------------------


def test_facts_filters_and_unknown_predicate() -> None:
    rows = [
        {"predicate": "MAPS_TO", "file": "a/b.java", "subject": "Foo", "qualifiers": {"fqcn": "c.Foo"}},
        {"predicate": "CUSTOM", "file": "x.java", "subject": "Bar", "qualifiers": "bad"},
        "skip-me",
    ]
    with pytest.raises(load_mod.QueryError, match="unknown facts predicate"):
        facts_mod.query_facts(rows, predicate="NOPE")
    hit = facts_mod.query_facts(
        rows,
        predicate="MAPS_TO",
        file_contains="a/",
        fqcn="c.Foo",
        subject_contains="Foo",
    )
    assert len(hit) == 1
    assert facts_mod._fqcn_of({"qualifiers": "x"}) == ""
    assert facts_mod.query_facts(rows, predicate="CUSTOM")[0]["predicate"] == "CUSTOM"


def test_dependents_want_filters_and_edges() -> None:
    assert dep_mod._normalize_want_file(None) is None
    assert dep_mod._normalize_want_file(r"a\b.java") == "a/b.java"
    assert dep_mod._matches_want_type("com.Foo", "Foo") is True
    assert dep_mod._passes_target_filters("a.java", "a.java", "x", None, None) is False
    assert dep_mod._arc_direction("a.java", "b.java", "a.java") == "outbound"
    assert dep_mod._arc_direction("a.java", "b.java", "b.java") == "inbound"
    assert dep_mod._from_edges({"groups": {}}, "missing", target_file=None) == []
    edges = {
        "groups": {
            "1": {
                "outbound": [{"from": "a.java", "to": "b.java"}, "skip"],
                "inbound": [{"from": "c.java", "to": "a.java"}],
            }
        }
    }
    rows = dep_mod._from_edges(edges, 1, target_file="a.java")
    assert {r["direction"] for r in rows} == {"outbound", "inbound"}


# --- scanning/spring.py scan entry ------------------------------------------


def test_scan_prepares_and_runs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spring_mod, "resolve_scanner_names", lambda _s: ["filesystem"])
    monkeypatch.setattr(
        spring_mod,
        "get_scanner",
        lambda _n: SimpleNamespace(name="filesystem", version_hash=lambda: "v"),
    )
    monkeypatch.setattr(
        "doc_engine.config.repo_trust.require_codeql_build_allowed",
        lambda *_a, **_k: None,
    )
    monkeypatch.setattr(
        spring_mod,
        "_run_spring_scan",
        lambda *a, **k: {"ok": True, "build": k.get("build_command")},
    )
    out = spring_mod.scan(str(tmp_path), scanners=["filesystem"], allow_codeql_build=False)
    assert out["ok"] is True


def test_tool_on_path_misses_all(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spring_mod.shutil, "which", lambda _n: None)
    assert spring_mod._tool_on_path("gradle", "gradle.bat") is None


def test_gradle_maven_tool_requires_marker_and_binary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert spring_mod._gradle_tool_command(str(tmp_path), "g") is None
    (tmp_path / "build.gradle").write_text("//", encoding="utf-8")
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: None)
    assert spring_mod._gradle_tool_command(str(tmp_path), "g") is None
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: "C:/gradle")
    assert "gradle" in (spring_mod._gradle_tool_command(str(tmp_path), "g") or "")

    assert spring_mod._maven_tool_command(str(tmp_path), "m") is None
    (tmp_path / "pom.xml").write_text("<project/>", encoding="utf-8")
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: None)
    assert spring_mod._maven_tool_command(str(tmp_path), "m") is None
    monkeypatch.setattr(spring_mod, "_tool_on_path", lambda *_n: "C:/mvn")
    assert "mvn" in (spring_mod._maven_tool_command(str(tmp_path), "m") or "")


# --- local_runner_phases/support.py remaining -------------------------------


def test_runner_keep_going_and_quiet_paths(tmp_path: Path) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner = phase_support.Runner(log, keep_going=True)
        runner._mark_critical_abort("stage0")
        assert runner.aborted is False
        runner._log_step_header("q", ["echo", "hi there"], quiet=True)
        runner.mock("m", lambda: (_ for _ in ()).throw(RuntimeError("x")))
        assert runner.aborted is False
        assert any(r[1] == "ERROR" for r in runner.results)
        runner.results.clear()
        runner.record("x", "FAIL", 0.1, "e")
        assert len(runner.gates_failed()) == 1
        runner.table()
    finally:
        log.close()


def test_emit_certification_with_notice_and_failure(tmp_path: Path) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner = phase_support.Runner(log, keep_going=False)
        runner.record("pipeline:s1", "FAIL", 0.0, "boom")
        report = SimpleNamespace(
            certified=False,
            stages=[SimpleNamespace(name="s1", status="fail")],
        )
        phase_support._emit_certification_outcome(
            log, runner, report, success_lines=["ok"], notice_lines=None
        )
        phase_support._emit_certification_outcome(
            log,
            runner,
            SimpleNamespace(certified=True, stages=[]),
            success_lines=["done"],
            notice_lines=["note"],
        )
        summary = phase_support._certification_failure_summary(runner, report)
        assert "stages:" in summary
    finally:
        log.close()


def test_write_certification_finish_uncertified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner = phase_support.Runner(log, keep_going=False)
        runner.record("pipeline:s1", "OK", 0.1, "")
        report = SimpleNamespace(certified=False, stages=[])
        monkeypatch.setattr(
            phase_support,
            "_build_and_write_certification",
            lambda *a, **k: (report, tmp_path / "certification.json"),
        )
        code = phase_support._write_certification_and_finish(
            log,
            runner,
            "certified",
            str(tmp_path),
            str(tmp_path),
            "mock",
            allow_mock=True,
            show_table=False,
            success_lines=None,
            notice_lines=["heads-up"],
        )
        assert code == 1
    finally:
        log.close()


def test_run_drift_with_prior_signals(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner = phase_support.Runner(log, keep_going=True)
        called: list[Any] = []

        def _capture(label, argv, **_k):
            called.append((label, argv))
            return None

        runner.run = _capture  # type: ignore[method-assign]
        prior = tmp_path / "prior.json"
        prior.write_text("{}", encoding="utf-8")
        args = SimpleNamespace(skip_drift=False, prior_signals=str(prior))
        phase_support._run_drift_check(
            log, runner, str(tmp_path), str(tmp_path / "m.json"), str(tmp_path), args, str(tmp_path / "sig.json")
        )
        assert called and called[0][0] == "spring_drift_check"
        assert str(prior.resolve()) in called[0][1]
    finally:
        log.close()


# --- stf implement + lint mutate --------------------------------------------


def test_finding_coverage_requires_critical_inv() -> None:
    tasks = build_minimal_valid_tasks()
    spec = SimpleNamespace(finding_ids=["C99", "N2"])
    assert implement_mod._finding_coverage(tasks, None) is True
    assert implement_mod._finding_coverage(tasks, spec) is False
    tasks.tasks[0].inputs.append({"origin": "INV-C99", "datum": "x"})
    assert implement_mod._finding_coverage(tasks, spec) is True


def test_wrapper_command_present(tmp_path: Path) -> None:
    assert spring_mod._wrapper_command(str(tmp_path), "gradlew", "build") is None
    (tmp_path / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod._wrapper_command(str(tmp_path), "gradlew", "build")
    assert cmd is not None and "gradlew" in cmd
    assert spring_mod._first_wrapper_command(str(tmp_path), ("missing", "gradlew"), "g") is not None
    assert spring_mod._first_wrapper_command(str(tmp_path), ("missing",), "g") is None


def test_plan_gate_fails_on_lint(monkeypatch: pytest.MonkeyPatch) -> None:
    tasks = build_minimal_valid_tasks()
    monkeypatch.setattr(
        implement_mod,
        "lint_tasks_document",
        lambda *_a, **_k: [SimpleNamespace(level="FAIL", name="x")],
    )
    monkeypatch.setattr(
        implement_mod,
        "lint_summary",
        lambda _r: {"ok": False, "fail": 1},
    )
    with pytest.raises(implement_mod.PlanGateError, match="plan gate failed"):
        implement_mod.plan_gate(tasks, None)


def test_run_waves_and_constitution(tmp_path: Path) -> None:
    store = TasksStore(tmp_path)
    store.write_tasks(build_minimal_valid_tasks())
    dry = implement_mod.run_waves(store)
    assert "executed" in dry
    seen: list[str] = []
    store.write_tasks(build_minimal_valid_tasks())
    live = implement_mod.run_waves(store, task_fn=seen.append, max_concurrent=2)
    assert sorted(seen) == sorted(live["executed"])
    (tmp_path / "CONSTRAINTS.md").write_text("c", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("l", encoding="utf-8")
    text = implement_mod.constitution_excerpts(tmp_path, max_chars=100)
    assert "CONSTRAINTS.md" in text and "CLAUDE.md" in text


def test_append_blocker_stalls(tmp_path: Path) -> None:
    store = TasksStore(tmp_path)
    store.write_tasks(build_minimal_valid_tasks())
    blocker = implement_mod.append_blocker(
        store,
        title="blocked",
        falsified="assumption",
        evidence="e",
        class_=BlockerClass.DECISION,
        falsified_tasks=["T0"],
    )
    assert blocker.id.startswith("B")
    assert store.load_tasks().ledger.value == "stall"


def test_mutate_tasks_modes() -> None:
    tasks = build_minimal_valid_tasks()
    for mode in ("bad-dep", "no-phase", "bad-inventory", "no-acceptance", "bad-blocker", "cycle"):
        mutated = lint_mod.mutate_tasks(tasks, mode)
        assert mutated is not tasks
    with pytest.raises(ValueError, match="unknown mutate mode"):
        lint_mod.mutate_tasks(tasks, "nope")
