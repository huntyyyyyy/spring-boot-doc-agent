"""Coverage climb batch B3: domain catalog / classify / shards / markers / ABI.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.test_domain_catalog,
test_domain_classify, test_path_shards, test_domain_markers_check,
emit_abi_matrix — asserts bite KeyError / orphan / unknown-marker / floor /
__main__ edges (not line-touch padding).
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path
from unittest import mock

import pytest

from doc_engine.ci import emit_abi_matrix
from doc_engine.ci import test_domain_catalog as catalog
from doc_engine.ci import test_domain_classify as classify
from doc_engine.ci import test_domain_markers_check as check_mod
from doc_engine.ci import test_path_shards as shards
from doc_engine.ci.test_domain_inventory import DocEngineDomainInventory

pytestmark = pytest.mark.domain_climb_sensor


def _seed(repo: Path, rel: str, body: str) -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_catalog_require_and_marker_lines() -> None:
    with pytest.raises(KeyError, match="unknown test domain"):
        catalog.require_domain("domain_does_not_exist")
    lines = catalog.pytest_marker_lines()
    assert any(line.startswith("domain_climb_sensor:") for line in lines)
    assert catalog.require_domain("domain_ci_meta").parallel_default == "parallel"


def test_classify_unreachable_rule_and_non_domain_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(classify, "CLASSIFICATION_RULES", ())
    orphan = _seed(tmp_path, "tests/x/test_z.py", "def test_z():\n    pass\n")
    with pytest.raises(RuntimeError, match="no classification rule"):
        classify.classify_test_path(tmp_path, orphan)

    plain = "import pytest\npytestmark = some_other_mark\ndef test_x():\n pass\n"
    assert classify.declared_domain_markers(plain) == []
    call_non_attr = (
        "import pytest\n"
        "pytestmark = mystery()\n"
        "def test_x():\n    pass\n"
    )
    assert classify.declared_domain_markers(call_non_attr) == []
    mixed = (
        "import pytest\n"
        "pytestmark = [pytest.mark.domain_ci_meta, mystery(), "
        "pytest.mark.domain_schemas()]\n"
        "def test_x():\n    pass\n"
    )
    assert set(classify.declared_domain_markers(mixed)) >= {
        "domain_ci_meta",
        "domain_schemas",
    }


def test_path_shards_pycache_empty_tests_and_orphan(tmp_path: Path) -> None:
    assert shards.orphan_parallel_modules(tmp_path) == []
    ci = tmp_path / "tests" / "ci"
    cache = ci / "__pycache__"
    cache.mkdir(parents=True)
    (cache / "test_ignored.py").write_text(
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_i():\n pass\n",
        encoding="utf-8",
    )
    assert shards.discover_collection_dirs(tmp_path) == []

    _seed(
        tmp_path,
        "tests/ci/test_gate.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_g():\n pass\n",
    )
    assert shards.discover_collection_dirs(tmp_path)
    # fixtures/ is classified parallel but outside DISCOVERY_ROOTS → orphan.
    _seed(
        tmp_path,
        "tests/fixtures/test_stray.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_s():\n pass\n",
    )
    orphans = shards.orphan_parallel_modules(tmp_path)
    assert any("tests/fixtures/test_stray.py" in item for item in orphans)


def test_markers_check_unknown_floor_truncation_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    unknown = _seed(
        tmp_path,
        "tests/ci/test_unknown.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_u():\n pass\n",
    )
    with mock.patch.object(
        check_mod, "declared_domain_markers", return_value=["domain_fake"]
    ):
        issues = check_mod.evaluate_module(
            tmp_path, unknown, require_classifier_match=False
        )
    assert any("unknown marker" in item for item in issues)

    # Known marker + require_classifier_match=False skips classifier compare.
    aligned = _seed(
        tmp_path,
        "tests/ci/test_aligned.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_a():\n pass\n",
    )
    assert (
        check_mod.evaluate_module(
            tmp_path, aligned, require_classifier_match=False
        )
        == []
    )

    _seed(
        tmp_path,
        "tests/ci/test_ok.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_o():\n pass\n",
    )
    fake_inv = DocEngineDomainInventory(
        floor=98.7,
        total=10,
        meeting=(),
        debt=tuple(Path(f"d{i}.py") for i in range(3)),
    )
    monkeypatch.setattr(
        check_mod, "build_doc_engine_inventory", lambda _repo: fake_inv
    )
    monkeypatch.setattr(check_mod, "domain_path_matrix", lambda _repo: ())
    monkeypatch.setattr(
        check_mod,
        "orphan_parallel_modules",
        lambda _repo: ["tests/fixtures/test_orphan.py"],
    )
    monkeypatch.setattr(check_mod, "evaluate_module", lambda *a, **k: [])
    assert check_mod.run_check(tmp_path, require_classifier_match=True) == 1
    err = capsys.readouterr().err
    assert "domain_path_matrix produced zero" in err
    assert "meeting rate" in err
    assert "test_orphan" in err

    # Truncation branch: >50 issues printed with ellipsis.
    flooded = [f"issue-{i}" for i in range(55)]
    monkeypatch.setattr(check_mod, "evaluate_module", lambda *a, **k: flooded)
    assert check_mod.run_check(tmp_path, require_classifier_match=True) == 1
    assert "more" in capsys.readouterr().err

    assert check_mod.main(["--repo-root", str(tmp_path)]) == 1



def test_emit_abi_matrix_github_output_and_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "gh_out"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    _seed(
        tmp_path,
        "tests/ci/test_gate.py",
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_g():\n pass\n",
    )
    matrix = emit_abi_matrix.build_abi_matrix(tmp_path, ("3.11",))
    emit_abi_matrix.write_github_output(matrix)
    text = out.read_text(encoding="utf-8")
    assert "matrix<<EOF" in text and "3.11" in text
    assert emit_abi_matrix.main(
        ["--python-versions", "3.11", "--repo-root", str(tmp_path)]
    ) == 0
    monkeypatch.setattr(
        sys,
        "argv",
        ["emit_abi_matrix", "--python-versions", "3.11", "--repo-root", str(tmp_path)],
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("doc_engine.ci.emit_abi_matrix", run_name="__main__")
    assert exc.value.code == 0
