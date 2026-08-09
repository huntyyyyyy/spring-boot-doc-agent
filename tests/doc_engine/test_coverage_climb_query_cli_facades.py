"""Coverage climb: query_artifacts dispatch and CLI gate facades."""

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
