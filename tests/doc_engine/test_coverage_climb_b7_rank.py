"""Coverage climb B7: query.rank empty / truncate / emission edges.

Q2 adequacy witness: mutmut_slice on doc_engine.query.rank — asserts bite empty
bucket priority, empty-request overlap, nested list truncate, apply_nested_cap_value,
freshness/contested copy, and non-mapping payload skip.
"""

from __future__ import annotations

import pytest

from doc_engine.query import rank as rank_mod

pytestmark = pytest.mark.domain_climb_sensor


def test_bucket_priority_empty_and_overlap_empty_request() -> None:
    assert rank_mod.lookup_bucket_priority_score(None) == 0.4
    assert rank_mod.lookup_bucket_priority_score("") == 0.4
    assert rank_mod.measure_token_overlap_ratio(set(), {"a"}) == 0.0


def test_nested_list_truncate_and_cap_value() -> None:
    big = list(range(60))
    capped, truncated = rank_mod.truncate_nested_lists_that_exceed_cap(
        big, max_list_length=10
    )
    assert truncated is True
    assert len(capped) == 10
    assert rank_mod.apply_nested_cap_value({"guards": big}, max_list=5)["guards"] == list(
        range(5)
    )


def test_emission_copies_freshness_contested_skips_bad_payload() -> None:
    item = {
        "provider": "facts",
        "path": "a.java",
        "line": 1,
        "match": "x",
        "bucket": "facts",
        "reason": "r",
        "score": 0.9,
        "freshness": "stale",
        "contested": True,
        "payload": "not-a-map",
    }
    emission = rank_mod.replace_bulky_payload_with_row_ref_pointer(item)
    assert emission["freshness"] == "stale"
    assert emission["contested"] is True
    assert "nested_truncated" not in emission
