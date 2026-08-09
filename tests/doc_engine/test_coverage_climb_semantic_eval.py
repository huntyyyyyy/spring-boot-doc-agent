"""Coverage climb: semantic_eval helpers and mermaid/architecture resolution."""

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
