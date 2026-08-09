"""Coverage climb: pipeline validators, secrets, check_pipeline_output, validate_artifacts."""

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

pytestmark = pytest.mark.domain_climb_sensor

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
