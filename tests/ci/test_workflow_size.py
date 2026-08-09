"""Coverage for doc_engine.ci.workflow_size (E-CI C3/C4)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.workflow_size import (
    CI_CALLER_MAX_LOC,
    WORKFLOW_HARD_LOC,
    check_no_python_heredocs,
    check_workflow_loc,
    line_count,
)

pytestmark = pytest.mark.domain_ci_meta


def test_line_count_reads_file(tmp_path: Path) -> None:
    path = tmp_path / "w.yml"
    path.write_text("a\nb\nc\n", encoding="utf-8")
    assert line_count(path) == 3


def test_ci_yml_over_caller_max_is_hard(tmp_path: Path) -> None:
    (tmp_path / "ci.yml").write_text(
        "\n".join(f"# {i}" for i in range(CI_CALLER_MAX_LOC + 1)) + "\n",
        encoding="utf-8",
    )
    hard, advisory = check_workflow_loc(tmp_path, label_fn=lambda p: p.name)
    assert hard and "ci.yml" in hard[0]
    assert advisory == []


def test_any_workflow_over_hard_max(tmp_path: Path) -> None:
    (tmp_path / "other.yml").write_text(
        "\n".join(f"# {i}" for i in range(WORKFLOW_HARD_LOC + 1)) + "\n",
        encoding="utf-8",
    )
    hard, _ = check_workflow_loc(tmp_path, label_fn=lambda p: p.name)
    assert any("other.yml" in e for e in hard)


def test_advisory_band_between_225_and_300(tmp_path: Path) -> None:
    (tmp_path / "mid.yml").write_text(
        "\n".join(f"# {i}" for i in range(230)) + "\n",
        encoding="utf-8",
    )
    hard, advisory = check_workflow_loc(tmp_path, label_fn=lambda p: p.name)
    assert hard == []
    assert any("mid.yml" in a for a in advisory)


def test_heredoc_marker_detected(tmp_path: Path) -> None:
    (tmp_path / "h.yml").write_text("run: |\n  python3 - <<'PY'\n  PY\n", encoding="utf-8")
    errors = check_no_python_heredocs(tmp_path, label_fn=lambda p: p.name)
    assert errors and "h.yml" in errors[0]
