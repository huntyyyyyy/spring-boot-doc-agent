"""Coverage climb: spring_drift_check CLI and fast-path stubs."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from doc_engine.tools import capacity_preflight as cap
from doc_engine.tools import spring_drift_check as drift

def test_drift_require_path_and_print(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit):
        drift._require_path(str(tmp_path / "missing"), expect_dir=True)
    d = tmp_path / "d"
    d.mkdir()
    drift._require_path(str(d), expect_dir=True)
    f = tmp_path / "f.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(SystemExit):
        drift._require_path(str(f), expect_dir=True)
    drift._require_path(str(f), expect_dir=False)
    report = {
        "file_signatures_baseline": {"source": "spring_signals.json"},
        "citations_checked": 1,
        "status_counts": {"unchanged": 1},
        "file_summary": {
            "unchanged": ["a"],
            "changed": [],
            "deleted": [],
            "added": [],
        },
    }
    drift._print_drift_summary(str(tmp_path / "out.json"), report)
    assert "Citations checked" in capsys.readouterr().out


def test_unchanged_fast_path_and_process_stubs() -> None:
    signals = {
        "evidence": {"sec": [{"file": "a.java", "line": 1, "rule_id": "r"}]},
        "entity_table_map": {},
    }
    rows = drift._unchanged_fast_path_results(signals)
    assert rows and rows[0]["status"] == "unchanged"
    results: list = []
    drift._append_uniform_status(
        results,
        [("evidence.sec", {"file": "a.java", "line": 1})],
        drift.STATUS_FILE_DELETED,
        detail="gone",
    )
    assert results[0]["status"] == drift.STATUS_FILE_DELETED
