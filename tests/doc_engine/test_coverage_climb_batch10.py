"""Coverage climb batch10: covering/validators/secrets/query CLI/cli facades.

Distinct from query-packet/spring/support and capacity/drift climb slices.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine import cli
from doc_engine.query.load import QueryError
from doc_engine.scanning import covering as cov
from doc_engine.tools import check_no_secrets_leaked as secrets
from doc_engine.tools import check_pipeline_output as cpo
from doc_engine.tools import pipeline_validators as pv
from doc_engine.tools import query_artifacts as qa
from doc_engine.tools import validate_artifacts as va


def test_covering_build_receipt_extra_and_verify_edges() -> None:
    sigs = {"a.java": "aa", "b.java": "bb"}
    root = cov.inventory_root(sigs)
    receipt = cov.build_receipt(
        scanner="filesystem",
        version_hash="v1",
        scope="all_signatures",
        expected_subset_root=root,
        acked_subset_root=root,
        status="complete",
        batches=2,
        extra={"note": "x"},
    )
    assert receipt["batches"] == 2 and receipt["note"] == "x"
    ok, why = cov.verify_covering_proof(
        cov.build_covering_proof(
            file_signatures=sigs, scanner_version="sv", receipts=[receipt]
        ),
        file_signatures=sigs,
        scanner_version="sv",
    )
    assert ok and why == ""
    assert "unsupported covering_proof schema_version" in (
        cov._schema_version_error({"schema_version": 99}) or ""
    )
    assert cov._root_and_version_error(
        {"inventory_root": "nope", "scanner_version": "sv", "barrier": {}},
        expected_root=root,
        scanner_version="sv",
    )
    assert cov._root_and_version_error(
        {
            "inventory_root": root,
            "scanner_version": "other",
            "barrier": {"inventory_root": root},
        },
        expected_root=root,
        scanner_version="sv",
    )
    assert cov._root_and_version_error(
        {
            "inventory_root": root,
            "scanner_version": "sv",
            "barrier": {"inventory_root": "x"},
        },
        expected_root=root,
        scanner_version="sv",
    )
    assert "receipt failed" in (
        cov._receipt_status_error({"status": "failed", "scanner": "s", "error": "e"}) or ""
    )
    assert "not complete" in (
        cov._receipt_status_error({"status": "partial", "scanner": "s"}) or ""
    )
    assert cov._receipt_scope_root({"scope": ""}, sigs)[1]
    assert "unknown covering receipt scope" in (
        cov._receipt_scope_root({"scope": "weird"}, sigs)[1] or ""
    )
    bad = dict(receipt)
    bad["expected_subset_root"] = "wrong"
    assert cov._receipt_root_mismatch(bad, recomputed=root)
    bad2 = dict(receipt)
    bad2["acked_subset_root"] = "wrong"
    assert cov._receipt_root_mismatch(bad2, recomputed=root)
    assert "no receipts" in (cov._verify_receipts([], sigs) or "")
    assert cov.java_scope_paths(sigs) == ["a.java", "b.java"]
    assert cov.subset_root(sigs, ["missing.java", "a.java"]) != root


def test_covering_write_and_pop(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "covering_proof.json"
    cov.write_covering_proof(path, {"schema_version": 1})
    assert json.loads(path.read_text(encoding="utf-8"))["schema_version"] == 1
    partial = {"covering_receipt": {"scanner": "x"}, "keep": 1}
    assert cov.pop_receipt(partial) == {"scanner": "x"}
    assert "covering_receipt" not in partial
    assert (
        cov.covering_proof_path_for_signals_out(
            tmp_path / "out" / "spring_signals.json"
        ).name
        == "covering_proof.json"
    )


def test_pipeline_validators_gap_review_and_main(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert "elided" in pv._gap_evidence_problems("see /.../Foo.java:1")[0]
    assert "no file citation" in pv._gap_evidence_problems("plain prose only")[0]
    assert pv._gap_evidence_problems("")[0].startswith("evidence must")
    problems = pv._validate_external_research(
        0,
        {"verdict": "CONFIRMED", "sources": [{"tier": "C", "url": "https://x"}]},
    )
    assert any("Tier C" in p[1] for p in problems)
    problems2 = pv._validate_external_research(
        0, {"verdict": "NOPE", "sources": [{"tier": "Z"}]}
    )
    assert len(problems2) >= 2
    labels = pv.extract_mermaid_node_labels('A["Alpha"] --> B[Beta]')
    assert "Alpha" in labels and "Beta" in labels
    assert pv.find_untraceable_nodes('N["Ghost"]', {"Alpha"}) == ["Ghost"]
    assert "not a directory" in pv.run_stage5_gate(str(tmp_path / "missing"), "x")[0]
    review = tmp_path / "architecture_testing_review.json"
    review.write_text("{}", encoding="utf-8")
    fails = pv._failures_from_review_json(review)
    assert fails and "JSON array" in fails[0]
    review.unlink()
    (tmp_path / "gap_questions.json").write_text(
        json.dumps(
            [
                {
                    "blocks_file": "readme",
                    "topic": "t",
                    "question": "q?",
                    "evidence": "src/A.java:1",
                }
            ]
        ),
        encoding="utf-8",
    )
    assert pv.main([str(tmp_path)]) == 0
    assert "OK" in capsys.readouterr().out
    (tmp_path / "summaries.json").write_text(json.dumps([{"file": "x"}]), encoding="utf-8")
    assert pv.main([str(tmp_path)]) == 1


def test_secrets_main_and_skip_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    clean = tmp_path / "ok.md"
    clean.write_text("no secrets here\n", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv", ["check_no_secrets_leaked", str(clean), str(tmp_path / "gone")]
    )
    assert secrets.main() == 0
    assert "skipping" in capsys.readouterr().err
    leak = tmp_path / "bad.md"
    leak.write_text("password: hunter2literal\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check_no_secrets_leaked", str(leak)])
    assert secrets.main() == 1
    monkeypatch.setattr("builtins.open", MagicMock(side_effect=OSError("denied")))
    assert secrets.check([str(clean)]) == {}


def test_check_pipeline_output_main_and_ignored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cpo.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr="boom"),
    )
    assert cpo.list_ignored_untracked(tmp_path) == []
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text("# R\n", encoding="utf-8")
    assert all(v == 0 for v in cpo.summarize_tags(docs).values())
    cpo._print_check_result(docs, ["issue-one"])
    assert "failed" in capsys.readouterr().err
    cpo._print_check_result(docs, [])
    assert "OK:" in capsys.readouterr().out
    assert cpo._resolve_dirs(SimpleNamespace(docs_dir=str(tmp_path / "no"), target_repo=None))[2] == 2
    assert (
        cpo._resolve_dirs(
            SimpleNamespace(docs_dir=str(docs), target_repo=str(tmp_path / "no-repo"))
        )[2]
        == 2
    )
    d, t, err = cpo._resolve_dirs(SimpleNamespace(docs_dir=str(docs), target_repo=None))
    assert err is None and t is None and d == docs
    monkeypatch.setattr("sys.argv", ["check_pipeline_output", str(docs), "--no-write-check"])
    monkeypatch.setattr(cpo, "check_all", lambda *a, **k: [])
    assert cpo.main() == 0


def test_validate_artifacts_require_and_all(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit):
        va.main(["--all", str(tmp_path), "--require", " , , "])
    assert va.main(["--all", str(tmp_path), "--require", "spring_signals"]) == 1
    assert "missing" in capsys.readouterr().err
    (tmp_path / "spring_signals.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "evidence": {},
                "config_key_sets": {},
                "entity_table_map": {},
                "scanner_version": "sv",
                "scanners": ["filesystem"],
            }
        ),
        encoding="utf-8",
    )
    assert va.main(["--all", str(tmp_path), "--require", "spring_signals"]) in (0, 1)


def test_query_artifacts_root_and_dispatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    sig = tmp_path / "spring_signals.json"
    sig.write_text("{}", encoding="utf-8")
    args = SimpleNamespace(
        kind="evidence",
        signals=str(sig),
        facts=None,
        run_dir=None,
        unsafe_no_root=False,
        root=None,
        limit=10,
        bucket=None,
        rule_id=None,
        file_contains=None,
        match_contains=None,
    )
    monkeypatch.delenv("DOC_ENGINE_ROOT", raising=False)
    monkeypatch.delenv("DOC_ENGINE_RUN_DIR", raising=False)
    assert qa._resolve_cli_root(args) == tmp_path.resolve()
    assert qa._resolve_cli_root(SimpleNamespace(unsafe_no_root=True, root=None)) == Path.cwd()
    assert qa._resolve_cli_root(
        SimpleNamespace(unsafe_no_root=False, root=str(tmp_path))
    ) == Path(str(tmp_path))
    monkeypatch.setattr(qa, "run_query", lambda *a, **k: {"items": []})
    assert qa._query_evidence(args, tmp_path)["items"] == []
    assert qa._query_routes(
        SimpleNamespace(
            signals=str(sig), limit=5, path_contains=None, rule_id=None, file_contains=None
        ),
        tmp_path,
    )["items"] == []
    assert qa._query_facts(
        SimpleNamespace(
            facts=str(tmp_path / "f.jsonl"),
            limit=5,
            predicate=None,
            file_contains=None,
            fqcn=None,
            subject_contains=None,
        ),
        tmp_path,
    )["items"] == []
    assert qa._query_entity(
        SimpleNamespace(signals=str(sig), limit=5, class_name=None, table=None, fqcn=None),
        tmp_path,
    )["items"] == []
    assert qa._query_dependents(
        SimpleNamespace(
            signals=str(sig),
            edges=None,
            limit=5,
            target_file=None,
            target_type=None,
            group_id=None,
        ),
        tmp_path,
    )["items"] == []
    assert qa._query_route_trace(
        SimpleNamespace(signals=str(sig), limit=5, path_contains=None, file_contains=None),
        tmp_path,
    )["items"] == []
    with pytest.raises(QueryError, match="unknown kind"):
        qa._execute_kind(SimpleNamespace(kind="nope"), tmp_path)
    monkeypatch.setattr(qa, "_execute_kind", lambda *_a, **_k: {"ok": True})
    assert qa.main(["evidence", "--signals", str(sig)]) == 0
    assert '"ok"' in capsys.readouterr().out
    monkeypatch.setattr(
        qa, "_execute_kind", lambda *_a, **_k: (_ for _ in ()).throw(QueryError("q"))
    )
    assert qa.main(["evidence", "--signals", str(sig)]) == 1
    monkeypatch.setattr(
        qa, "_execute_kind", lambda *_a, **_k: (_ for _ in ()).throw(KeyError("k"))
    )
    assert qa.main(["evidence", "--signals", str(sig)]) == 2


def test_cli_facade_cmds(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[list[str]] = []

    def _fake(argv=None):
        captured.append(list(argv or []))
        return 0

    monkeypatch.setattr("doc_engine.ci.quality_gates.main", _fake)
    assert (
        cli.cmd_quality_gates(
            SimpleNamespace(
                compare_ref="HEAD~1",
                coverage_xml=Path("c.xml"),
                skip_coverage=True,
                no_fail_fast=True,
            )
        )
        == 0
    )
    assert "--skip-coverage" in captured[-1] and "--no-fail-fast" in captured[-1]
    monkeypatch.setattr("doc_engine.ci.coverage_gap_average.main", _fake)
    assert (
        cli.cmd_coverage_gap_average(
            SimpleNamespace(
                coverage_xml=Path("c.xml"),
                floor=90.0,
                worst=5,
                markdown=True,
                append_github_summary=True,
            )
        )
        == 0
    )
    assert "--markdown" in captured[-1]
    monkeypatch.setattr("doc_engine.ci.complexipy_ratchet.main", _fake)
    assert cli.cmd_complexipy_ratchet(SimpleNamespace(baseline=Path("b.json"), update=True)) == 0
    assert "--update" in captured[-1]
    monkeypatch.setattr("doc_engine.ci.size_ratchet.main", _fake)
    assert cli.cmd_size_ratchet(SimpleNamespace(baseline=None, update=False)) == 0
