"""Coverage climb B8: dependents dedupe / filter continue edges.

Q2 adequacy witness: mutmut_slice on doc_engine.query.handlers.dependents —
asserts bite seen-key early return and continue filters on targets/type.
"""

from __future__ import annotations

from typing import Any

import pytest

from doc_engine.query.handlers import dependents as dep

pytestmark = pytest.mark.domain_climb_sensor


def test_append_import_arc_dedupes() -> None:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    kwargs = dict(
        src="A.java",
        dst="B.java",
        qualified="com.B",
        confidence="high",
        is_static=False,
        want_file=None,
    )
    dep._append_import_arc(rows, seen, **kwargs)
    dep._append_import_arc(rows, seen, **kwargs)
    assert len(rows) == 1


def test_append_resolved_and_unresolved_continues() -> None:
    rows: list[dict[str, Any]] = []
    seen: set = set()
    dep._append_resolved_targets(
        rows,
        seen,
        src="A.java",
        qualified="com.X",
        is_static=False,
        targets=["B.java", "C.java"],
        confidence="low",
        want_file="Z.java",
        want_type=None,
    )
    # want_file filter should continue past non-matching destinations.
    assert rows == []

    dep._collect_arcs_for_source(
        rows,
        seen,
        src="A.java",
        entries=[("com.missing.Thing", False)],
        decl_files={},
        stem_index={},
        want_file=None,
        want_type=None,
    )
    assert rows == []
