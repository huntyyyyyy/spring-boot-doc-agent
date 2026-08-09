"""Coverage climb B8: resolve_lineage clean / None query edges.

Q2 adequacy witness: mutmut_slice on doc_engine.scanning._resolve_lineage —
asserts bite clean table without prefix and None query skip (no module reload).
"""

from __future__ import annotations

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
