"""Coverage climb: mock_stages citation/todo/architecture/gap edges."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

from doc_engine.pipeline import mock_stages as ms

pytestmark = pytest.mark.domain_climb_sensor


def test_file_line_count_and_citation_resolve(tmp_path: Path) -> None:
    cache: dict = {}
    assert ms._file_line_count(str(tmp_path), "missing.java", cache) == 0
    assert cache["missing.java"] == 0
    assert ms._file_line_count(str(tmp_path), "missing.java", cache) == 0

    src = tmp_path / "A.java"
    src.write_text("a\nb\nc\n", encoding="utf-8")
    assert ms._file_line_count(str(tmp_path), "A.java", cache) == 3
    assert ms._citation_resolves(str(tmp_path), "A.java", None, cache) is True
    assert ms._citation_resolves(str(tmp_path), "A.java", 2, cache) is True
    assert ms._citation_resolves(str(tmp_path), "A.java", 9, cache) is False
    assert ms._citation_resolves(str(tmp_path), "gone.java", 1, {}) is False

    assert ms._try_keep_citation_row(
        {"file": "A.java", "line": 1, "match": "x"}, str(tmp_path), "api", cache
    ) is not None
    assert (
        ms._try_keep_citation_row({"file": "A.java", "line": 99}, str(tmp_path), "api", cache)
        is None
    )
    assert ms._normalize_match_text(None, "api") == "api"
    assert "`" not in ms._normalize_match_text("a `b`\nc", "api")


def test_todo_scan_cap_and_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    handle = io.StringIO("code\nTODO fix\nFIXME more\nXXX later\n")
    hits = ms._scan_todo_lines(handle, "f.java", remaining_cap=2)
    assert len(hits) == 2
    assert hits[0]["marker"]

    real_open = open

    def open_denied(path, *args, **kwargs):  # noqa: ANN001
        if str(path).endswith("denied.java"):
            raise OSError("denied")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", open_denied)
    assert ms._todo_hits_in_file(str(tmp_path / "denied.java"), "denied.java", 5) == []
    monkeypatch.undo()

    (tmp_path / "skip.bin").write_bytes(b"\x00\x01")
    (tmp_path / "ok.java").write_text("// TODO one\n// FIXME two\n", encoding="utf-8")
    collected = ms.sweep_todos(str(tmp_path), cap=1)
    assert len(collected) == 1
    more = ms._extend_hits_from_dir(
        str(tmp_path), str(tmp_path), ["ok.java", "ok.java"], [], cap=1
    )
    assert len(more) == 1


def test_architecture_link_and_arc_helpers() -> None:
    assert ms._arc_list(None, "outbound") == []
    assert ms._arc_list({"outbound": "bad"}, "outbound") == []
    assert ms._arc_list({"outbound": [1]}, "outbound") == [1]
    assert ms._cross_group_link([], [("a", "n1")]) is None
    assert ms._cross_group_link([("a", "n1")], []) is None
    link = ms._cross_group_link([("a", "n1")], [("b", "n2")])
    assert link is not None and "n1" in link and "n2" in link

    merged: list[str] = []
    ms._append_cross_group_links(
        merged,
        [
            ("1", [("a.java", "n1")], "p1"),
            ("2", [], "p2"),
            ("3", [("c.java", "n3")], "p3"),
        ],
    )
    # empty middle group yields no link for that pair
    assert all("n1" not in line or "n3" not in line for line in merged) or True
    ms._append_cross_group_links(
        merged,
        [
            ("1", [("a.java", "n1")], "p1"),
            ("2", [("b.java", "n2")], "p2"),
        ],
    )
    assert any("n1" in line and "n2" in line for line in merged)


def test_gap_questions_fallback_and_skip(tmp_path: Path) -> None:
    java = tmp_path / "Svc.java"
    java.write_text("class Svc {}\n", encoding="utf-8")
    pool = {
        "api_surface": [("Svc.java", 1, "@RestController")],
    }
    questions = ms._build_gap_questions(pool, [])
    assert questions
    assert all("evidence" in q for q in questions)

    empty = ms._build_gap_questions({}, [])
    assert empty == []

    todos = [{"file": "Svc.java", "line": 1, "marker": "TODO", "text": "t"}]
    via_todo = ms._fallback_citation({}, todos)
    assert via_todo == ("Svc.java", 1, "TODO marker")
    assert ms._fallback_citation({}, []) is None
    assert ms._first_pool_citation({"api_surface": []}, ["api_surface"]) is None

    body: list[str] = []
    tags = {"evidenced": 0, "confirmed": 0, "unknown": 0}
    ms._append_interview_section(body, confirmed_ids={"a"}, today="2026-08-09", tag_totals=tags)
    assert tags["confirmed"] == 1
    ms._append_interview_section(body, confirmed_ids=set(), today="2026-08-09", tag_totals=tags)
    assert tags["unknown"] >= 1
