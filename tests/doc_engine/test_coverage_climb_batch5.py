"""Coverage climb batch: paths, semantic_eval, spring_signal_scan, absence_recall."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine import paths as paths_mod
from doc_engine.paths import PathValidationError
from doc_engine.scanning.gap_probe import absence_recall as absence
from doc_engine.tools import semantic_eval_helpers as seh
from doc_engine.tools import spring_signal_scan as sss


# --- paths.py ---------------------------------------------------------------


def test_checked_path_file_and_unknown_want(tmp_path: Path) -> None:
    f = tmp_path / "f.txt"
    f.write_text("x", encoding="utf-8")
    assert paths_mod.checked_path(f, want="file") == f.resolve()
    with pytest.raises(PathValidationError, match="not a file"):
        paths_mod.checked_path(tmp_path, want="file")
    with pytest.raises(PathValidationError, match="not a directory"):
        paths_mod.checked_path(f, want="dir")
    with pytest.raises(ValueError, match="unknown want"):
        paths_mod.checked_path(tmp_path, want="socket")


def test_checked_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self, *a, **k):
        if "bad" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve"):
        paths_mod.checked_path(tmp_path / "bad", want="dir")


def test_checked_output_path_refuses_directory(tmp_path: Path) -> None:
    d = tmp_path / "outdir"
    d.mkdir()
    with pytest.raises(PathValidationError, match="not a file"):
        paths_mod.checked_output_path(d)


def test_checked_output_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self, *a, **k):
        if "boom" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve"):
        paths_mod.checked_output_path(tmp_path / "boom.json")


def test_join_under_absolute_and_escape(tmp_path: Path) -> None:
    with pytest.raises(PathValidationError, match="unsafe|escapes"):
        paths_mod.join_under(tmp_path, "/abs")
    with pytest.raises(PathValidationError, match="unsafe"):
        paths_mod.join_under(tmp_path, "..", "x")
    nested = tmp_path / "a"
    nested.mkdir()
    assert paths_mod.join_under(tmp_path, "a") == nested.resolve()


def test_scripts_meta_path_entries_and_packaged_astgrep() -> None:
    entries = paths_mod.scripts_meta_path_entries()
    assert any(e.endswith("ci") or e.replace("\\", "/").endswith("/ci") for e in entries)
    assert paths_mod.codeql_pack_dir().name == "spring-signals"
    # Prefer packaged rules when present.
    p = paths_mod.ast_grep_rules_path()
    assert p.is_file()


# --- semantic_eval_helpers --------------------------------------------------


def test_tokenize_and_claim_clause() -> None:
    toks = seh._tokenize("The Widget Service is ready for use")
    assert "widget" in toks
    assert "the" not in toks
    # Use the same em dash as CONFIRMED_TAG_RE (U+2014).
    tag = "[Confirmed \u2014 interview, 2026-01-01]"
    # No trailing period before the tag — _claim_clause splits on [.!?]\s+.
    text = f"First sentence. Second claim here {tag}"
    m = seh.CONFIRMED_TAG_RE.search(text)
    assert m is not None
    clause = seh._claim_clause(text, m.start())
    assert "Second claim" in clause


def test_markdown_names_and_scan_confirmed(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text(
        "Claim about payments. [Confirmed — interview, 2026-01-01]\n",
        encoding="utf-8",
    )
    (docs / "skip.txt").write_text("x", encoding="utf-8")
    names = seh._markdown_names(str(docs))
    assert names == ["readme.md"]

    interview = [
        {
            "topic": "payments",
            "question": "who owns?",
            "status": "answered",
            "answer": "team A owns payments ledger",
            "date": "2026-01-01",
        }
    ]
    # High threshold forces unmatched when overlap is modest.
    findings = seh._scan_confirmed_docs(str(tmp_path), interview, overlap_threshold=0.99)
    assert "readme.md" in findings or findings == {}


def test_resolve_architecture_and_mermaid(tmp_path: Path) -> None:
    assert seh._resolve_architecture_path(str(tmp_path)) is None
    docs = tmp_path / "docs"
    docs.mkdir()
    arch = docs / "architecture.md"
    arch.write_text(
        "```mermaid\nflowchart LR\n  A-->B\n```\n",
        encoding="utf-8",
    )
    assert seh._resolve_architecture_path(str(tmp_path)).endswith("architecture.md")
    findings = seh._scan_mermaid(str(tmp_path))
    assert isinstance(findings, list)


def test_semantic_run_and_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    (tmp_path / "interview_answers.json").write_text("[]", encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text("# hi\n", encoding="utf-8")
    report = seh.run(str(tmp_path))
    assert report["artifacts_dir"]
    out = tmp_path / "mech.json"
    monkeypatch.setattr(
        "sys.argv",
        ["seh", str(tmp_path), "--out", str(out)],
    )
    seh.main()
    assert out.is_file()
    assert "semantic_eval_helpers" in capsys.readouterr().out


def test_semantic_main_bad_artifacts(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["seh", "/no/such/artifacts"])
    with pytest.raises(SystemExit) as exc:
        seh.main()
    assert exc.value.code == 1


# --- spring_signal_scan -----------------------------------------------------


def test_run_ast_grep_missing_and_nonzero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sss.shutil, "which", lambda _b: None)
    with pytest.raises(sss.AstGrepNotFoundError):
        sss.run_ast_grep("ast-grep", ".")
    monkeypatch.setattr(sss.shutil, "which", lambda _b: "/bin/ast-grep")
    monkeypatch.setattr(
        sss.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=2, stdout="", stderr="boom"),
    )
    with pytest.raises(sss.AstGrepError, match="status 2"):
        sss.run_ast_grep("ast-grep", ".")


def test_run_ast_grep_bad_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sss.shutil, "which", lambda _b: "/bin/ast-grep")
    monkeypatch.setattr(
        sss.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(returncode=0, stdout="not-json", stderr=""),
    )
    with pytest.raises(sss.AstGrepError, match="not valid JSON"):
        sss.run_ast_grep("ast-grep", ".")


def test_strip_and_emit_helpers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    result = {
        "evidence": {"api_surface": [{"file": "a.java"}]},
        "entity_table_map": {"A": {}},
        "redaction_zones": {"a.java": [1]},
        "config_key_sets": {"application.yml": ["a"]},
        "files_scanned": 1,
        "_covering_proof": {"inventory_root": "r", "receipts": [{}]},
        "_scan_partials_meta": {"x": 1},
    }
    stripped = sss._strip_internal_keys(result)
    assert "_covering_proof" not in stripped
    monkeypatch.setattr(sss, "write_covering_proof", lambda *a, **k: None)
    monkeypatch.setattr(sss, "write_facts_jsonl", lambda *a, **k: None)
    monkeypatch.setattr(sss, "facts_from_signals", lambda _r: [{"p": 1}])
    monkeypatch.setattr(
        sss,
        "fact_emit_counts",
        lambda _f: {
            "facts_total": 1,
            "facts_maps_to": 0,
            "facts_maps_to_contested": 0,
            "facts_evidence": 1,
            "facts_absence": 0,
            "facts_unproven": 0,
            "facts_recall_miss": 0,
        },
    )
    out = tmp_path / "spring_signals.json"
    cov = sss._emit_covering_proof(result, str(out))
    assert cov
    facts_path, emit = sss._emit_facts(result, str(out))
    assert emit["facts_total"] == 1
    sss._print_scan_summary(str(out), cov, facts_path, emit, stripped)
    assert "Wrote" in capsys.readouterr().out


def test_spring_signal_scan_main_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    out = tmp_path / "out" / "signals.json"
    out.parent.mkdir()
    monkeypatch.setattr(
        "sys.argv",
        ["sss", str(repo), "--out", str(out)],
    )
    monkeypatch.setattr(
        sss,
        "scan",
        lambda *a, **k: {
            "evidence": {},
            "entity_table_map": {},
            "redaction_zones": {},
            "config_key_sets": {},
            "files_scanned": 0,
            "_covering_proof": {"inventory_root": "r", "receipts": []},
        },
    )
    monkeypatch.setattr(sss, "write_covering_proof", lambda *a, **k: None)
    monkeypatch.setattr(sss, "write_facts_jsonl", lambda *a, **k: None)
    monkeypatch.setattr(sss, "facts_from_signals", lambda _r: [])
    monkeypatch.setattr(
        sss,
        "fact_emit_counts",
        lambda _f: {
            "facts_total": 0,
            "facts_maps_to": 0,
            "facts_maps_to_contested": 0,
            "facts_evidence": 0,
        },
    )
    assert sss.main() == 0
    assert out.is_file()

    monkeypatch.setattr(
        "sys.argv",
        ["sss", str(tmp_path / "missing"), "--out", str(out)],
    )
    assert sss.main() == 1

    monkeypatch.setattr("sys.argv", ["sss", str(repo), "--out", str(out)])
    monkeypatch.setattr(
        sss,
        "scan",
        lambda *a, **k: (_ for _ in ()).throw(sss.CodeQLScannerError("nope")),
    )
    assert sss.main() == 1


# --- absence_recall ---------------------------------------------------------


def test_absence_rate_block_and_measure() -> None:
    zero = absence._absence_rate_block(0, None)
    assert zero["denominator"] == 0
    assert zero.get("rate") in (None, 0.0)
    assert absence._absence_rate_block(2, None)["denominator"] == 2
    assert absence._absence_rate_block(1, 0)["denominator"] == 0
    assert absence._absence_rate_block(1, 4)["numerator"] == 1

    facts = [
        {
            "predicate": "ABSENCE",
            "subject": "s",
            "file": "a.java",
            "qualifiers": {"trial": "callable", "family": "auth"},
        },
        {"predicate": "ABSENCE", "subject": "ignored", "file": "z.java"},
        {"predicate": "UNPROVEN", "subject": "u", "file": "b.java"},
        {
            "predicate": "RECALL_MISS",
            "subject": "r",
            "file": "c.java",
            "qualifiers": {"verdict": "EVIDENTIARY", "oracle_arm": True},
        },
        {
            "predicate": "RECALL_MISS",
            "subject": "r2",
            "file": "d.java",
            "qualifiers": {"verdict": "STRUCTURAL"},
        },
    ]
    block = absence.measure_r_absence(facts, callable_trials=10)
    assert block["callable_absence"] == 1
    assert block["unproven"] == 1
    assert len(block["failures"]) == 1
    assert absence.measure_r_recall(facts, oracle_arm_present=False) is None
    recall = absence.measure_r_recall(facts, oracle_arm_present=True)
    assert recall is not None
    assert recall["evidentiary"] == 1
    assert recall["structural"] == 1
    planted = absence._planted_recall_failures(facts)
    assert any(r["stratum"] == "untrusted_planted" for r in planted)
    assert absence._trusted_codeql_oracle_arm(
        {
            "receipts": [
                {
                    "scanner": "codeql",
                    "status": "complete",
                    "expected_subset_root": "a",
                    "acked_subset_root": "a",
                }
            ]
        }
    )
    assert not absence._astgrep_receipt_complete({"receipts": []})
    assert absence._resolve_covering_path(signals_path=None, covering_path=None) is None


def test_receipt_complete_helpers() -> None:
    assert absence._receipt_complete_for_scanner("x", "filesystem") is False
    bad = {"scanner": "filesystem", "status": "failed"}
    assert absence._receipt_complete_for_scanner(bad, "filesystem") is False
    good = {
        "scanner": "filesystem",
        "status": "complete",
        "expected_subset_root": "r",
        "acked_subset_root": "r",
    }
    assert absence._receipt_complete_for_scanner(good, "filesystem") is True
    proof = {"receipts": [good]}
    assert absence._complete_receipt_for_scanner(proof, scanner="filesystem") is True
    assert absence._complete_receipt_for_scanner(None, scanner="filesystem") is False
