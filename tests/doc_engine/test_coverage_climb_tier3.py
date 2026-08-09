"""Third-tier coverage climb: validation, site builder, generative, live_gates."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.pipeline import live_gates as live_gates_mod
from doc_engine.pipeline import validation as val_mod
from doc_engine.pipeline.compliance import GateRecord
from doc_engine.pipeline.local_runner_phases import generative as gen_mod
from doc_engine.pipeline.local_runner_phases.state import LocalRunState
from doc_engine.tools import build_docs_site as site_mod

pytestmark = pytest.mark.domain_climb_sensor

def test_load_jsonl_skips_blank_and_rejects_bad(tmp_path: Path) -> None:
    path = tmp_path / "facts.jsonl"
    path.write_text('\n{"a":1}\n\n{not-json\n', encoding="utf-8")
    with pytest.raises(val_mod.ArtifactValidationError, match="invalid JSON"):
        val_mod.load_jsonl_objects(path)

def test_validate_artifact_data_unknown_and_bad() -> None:
    with pytest.raises(KeyError, match="unknown artifact"):
        val_mod.validate_artifact_data("nope", {})
    with pytest.raises(val_mod.ArtifactValidationError):
        val_mod.validate_artifact_data("spring_signals", {"not": "valid"})

def test_missing_required_unknown_key(tmp_path: Path) -> None:
    with pytest.raises(KeyError, match="unknown artifact"):
        val_mod.missing_required_artifacts(tmp_path, ["not_a_real_artifact"])

def test_gap_report_helpers(tmp_path: Path) -> None:
    bad = tmp_path / "gap.json"
    bad.write_text("[]", encoding="utf-8")
    with pytest.raises(val_mod.ArtifactValidationError, match="JSON object"):
        val_mod._load_gap_report_object(bad)
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    with pytest.raises(val_mod.ArtifactValidationError):
        val_mod._load_gap_report_object(broken)

    path = tmp_path / "g.json"
    data = {"schema_version": "wrong"}
    with pytest.raises(val_mod.ArtifactValidationError, match="schema_version"):
        val_mod._require_gap_schema_version(path, data, "expected")
    with pytest.raises(val_mod.ArtifactValidationError, match="verified"):
        val_mod._require_gap_covering_verified(path, {"s1_covering": {"verified": False}})
    with pytest.raises(val_mod.ArtifactValidationError, match="uncertainty"):
        val_mod._require_gap_uncertainty(path, {})

def test_require_gap_probe_missing_report(tmp_path: Path) -> None:
    from doc_engine.pipeline.artifacts import ARTIFACT_FILENAMES

    (tmp_path / ARTIFACT_FILENAMES["spring_signals"]).write_text("{}", encoding="utf-8")
    with pytest.raises(val_mod.ArtifactValidationError, match="gap probe"):
        val_mod.require_gap_probe_artifact(tmp_path)

def test_build_docs_site_helpers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert site_mod._find_mkdocs_yml().name == "mkdocs.yml"
    docs = tmp_path / "docs"
    docs.mkdir()
    with pytest.raises(RuntimeError, match="no recognized"):
        site_mod._write_mkdocs_config(tmp_path, docs, "Site", None)
    (docs / "readme.md").write_text("# R\n", encoding="utf-8")
    work = tmp_path / "work"
    work.mkdir()
    site_mod._write_mkdocs_config(work, docs, "Site", "https://example.com/repo")
    text = (work / "mkdocs.yml").read_text(encoding="utf-8")
    assert "repo_url: https://example.com/repo" in text
    assert "Readme" in text

    site_mod._copy_docs(docs, work)
    assert (work / "docs" / "index.md").is_file()

    # Placeholder index when readme absent
    work2 = tmp_path / "work2"
    work2.mkdir()
    docs2 = tmp_path / "docs2"
    docs2.mkdir()
    (docs2 / "architecture.md").write_text("# A\n", encoding="utf-8")
    site_mod._copy_docs(docs2, work2)
    assert (work2 / "docs" / "index.md").read_text(encoding="utf-8").startswith("# Doc")

    monkeypatch.setattr(
        site_mod.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr="boom"),
    )
    with pytest.raises(RuntimeError, match="mkdocs build failed"):
        site_mod._run_mkdocs(work, tmp_path / "out")

def test_build_docs_site_main_missing_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["build_docs_site", "--docs-dir", str(tmp_path / "missing"), "--out-dir", str(tmp_path / "out")],
    )
    assert site_mod.main() == 1
    assert "docs-dir not found" in capsys.readouterr().err

def test_note_existing_readme_and_generative_abort(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "README.md").write_text("hi", encoding="utf-8")
    log = MagicMock()
    state = SimpleNamespace(repo_path=str(tmp_path), log=log)
    gen_mod._note_existing_readme(state)  # type: ignore[arg-type]
    assert log.call_count >= 1

    from doc_engine.pipeline.compliance import ComplianceProfile
    from doc_engine.pipeline.local_runner_phases.support import Log, Runner

    run_log = Log(tmp_path / "run.log")
    try:
        runner = Runner(run_log, keep_going=False)
        runner.aborted = True
        full = LocalRunState(
            args=SimpleNamespace(),
            repo_path=str(tmp_path),
            out_dir=str(tmp_path / "out"),
            docs_dir=str(tmp_path / "docs"),
            today="2026-08-08",
            profile=ComplianceProfile.CERTIFIED,
            allow_mock=True,
            skip_signal_scan=False,
            strict_citations_effective=False,
            log=run_log,
            runner=runner,
            py="python",
            manifest=str(tmp_path / "m.json"),
            signals_path=str(tmp_path / "s.json"),
            preflight_path=str(tmp_path / "p.json"),
            pipeline_ctx=object(),  # type: ignore[arg-type]
            mock_executor=object(),  # type: ignore[arg-type]
            generative_specs=[],
        )
        monkeypatch.setattr(
            gen_mod,
            "PipelineRunner",
            lambda **_k: SimpleNamespace(run=lambda _ctx: []),
        )
        monkeypatch.setattr(
            gen_mod,
            "_write_certification_and_finish",
            lambda *a, **k: 9,
        )
        assert gen_mod.phase_generative(full) == 9
    finally:
        run_log.close()

def test_fail_missing_live_gates_records_failures() -> None:
    gates: list[GateRecord] = []
    failures: list[str] = []
    live_gates_mod._fail_missing_live_gates(gates, failures)
    assert failures
    assert all(g.status == "fail" for g in gates)

def test_live_gates_main_defaults_docs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    captured = {}

    def _fake(**kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(live_gates_mod, "run_live_gates", _fake)
    rc = live_gates_mod.main(
        ["--out-dir", str(tmp_path / "out"), "--target-repo", str(tmp_path / "repo")]
    )
    assert rc == 0
    assert captured["docs_dir"].endswith("docs")
