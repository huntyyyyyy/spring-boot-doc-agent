"""Coverage climb B9: evidence / entity / route_trace filter edges.

Q2 adequacy witness: mutmut_slice on query handlers evidence/entity/route_trace —
asserts bite file-filter False, non-list/non-map empties, candidates-not-list,
and match path_contains keep.
"""

from __future__ import annotations

import pytest

from doc_engine.query.handlers import entity, evidence, route_trace

pytestmark = pytest.mark.domain_climb_sensor

def test_evidence_filter_false_and_empty_shapes() -> None:
    row = {"file": "a.java", "rule_id": "r", "match": "x"}
    assert (
        evidence._row_passes(
            row, rule_id=None, file_contains="nope", match_contains=None
        )
        is False
    )
    assert (
        evidence._filter_bucket(
            {"security": "not-a-list"},
            "security",
            rule_id=None,
            file_contains=None,
            match_contains=None,
        )
        == []
    )
    assert evidence.query_evidence({"evidence": ["bad"]}) == []

def test_entity_candidates_not_list_and_bad_map() -> None:
    assert (
        entity._candidate_field_matches(
            {"table": "t", "candidates": "bad"}, "fqcn", "x"
        )
        is False
    )
    assert entity.query_entity({"entity_table_map": ["bad"]}) == []

def test_route_trace_match_path_contains() -> None:
    raw = {"rule_id": "other", "match": "/api/orders", "file": "C.java"}
    assert route_trace._mapping_row_kept(raw, "/api/") is True
    assert route_trace._mapping_row_kept(raw, "/nope") is False
