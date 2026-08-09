"""Coverage climb: domain classify + path shards hermetic edges.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.test_domain_classify /
test_path_shards / emit_abi_matrix (assert discriminative edges, not line touch).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci import test_domain_classify as classify
from doc_engine.ci import test_path_shards as shards
from doc_engine.ci.test_domain_rules import (
    DirPrefixRule,
    FallbackUnclassified,
    FilenameContainsRule,
    FilenamePrefixRule,
)

pytestmark = pytest.mark.domain_climb_sensor


def test_iter_modules_and_declared_markers(tmp_path: Path) -> None:
    assert classify.iter_test_modules(tmp_path) == []
    tests = tmp_path / "tests" / "ci"
    tests.mkdir(parents=True)
    (tests / "__pycache__").mkdir()
    (tests / "__pycache__" / "test_skip.py").write_text("pass\n", encoding="utf-8")
    good = tests / "test_gate.py"
    good.write_text(
        "import pytest\n\npytestmark = pytest.mark.domain_ci_meta\n\ndef test_x():\n    pass\n",
        encoding="utf-8",
    )
    modules = classify.iter_test_modules(tmp_path)
    assert good.resolve() in [m.resolve() for m in modules]
    assert all("__pycache__" not in m.parts for m in modules)

    assert classify.declared_domain_markers("not python {{{") == []
    multi = (
        "import pytest\n"
        "pytestmark = [pytest.mark.domain_ci_meta, pytest.mark.domain_schemas]\n"
    )
    assert set(classify.declared_domain_markers(multi)) >= {
        "domain_ci_meta",
        "domain_schemas",
    }
    call_form = "import pytest\npytestmark = pytest.mark.domain_ci_meta()\n"
    assert "domain_ci_meta" in classify.declared_domain_markers(call_form)
    assert classify.declared_domain_markers("x = 1\n") == []


def test_ensure_pytestmark_inject_edges() -> None:
    with pytest.raises(KeyError):
        classify.ensure_pytestmark("def test_x():\n    pass\n", "domain_nope")
    empty = classify.ensure_pytestmark("", "domain_ci_meta")
    assert "import pytest" in empty and "domain_ci_meta" in empty
    with_doc = classify.ensure_pytestmark(
        '"""Doc."""\n\ndef test_x():\n    pass\n', "domain_ci_meta"
    )
    assert with_doc.index('"""Doc."""') < with_doc.index("pytestmark")
    already = (
        "import pytest\n\npytestmark = pytest.mark.domain_schemas\n\ndef test_x():\n    pass\n"
    )
    updated = classify.ensure_pytestmark(already, "domain_ci_meta")
    assert "domain_ci_meta" in updated
    assert "domain_schemas" not in updated.split("pytestmark")[1].split("\n")[0]

    bad = "def (\n"
    assert classify._ast_insert_index(bad, bad.splitlines(True)) == 0
    shebang = "#!/usr/bin/env python3\n\ndef test_x():\n    pass\n"
    lines = shebang.splitlines(keepends=True)
    assert classify._fallback_insert_index(lines) >= 1


def test_classification_rules_match() -> None:
    assert (
        DirPrefixRule(prefix="tests/ci", marker="domain_ci_meta").match(
            "tests/ci/test_a.py", "test_a.py"
        )
        == "domain_ci_meta"
    )
    assert (
        DirPrefixRule(prefix="tests/ci", marker="domain_ci_meta").match(
            "tests/other/test_a.py", "test_a.py"
        )
        is None
    )
    assert (
        FilenamePrefixRule(
            name_prefix="test_coverage_climb_",
            marker="domain_climb_sensor",
            under="tests/doc_engine",
        ).match("tests/doc_engine/test_coverage_climb_x.py", "test_coverage_climb_x.py")
        == "domain_climb_sensor"
    )
    assert (
        FilenamePrefixRule(
            name_prefix="test_coverage_climb_",
            marker="domain_climb_sensor",
            under="tests/doc_engine",
        ).match("tests/ci/test_coverage_climb_x.py", "test_coverage_climb_x.py")
        is None
    )
    assert (
        FilenameContainsRule(needle="schema", marker="domain_schemas").match(
            "tests/doc_engine/test_artifact_schemas.py", "test_artifact_schemas.py"
        )
        == "domain_schemas"
    )
    assert FallbackUnclassified().match("tests/x/test_y.py", "test_y.py") == (
        "domain_unclassified"
    )


def test_path_shards_discovery_and_orphans(tmp_path: Path) -> None:
    assert shards.discover_collection_dirs(tmp_path) == []
    ci = tmp_path / "tests" / "ci"
    ci.mkdir(parents=True)
    (ci / "support").mkdir()
    (ci / "support" / "test_helper.py").write_text(
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_h():\n pass\n",
        encoding="utf-8",
    )
    (ci / "test_gate.py").write_text(
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_g():\n pass\n",
        encoding="utf-8",
    )
    found = shards.discover_collection_dirs(tmp_path)
    assert any(p.name == "ci" for p in found)
    assert not any("support" in p.parts for p in found)

    matrix = shards.domain_path_matrix(tmp_path)
    assert any(g.marker == "domain_ci_meta" for g in matrix)
    assert shards.paths_for_marker(tmp_path, "domain_ci_meta")
    assert shards.paths_for_marker(tmp_path, "domain_stage0") == ()
    assert shards.parallel_path_shards(tmp_path) == matrix
    rows = shards.github_matrix_include(tmp_path)
    assert rows and "paths" in rows[0]
    assert shards.orphan_parallel_modules(tmp_path) == []


def test_emit_abi_matrix_empty_and_no_github_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from doc_engine.ci import emit_abi_matrix

    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    emit_abi_matrix.write_github_output({"include": [{"id": "x"}]})
    with pytest.raises(SystemExit):
        emit_abi_matrix.build_abi_matrix(tmp_path, ("3.10",))

    seeded = tmp_path / "tests" / "ci"
    seeded.mkdir(parents=True)
    (seeded / "test_gate.py").write_text(
        "import pytest\npytestmark = pytest.mark.domain_ci_meta\ndef test_g():\n pass\n",
        encoding="utf-8",
    )
    matrix = emit_abi_matrix.build_abi_matrix(tmp_path, ("3.10", "3.12"))
    assert len(matrix["include"]) == 2
    assert emit_abi_matrix.main(["--python-versions", "3.11", "--repo-root", str(tmp_path)]) == 0

    import runpy
    import sys

    monkeypatch.setattr(
        sys,
        "argv",
        ["emit_abi_matrix", "--python-versions", "3.10", "--repo-root", str(tmp_path)],
    )
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("doc_engine.ci.emit_abi_matrix", run_name="__main__")
    assert exc.value.code == 0
