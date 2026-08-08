"""Tests for doc_engine.core.jsonio."""

from pathlib import Path

import pytest

from doc_engine.core.jsonio import dump_json, load_json


def test_round_trip_dict(tmp_path: Path) -> None:
    path = tmp_path / "payload.json"
    dump_json(path, {"a": 1, "nested": {"b": True}})
    assert load_json(path) == {"a": 1, "nested": {"b": True}}


def test_dump_json_respects_indent(tmp_path: Path) -> None:
    path = tmp_path / "indented.json"
    dump_json(path, {"k": "v"}, indent=1)
    text = path.read_text(encoding="utf-8")
    assert '{\n "k": "v"\n}' == text


def test_load_json_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_json(tmp_path / "missing.json")


def test_load_json_invalid_raises(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_json(path)
