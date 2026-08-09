"""Bounds-safe arc snippet helpers for mock Stage summaries."""

from doc_engine.pipeline import mock_stages as ms

import pytest

pytestmark = pytest.mark.domain_pipeline

def test_cross_group_arc_snippets_handles_missing_keys():
    assert ms._cross_group_arc_snippets({}) == []

def test_cross_group_arc_snippets_handles_non_list_values():
    assert ms._cross_group_arc_snippets({"outbound": "nope", "same_package_outside": 1}) == []

def test_cross_group_arc_snippets_caps_at_five():
    edges = {
        "outbound": [{"i": n} for n in range(8)],
        "same_package_outside": [{"j": n} for n in range(8)],
    }
    snippets = ms._cross_group_arc_snippets(edges)
    assert len(snippets) == 10
    assert '"i": 0' in snippets[0]
    assert '"j": 4' in snippets[-1]
