"""Coverage climb B8: resolve_lineage import-miss / clean / None query.

Q2 adequacy witness: mutmut_slice on doc_engine.scanning._resolve_lineage —
asserts bite ImportError flag, clean table without prefix, and None query skip.
"""

from __future__ import annotations

import builtins
import importlib
import sys

import pytest

from doc_engine.scanning import _resolve_lineage as rl

pytestmark = pytest.mark.domain_climb_sensor


def test_clean_table_name_without_prefix() -> None:
    assert rl._clean_table_name("orders") == "orders"
    assert rl._clean_table_name(rl.SQLLINEAGE_DEFAULT_SCHEMA_PREFIX + "t") == "t"


def test_annotate_skips_none_query() -> None:
    entry: dict = {"query_kind": "native"}
    rl.SpringLineageResolver()._annotate_query_entry(
        entry, entity_table_map={}, sql_dialect="ansi"
    )
    assert "lineage" not in entry


def test_sqllineage_import_error_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    real_import = builtins.__import__

    def fake_import(name: str, *a, **k):
        if name.startswith("sqllineage"):
            raise ImportError("no sqllineage")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    sys.modules.pop("doc_engine.scanning._resolve_lineage", None)
    sys.modules.pop("sqllineage", None)
    sys.modules.pop("sqllineage.runner", None)
    reloaded = importlib.import_module("doc_engine.scanning._resolve_lineage")
    assert reloaded._SQLLINEAGE_AVAILABLE is False
