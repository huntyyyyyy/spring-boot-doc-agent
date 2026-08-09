"""Coverage climb B7: query providers contested / redaction / cap edges.

Q2 adequacy witness: mutmut_slice on doc_engine.query.providers — asserts bite
non-Mapping qualifiers, FactsProvider limit break, DependentsProvider emit,
non-mapping hits, zone shapes, and non-str redaction path.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.query import providers as prov

pytestmark = pytest.mark.domain_climb_sensor


def test_facts_row_contested_non_mapping_quals() -> None:
    facts = prov.FactsProvider()
    assert facts._row_contested({"qualifiers": ["not", "a", "map"]}) is False


def test_facts_provider_breaks_at_limit(tmp_path: Path) -> None:
    rows = [
        {"predicate": "MAPS_TO", "object": f"o{i}", "file": f"f{i}.java"}
        for i in range(10)
    ]
    out = prov.FactsProvider().provide(
        "q", signals={}, facts_rows=rows, run_dir=tmp_path, limit=2
    )
    assert len(out) == 4  # limit * 2
    assert all(item["provider"] == "facts" for item in out)


def test_dependents_provider_emits_rows(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        prov.dependents,
        "query_dependents",
        lambda _signals: [{"from": "A.java", "via": "import"}, {"from": "B.java"}],
    )
    out = prov.DependentsProvider().provide(
        "q", signals={}, facts_rows=[], run_dir=tmp_path, limit=5
    )
    assert len(out) == 2
    assert out[0]["path"] == "A.java"
    assert out[0]["match"] == "import"


def test_hit_row_and_zone_normalization_shapes() -> None:
    assert prov._hit_row("a.java", "plain") == {
        "file": "a.java",
        "reason": "plain",
    }
    assert prov._rows_from_zone_hits("z.java", "not-a-list") == [
        {"file": "z.java", "reason": "redaction_zone"}
    ]
    assert prov._normalize_redaction_zones(42) == []
    assert prov._redaction_path({"file": 99}) is None
