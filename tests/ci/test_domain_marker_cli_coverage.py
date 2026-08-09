"""Coverage climb: domain marker apply/check CLI + ABI matrix emission."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from doc_engine.ci import emit_abi_matrix
from doc_engine.ci import test_domain_markers_apply as apply_mod
from doc_engine.ci import test_domain_markers_check as check_mod

pytestmark = pytest.mark.domain_ci_meta


def _seed_test_module(repo: Path, rel: str, body: str) -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_apply_markers_dry_run_and_write(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo = tmp_path
    path = _seed_test_module(
        repo,
        "tests/ci/test_example_gate.py",
        '"""Ex."""\n\ndef test_ok():\n    assert True\n',
    )
    changed, total = apply_mod.apply_markers(repo, dry_run=True)
    assert total == 1
    assert changed == 1
    assert "pytestmark" not in path.read_text(encoding="utf-8")
    out = capsys.readouterr().out
    assert "dry-run" in out
    assert "domain_ci_meta" in out

    changed, total = apply_mod.apply_markers(repo, dry_run=False)
    assert changed == 1
    text = path.read_text(encoding="utf-8")
    assert "pytestmark = pytest.mark.domain_ci_meta" in text
    changed_again, _total = apply_mod.apply_markers(repo, dry_run=False)
    assert changed_again == 0


def test_apply_markers_main_dry_run(tmp_path: Path) -> None:
    _seed_test_module(
        tmp_path,
        "tests/doc_engine/test_artifact_schemas.py",
        "def test_x():\n    pass\n",
    )
    assert apply_mod.main(["--repo-root", str(tmp_path), "--dry-run"]) == 0


def test_run_check_passes_aligned_tree(tmp_path: Path) -> None:
    path = _seed_test_module(
        tmp_path,
        "tests/ci/test_aligned.py",
        "def test_x():\n    pass\n",
    )
    apply_mod.apply_markers(tmp_path, dry_run=False)
    assert "domain_ci_meta" in path.read_text(encoding="utf-8")
    assert check_mod.run_check(tmp_path, require_classifier_match=True) == 0


def test_run_check_fails_missing_and_mismatch(tmp_path: Path) -> None:
    _seed_test_module(tmp_path, "tests/ci/test_missing.py", "def test_x():\n    pass\n")
    assert check_mod.run_check(tmp_path, require_classifier_match=False) == 1
    path = _seed_test_module(
        tmp_path,
        "tests/ci/test_wrong.py",
        "import pytest\n\npytestmark = pytest.mark.domain_schemas\n\n"
        "def test_x():\n    pass\n",
    )
    issues = check_mod.evaluate_module(
        tmp_path, path, require_classifier_match=True
    )
    assert any("classifier expects" in item for item in issues)


def test_run_check_multiple_markers_reported(tmp_path: Path) -> None:
    multi = _seed_test_module(
        tmp_path,
        "tests/ci/test_multi.py",
        "import pytest\n"
        "pytestmark = [pytest.mark.domain_ci_meta, pytest.mark.domain_schemas]\n"
        "def test_x():\n    pass\n",
    )
    issues = check_mod.evaluate_module(
        tmp_path, multi, require_classifier_match=False
    )
    assert any("multiple domain markers" in item for item in issues)


def test_check_main_no_modules_returns_2(tmp_path: Path) -> None:
    assert check_mod.main(["--repo-root", str(tmp_path)]) == 2


def test_emit_abi_matrix_builds_and_writes_github_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Minimal real-shaped tree: one classified module so matrix non-empty.
    # Use the live repo root for discovery — build against workspace.
    from doc_engine.paths import repo_root

    out = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    matrix = emit_abi_matrix.build_abi_matrix(
        repo_root(), ("3.10",)
    )
    assert matrix["include"]
    assert matrix["include"][0]["python-version"] == "3.10"
    emit_abi_matrix.write_github_output(matrix)
    payload = out.read_text(encoding="utf-8")
    assert "matrix<<EOF" in payload
    assert emit_abi_matrix.main(["--python-versions", "3.10", "--repo-root", str(repo_root())]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert "include" in printed
