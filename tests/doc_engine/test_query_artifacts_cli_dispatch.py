"""Query artifacts CLI dispatch edges."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.envelope import QUERY_RESULT_SCHEMA_VERSION, apply_limit
from doc_engine.query.handlers import dependents, entity, evidence, facts, routes
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError, load_json, load_jsonl
from doc_engine.query.registry import get_query_handler, run_query
from doc_engine.real_fixture import real_artifacts_dir
FIXTURE_SIGNALS = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "fixtures"
    / "spring_signals"
)
from tests.support.query_artifacts.factories import _signals_doc, _facts_rows

def test_real_artifacts_evidence_stays_capped() -> None:
    """Deviation: OCS-scale references dump uncapped through query.

    Prefer the dedicated suite ``test_query_ocs_real_world.py``; this keeps a
    thin cap check in the unit module when the artifact lane is present.
    """
    from doc_engine.paths import repo_root
    from doc_engine.real_fixture import real_artifacts_dir

    art = real_artifacts_dir(prefer_default=True)
    assert art is not None
    if not art.is_absolute():
        art = repo_root() / art
    signals = art / "spring_signals.json"
    if not signals.is_file():
        pytest.skip("spring_signals.json missing — run regen_real_repo_artifacts.py")
    result = run_query(
        "evidence",
        signals_path=signals,
        root=art,
        bucket="references",
        limit=25,
    )
    assert len(result["rows"]) <= 25
    assert result["truncated"] is True or len(result["rows"]) < 25


def test_unknown_evidence_bucket_raises() -> None:
    """Deviation: H3 - typo bucket returns empty success."""
    signals = _signals_doc()
    with pytest.raises(QueryError, match="unknown evidence bucket"):
        evidence.query_evidence(signals, bucket="secuirty")


def test_unknown_facts_predicate_raises() -> None:
    """Deviation: H3 - typo predicate returns empty success."""
    rows = _facts_rows()
    with pytest.raises(QueryError, match="unknown facts predicate"):
        facts.query_facts(rows, predicate="MAPS_TOO")


def test_redaction_provider_dict_zones_produce_risks() -> None:
    """Deviation: H2 - production {rel_path: [hits]} yields empty risks."""
    from doc_engine.query.providers import RedactionProvider

    signals = {
        "redaction_zones": {
            "application.yml": [
                {"line": 12, "heuristic": "key-name:password"},
                {"line": 40, "heuristic": "aws_access_key_id"},
            ]
        }
    }
    items = RedactionProvider().provide(
        "secrets",
        signals=signals,
        facts_rows=[],
        run_dir=Path("."),
        limit=10,
    )
    assert len(items) == 2
    assert items[0]["path"] == "application.yml"
    assert "password" in (items[0]["match"] or "")


def test_estimate_tokens_counts_full_emission() -> None:
    """Deviation: C2 - estimate_tokens ignores payload while emission includes it."""
    from doc_engine.query.rank import estimate_tokens, to_emission_item

    fat = {
        "provider": "evidence",
        "path": "src/A.java",
        "line": 1,
        "match": "hit",
        "bucket": "security",
        "reason": "x",
        "score": 1.0,
        "payload": {"blob": "y" * 4000},
    }
    emission = to_emission_item(fat)
    assert "payload" not in emission
    assert "row_ref" in emission
    assert estimate_tokens(emission) == len(json.dumps(emission, ensure_ascii=False)) // 4
    assert estimate_tokens({**emission, "payload": fat["payload"]}) > estimate_tokens(emission)


def test_assume_indexed_returns_unknown() -> None:
    """Deviation: M1 - AssumeIndexed always claims fresh_indexed."""
    from doc_engine.query.freshness import AssumeIndexed, label_item_path

    assert label_item_path(AssumeIndexed(), "does/not/exist.java") == "unknown"


def test_partition_budget_never_overshoots() -> None:
    """Deviation: N1 - max(1,...) primary+finding+risk exceeds small budgets."""
    from doc_engine.query.rank import partition_budget

    for budget in range(0, 12):
        primary, finding, risk = partition_budget(budget)
        assert primary + finding + risk == budget
        assert primary >= 0
        assert finding >= 0
        assert risk >= 0


def test_apply_nested_cap_truncates_guards() -> None:
    """Deviation: H1 - nested guards unbounded; truncated lies."""
    from doc_engine.query.envelope import apply_nested_cap

    row = {"file": "A.java", "guards": [{"i": i} for i in range(200)]}
    capped, truncated = apply_nested_cap([row], max_list=50)
    assert truncated is True
    assert len(capped[0]["guards"]) == 50
