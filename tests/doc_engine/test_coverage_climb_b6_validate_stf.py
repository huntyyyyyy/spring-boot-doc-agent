"""Coverage climb B6: validate_artifacts + stf scoring/validators edges.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.validate_artifacts,
stf.eval.scoring, stf.validators.lint_tasks — asserts bite envelope QueryError,
require KeyError, validation failures, empty-ratio scores, and lint mutators.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import pytest

from doc_engine.query.load import QueryError
from doc_engine.tools import validate_artifacts as va
from stf.eval.scoring import (
    estimate_main_context_peak,
    load_answer_key,
    score_decompose,
)
from stf.validators.lint_tasks import (
    LintResult,
    lint_summary,
    lint_tasks_document,
    mutate_tasks,
)
from tests.stf.conftest import build_minimal_valid_spec, build_minimal_valid_tasks

pytestmark = pytest.mark.domain_climb_sensor


def test_validate_envelope_query_error_and_require_keyerror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "env.json"
    path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        "doc_engine.query.load.load_json",
        mock.Mock(side_effect=QueryError("bad envelope")),
    )
    assert va.main(["--envelope", "query_result", str(path)]) == 1
    assert "bad envelope" in capsys.readouterr().err

    with mock.patch.object(
        va, "missing_required_artifacts", side_effect=KeyError("unknown key")
    ):
        assert va.main(["--all", str(tmp_path), "--require", "nope"]) == 2
    assert "unknown key" in capsys.readouterr().err


def test_validate_all_and_single_failure_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    from doc_engine.pipeline.validation import ArtifactValidationError

    monkeypatch.setattr(
        va,
        "require_stage0_siblings",
        mock.Mock(
            side_effect=ArtifactValidationError(
                "spring_signals", tmp_path / "x.json", "siblings missing"
            )
        ),
    )
    assert va.main(["--all", str(tmp_path)]) == 1
    assert "siblings missing" in capsys.readouterr().err

    monkeypatch.setattr(va, "require_stage0_siblings", lambda *_a, **_k: None)
    monkeypatch.setattr(va, "require_gap_probe_artifact", lambda *_a, **_k: None)
    monkeypatch.setattr(va, "validate_artifacts_in_dir", lambda *_a, **_k: [])
    assert va.main(["--all", str(tmp_path)]) == 1
    assert "no known artifact" in capsys.readouterr().err

    bad = tmp_path / "signals.json"
    bad.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        va,
        "validate_artifact_file",
        mock.Mock(
            side_effect=ArtifactValidationError("spring_signals", bad, "shape bad")
        ),
    )
    assert va.main(["spring_signals", str(bad)]) == 1
    assert "shape bad" in capsys.readouterr().err


def test_scoring_empty_ratios_and_load_key(tmp_path: Path) -> None:
    key = {
        "required_task_titles_substrings": [],
        "required_inventory_ids": [],
        "must_surface_conflict": None,
        "threshold": 0.5,
    }
    result = score_decompose(
        build_minimal_valid_tasks(), key, spec=build_minimal_valid_spec()
    )
    assert result["scores"]["G1"] == 1.0
    assert result["scores"]["G2"] == 1.0
    assert result["scores"]["C1"] == 1.0
    assert result["pass"] is True

    conflict_key = {**key, "must_surface_conflict": "never-in-blob-xyz"}
    conflicted = score_decompose(
        build_minimal_valid_tasks(), conflict_key, spec=build_minimal_valid_spec()
    )
    assert conflicted["scores"]["C1"] == 0.0

    path = tmp_path / "answer.json"
    path.write_text(json.dumps(key), encoding="utf-8")
    assert load_answer_key(path)["threshold"] == 0.5
    empty = estimate_main_context_peak([])
    assert empty["peak_main_ctx"] == 0
    assert empty["events"] == 0


def _assert_mutant_fails(tasks, mode: str, spec, *, root: Path | None = None) -> None:
    mutant = mutate_tasks(tasks, mode)
    assert any(r.level == "FAIL" for r in lint_tasks_document(mutant, spec, root=root))


def test_lint_anchors_and_summary(tmp_path: Path) -> None:
    tasks = build_minimal_valid_tasks()
    spec = build_minimal_valid_spec()
    anchor = tmp_path / "src" / "doc_engine" / "query"
    anchor.mkdir(parents=True)
    (anchor / "load.py").write_text("# probe\n", encoding="utf-8")
    results = lint_tasks_document(tasks, spec, root=tmp_path)
    summary = lint_summary(results)
    assert summary["ok"] is True
    assert LintResult(level="PASS", name="x").to_dict()["level"] == "PASS"


def test_lint_named_mutators_fail(tmp_path: Path) -> None:
    tasks = build_minimal_valid_tasks()
    spec = build_minimal_valid_spec()
    for mode in (
        "bad-dep",
        "no-phase",
        "bad-inventory",
        "no-acceptance",
        "bad-blocker",
        "cycle",
    ):
        _assert_mutant_fails(tasks, mode, spec, root=tmp_path)
    with pytest.raises(ValueError, match="unknown mutate mode"):
        mutate_tasks(tasks, "not-a-mode")
