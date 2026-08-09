"""Coverage climb B8: pipeline_validators missing-keys / evidence / __main__.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.pipeline_validators —
asserts bite gap/review missing-keys returns, non-dict evidence item, and
__main__ SystemExit.
"""

from __future__ import annotations

import runpy
import sys

import pytest

from doc_engine.tools import pipeline_validators as pv

pytestmark = pytest.mark.domain_climb_sensor


def test_check_gap_question_missing_keys() -> None:
    problems = pv._check_gap_question(0, {"topic": "t"}, [])
    assert problems
    assert "missing keys" in problems[0][1]


def test_evidence_item_non_dict() -> None:
    problems = pv._evidence_item_problems(3, "not-a-dict")
    assert problems
    assert "must be an object" in problems[0]


def test_validate_review_finding_missing_keys() -> None:
    problems = pv._validate_review_finding(1, {"lens": "a"})
    assert problems
    assert "missing keys" in problems[0][1]


def test_validators_main_module_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["pipeline_validators", "/no/such/dir"])
    with pytest.raises(SystemExit):
        runpy.run_module("doc_engine.tools.pipeline_validators", run_name="__main__")
