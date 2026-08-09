"""Coverage climb B6: domain markers_check success + empty-suite edges.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.test_domain_markers_check —
asserts bite missing/multi marker evaluate paths, empty module discovery,
classifier mismatch, and green OK prints (not padding).
"""

from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

from doc_engine.ci import test_domain_catalog as catalog
from doc_engine.ci import test_domain_markers_check as check_mod
from doc_engine.ci.test_domain_inventory import DocEngineDomainInventory

pytestmark = pytest.mark.domain_climb_sensor


def _seed(repo: Path, rel: str, body: str) -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_evaluate_missing_multi_and_mismatch(tmp_path: Path) -> None:
    missing = _seed(tmp_path, "tests/ci/test_missing.py", "def test_m():\n pass\n")
    assert any(
        "missing domain" in item
        for item in check_mod.evaluate_module(
            tmp_path, missing, require_classifier_match=False
        )
    )

    multi = _seed(
        tmp_path,
        "tests/ci/test_multi.py",
        "import pytest\n"
        "pytestmark = [pytest.mark.domain_ci_meta, pytest.mark.domain_schemas]\n"
        "def test_m():\n pass\n",
    )
    assert any(
        "multiple domain" in item
        for item in check_mod.evaluate_module(
            tmp_path, multi, require_classifier_match=False
        )
    )

    mismatched = _seed(
        tmp_path,
        "tests/ci/test_mismatch.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_m():\n pass\n",
    )
    with mock.patch.object(check_mod, "classify_test_path", return_value="domain_schemas"):
        issues = check_mod.evaluate_module(
            tmp_path, mismatched, require_classifier_match=True
        )
    assert any("classifier expects" in item for item in issues)


def test_run_check_empty_and_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check_mod, "iter_test_modules", lambda _repo: [])
    assert check_mod.run_check(tmp_path) == 2
    assert "no tests" in capsys.readouterr().err

    module = _seed(
        tmp_path,
        "tests/ci/test_ok.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_o():\n pass\n",
    )
    inv = DocEngineDomainInventory(
        floor=98.7,
        total=1,
        meeting=(module,),
        debt=(),
    )
    monkeypatch.setattr(check_mod, "iter_test_modules", lambda _repo: [module])
    monkeypatch.setattr(check_mod, "evaluate_module", lambda *a, **k: [])
    monkeypatch.setattr(check_mod, "orphan_parallel_modules", lambda _repo: [])
    monkeypatch.setattr(
        check_mod,
        "domain_path_matrix",
        lambda _repo: [SimpleGroup()],
    )
    monkeypatch.setattr(check_mod, "build_doc_engine_inventory", lambda _repo: inv)
    assert check_mod.run_check(tmp_path, require_classifier_match=True) == 0
    out = capsys.readouterr().out
    assert "OK:" in out
    assert "classifier-aligned" in out

    assert catalog.known_markers()
    assert catalog.parallel_shard_markers()
    assert "domain_" in catalog.serial_expression()


class SimpleGroup:
    paths = (Path("tests/ci"),)


def test_markers_check_main_optional_flags(tmp_path: Path) -> None:
    # Empty suite → exit 2 via main() (covers argv + repo_root default path).
    assert check_mod.main(["--repo-root", str(tmp_path), "--no-require-classifier-match"]) == 2
