"""Query artifacts facts/entity filters."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.envelope import QUERY_RESULT_SCHEMA_VERSION, apply_limit
from doc_engine.query.handlers import dependents, entity, evidence, facts, routes
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError, load_json, load_jsonl
from doc_engine.query.registry import get_query_handler, run_query
from doc_engine.real_fixture import real_artifacts_dir

pytestmark = pytest.mark.domain_pipeline

FIXTURE_SIGNALS = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "fixtures"
    / "spring_signals"
)
from tests.support.query_artifacts.factories import _signals_doc, _facts_rows

def test_load_jsonl_skips_blank_but_rejects_truncated_line(tmp_path: Path) -> None:
    """Deviation: truncated JSONL line silently dropped (chaos/fault injection)."""
    p = tmp_path / "facts.jsonl"
    p.write_text('{"predicate":"X","subject":"a","object":"b","qualifiers":{},"file":"f","line":1,"rule_id":"r","scanner":"s"}\n{bad\n', encoding="utf-8")
    with pytest.raises(QueryError):
        load_jsonl(p, root=tmp_path)

def test_path_outside_root_refused(tmp_path: Path) -> None:
    """Deviation: path escape / traversal accepted (untrusted artifact paths)."""
    root = tmp_path / "run"
    root.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    with pytest.raises(QueryPathError):
        load_json(outside, root=root)

def test_symlink_escaping_root_refused(tmp_path: Path) -> None:
    """Deviation: symlink into escape path accepted as in-tree artifact."""
    root = tmp_path / "run"
    root.mkdir()
    outside = tmp_path / "secret.json"
    outside.write_text('{"ok": true}', encoding="utf-8")
    link = root / "signals.json"
    try:
        os.symlink(outside, link)
    except OSError as exc:
        pytest.skip(f"symlink creation failed: {exc}")
    # resolve() follows the link → outside root
    with pytest.raises(QueryPathError):
        load_json(link, root=root)

def test_cli_evidence_exit_zero_and_truncated(tmp_path: Path) -> None:
    """Deviation: CLI dumps uncapped JSON or non-zero on valid input."""
    sig = tmp_path / "spring_signals.json"
    sig.write_text(json.dumps(_signals_doc()), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "doc_engine.tools.query_artifacts",
            "evidence",
            "--signals",
            str(sig),
            "--bucket",
            "api_surface",
            "--limit",
            "1",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["truncated"] is True
    assert len(payload["rows"]) == 1

def test_cli_missing_signals_nonzero(tmp_path: Path) -> None:
    """Deviation: missing --signals exits 0 with empty envelope."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "doc_engine.tools.query_artifacts",
            "evidence",
            "--signals",
            str(tmp_path / "missing.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0

def test_doc_engine_query_facade(tmp_path: Path) -> None:
    """Deviation: doc-engine query subcommand missing from public facade."""
    sig = tmp_path / "spring_signals.json"
    sig.write_text(json.dumps(_signals_doc()), encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "doc_engine.cli",
            "query",
            "entity",
            "--signals",
            str(sig),
            "--class",
            "User",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["kind"] == "entity"
    assert payload["rows"][0]["class_name"] == "User"

def test_unknown_kind_raises() -> None:
    """Deviation: unknown kind silently no-ops."""
    with pytest.raises(KeyError):
        get_query_handler("not-a-kind")
