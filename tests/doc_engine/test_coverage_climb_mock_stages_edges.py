"""Coverage climb: mock_stages edges; Q2 witness mutmut_slice on mock_stages."""

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
    assert ms._try_keep_citation_row({"file": "", "line": 1}, str(tmp_path), "api", cache) is None
    assert ms._normalize_match_text(None, "api") == "api"
    assert "`" not in ms._normalize_match_text("a `b`\nc", "api")


def test_file_line_count_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "locked.java"
    target.write_text("x\n", encoding="utf-8")
    real_open = open

    def open_denied(path, *args, **kwargs):  # noqa: ANN001
        if str(path).endswith("locked.java"):
            raise OSError("locked")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", open_denied)
    assert ms._file_line_count(str(tmp_path), "locked.java", {}) == 0


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
    nested = tmp_path / "pkg"
    nested.mkdir()
    (nested / "a.java").write_text("// TODO a\n", encoding="utf-8")
    (nested / "b.java").write_text("// FIXME b\n", encoding="utf-8")
    assert len(ms._collect_todo_hits_under(str(tmp_path), cap=1)) == 1


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
    assert not any("n1" in line and "n3" in line for line in merged)
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
    assert ms._first_pool_citation(pool, ["api_surface"]) == pool["api_surface"][0]

    body: list[str] = []
    tags = {"evidenced": 0, "confirmed": 0, "unknown": 0}
    ms._append_interview_section(body, confirmed_ids={"a"}, today="2026-08-09", tag_totals=tags)
    assert tags["confirmed"] == 1
    ms._append_interview_section(body, confirmed_ids=set(), today="2026-08-09", tag_totals=tags)
    assert tags["unknown"] >= 1


def _ctrl_pool(tmp_path: Path) -> dict:
    src = tmp_path / "Ctrl.java"
    src.write_text("class Ctrl {}\n", encoding="utf-8")
    signals = {
        "evidence": {
            "api_surface": [
                {"file": "Ctrl.java", "line": 1, "match": "@RestController"},
                {"file": "missing.java", "line": 1, "match": "gone"},
            ],
            "security": [{"file": "Ctrl.java", "line": 0, "match": "bad"}],
        }
    }
    return ms.load_citations(signals, str(tmp_path))


def test_load_citations_and_pick(tmp_path: Path) -> None:
    pool = _ctrl_pool(tmp_path)
    assert pool["api_surface"] and not pool["security"]
    picked = ms.pick(pool, ["api_surface", "security"], limit=2)
    assert picked and picked[0][0] == "api_surface"


def test_mock_file_summaries_and_architecture(tmp_path: Path) -> None:
    pool = _ctrl_pool(tmp_path)
    logs: list[str] = []
    groups = {"groups": [{"id": 1, "files": ["Ctrl.java"]}]}
    edges = {"groups": {"1": {"outbound": [{"to": "x"}], "same_package_outside": []}}}
    summary = ms.mock_file_summaries(str(tmp_path), groups, pool, edges, logs.append)
    assert "file summaries" in summary
    assert (tmp_path / "summaries.json").is_file()
    arch = ms.mock_architecture(str(tmp_path), groups, pool, logs.append)
    assert "architecture_merged" in arch
    assert (tmp_path / "architecture_merged.md").is_file()


def test_mock_docs_todo_and_empty(tmp_path: Path) -> None:
    pool = _ctrl_pool(tmp_path)
    logs: list[str] = []
    (tmp_path / "README.md").write_text("# hi\n", encoding="utf-8")
    assert ms.find_existing_readme(str(tmp_path)) == "README.md"
    docs_dir = tmp_path / "docs"
    answers = [
        {"id": "integrations.external-consumers", "status": "answered"},
        {"id": "ops.skip", "status": "skipped"},
    ]
    todos = [{"file": "Ctrl.java", "line": 1, "marker": "TODO", "text": "fix"}]
    detail = ms.mock_docs(
        str(docs_dir), pool, todos, answers, "2026-08-09", "README.md", logs.append
    )
    assert "docs" in detail
    assert (docs_dir / "known_limitations.md").is_file()
    kl = (docs_dir / "known_limitations.md").read_text(encoding="utf-8")
    assert "TODO" in kl
    empty_detail = ms.mock_docs(
        str(tmp_path / "docs2"), {}, [], [], "2026-08-09", None, logs.append
    )
    assert "docs" in empty_detail
    kl2 = (tmp_path / "docs2" / "known_limitations.md").read_text(encoding="utf-8")
    assert "No TODO" in kl2


def test_mock_gap_and_interview_writes(tmp_path: Path) -> None:
    pool = _ctrl_pool(tmp_path)
    logs: list[str] = []
    todos = [{"file": "Ctrl.java", "line": 1, "marker": "TODO", "text": "fix"}]
    gap = ms.mock_gap_and_interview(str(tmp_path), pool, todos, "2026-08-09", logs.append)
    assert "gap question" in gap
    assert (tmp_path / "gap_questions.json").is_file()
    assert (tmp_path / "interview_answers.json").is_file()


def test_node_id_and_group_architecture_fallback(tmp_path: Path) -> None:
    seen: set[str] = set()
    assert ms._node_id("a/Foo.java", seen) == "Foo_java"
    assert ms._node_id("b/Foo.java", seen) == "Foo_java_2"
    assert ms._spring_role_for_signals([("unknown_bucket", 1, "x")]) == "other"
    plain = {"groups": [{"id": 9, "files": ["plain.java", "other.java"]}]}
    (tmp_path / "plain.java").write_text("class P {}\n", encoding="utf-8")
    (tmp_path / "other.java").write_text("class O {}\n", encoding="utf-8")
    fallback = ms._group_architecture_files(plain["groups"][0], interesting=set())
    assert fallback == ["plain.java", "other.java"]
