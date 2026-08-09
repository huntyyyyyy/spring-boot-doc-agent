"""RefactorBench-style structure characterization for AstGrepBackend façade."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from doc_engine.scanning import _scanner_astgrep as facade
from doc_engine.scanning._scanner_astgrep import AstGrepBackend, chunk_paths_for_argv

pytestmark = pytest.mark.domain_stage0

REPO = Path(__file__).resolve().parents[2]

class AstGrepStructureTest:
    def test_facade_exports_backend_and_chunk_helper(self) -> None:
        assert facade.AstGrepBackend is AstGrepBackend
        assert facade.chunk_paths_for_argv is chunk_paths_for_argv

    def test_version_hash_paths_include_astgrep_package(self) -> None:
        paths = AstGrepBackend._version_hash_paths()
        joined = "\n".join(paths)
        assert "_scanner_astgrep.py" in joined
        assert str(Path("astgrep") / "argv.py") in joined or "/astgrep/argv.py" in joined
        assert any(p.endswith("astgrep/invoke.py") or p.endswith("astgrep\\invoke.py") for p in paths)

    def test_facade_module_still_defines_astgrep_backend_class(self) -> None:
        source = Path(inspect.getfile(facade)).read_text(encoding="utf-8")
        tree = ast.parse(source)
        names = {
            node.name
            for node in tree.body
            if isinstance(node, ast.ClassDef)
        }
        assert "AstGrepBackend" in names

    def test_poke_surface_attrs_present(self) -> None:
        for attr in (
            "_PATH_LIST_CHAR_LIMIT",
            "subprocess",
            "extract_entity",
            "first_line_match",
            "read_source_lines",
            "RULE_FILE",
        ):
            assert hasattr(facade, attr), attr
