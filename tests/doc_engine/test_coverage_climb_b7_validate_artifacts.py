"""Coverage climb B7: validate_artifacts envelope / argv error edges.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.validate_artifacts —
asserts bite non-dict envelope rejection, ok path print, and missing argv
parser.error.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.tools import validate_artifacts as va

pytestmark = pytest.mark.domain_climb_sensor


def test_handle_envelope_non_dict_and_ok(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps([1, 2]), encoding="utf-8")

    monkeypatch.setattr(
        "doc_engine.query.load.load_json", lambda _path: [1, 2]
    )
    assert va._handle_envelope("context_packet", str(bad)) == 1
    assert "JSON object" in capsys.readouterr().err

    payload = {
        "schema_version": 1,
        "request": "q",
        "items": [],
        "budget": {"tokens": 10, "used": 0},
    }
    monkeypatch.setattr(
        "doc_engine.query.load.load_json", lambda _path: payload
    )
    monkeypatch.setattr(
        "doc_engine.query.schema_check.validate_envelope",
        lambda kind, data: None,
    )
    assert va._handle_envelope("context_packet", str(tmp_path / "good.json")) == 0
    assert "ok:" in capsys.readouterr().out


def test_dispatch_cli_missing_artifact_path() -> None:
    parser = va._build_parser()
    args = parser.parse_args([])
    with pytest.raises(SystemExit):
        va._dispatch_cli(parser, args)
