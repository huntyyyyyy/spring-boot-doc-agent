"""Unit tests for ``doc_engine.ci.complexipy_ratchet``."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.ci import complexipy_ratchet as ratchet


def test_count_offenders_parses_plain_lines(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ratchet, "require_venv_script", lambda _n: "complexipy")
    stdout = (
        "src/a.py:foo 3\n"
        "src/a.py:bar 9\n"
        "not-a-count line\n"
        "src/b.py:baz 6\n"
    )
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *a, **k: SimpleNamespace(stdout=stdout, returncode=1),
    )
    assert ratchet.count_offenders() == 2


def test_load_baseline_schema_and_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ratchet, "checked_path_under_repo", lambda p: Path(p))
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema_version": 99, "offender_count": 0}), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        ratchet.load_baseline(bad)
    assert exc.value.code == 2

    good = tmp_path / "good.json"
    ratchet.write_baseline(good, 3)
    data = ratchet.load_baseline(good)
    assert data["offender_count"] == 3
    assert data["schema_version"] == ratchet.SCHEMA_VERSION


def test_main_update_and_ratchet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ratchet, "count_offenders", lambda: 2)
    monkeypatch.setattr(ratchet, "checked_path_under_repo", lambda p: Path(p))
    baseline = tmp_path / "baseline.json"

    assert ratchet.main(["--baseline", str(baseline), "--update"]) == 0
    assert baseline.is_file()

    monkeypatch.setattr(ratchet, "count_offenders", lambda: 2)
    assert ratchet.main(["--baseline", str(baseline)]) == 0

    monkeypatch.setattr(ratchet, "count_offenders", lambda: 1)
    assert ratchet.main(["--baseline", str(baseline)]) == 0  # drop is ok (note only)

    monkeypatch.setattr(ratchet, "count_offenders", lambda: 5)
    assert ratchet.main(["--baseline", str(baseline)]) == 1  # rise fails


def test_main_missing_baseline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ratchet, "count_offenders", lambda: 0)
    missing = tmp_path / "absent.json"
    assert ratchet.main(["--baseline", str(missing)]) == 2
