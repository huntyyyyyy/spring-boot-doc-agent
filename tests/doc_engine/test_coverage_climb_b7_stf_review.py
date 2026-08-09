"""Coverage climb B7: stf review epic duplicate + table parse.

Q2 adequacy witness: mutmut_slice on stf.ingest.review epic row path —
asserts bite non-epic continue and duplicate tid skip after first insert.
"""

from __future__ import annotations

import pytest

from stf.ingest import review as rev
from stf.schemas.findings import FindingSeverity

pytestmark = pytest.mark.domain_climb_sensor


def test_sev_helpers_and_empty_claim() -> None:
    assert rev._sev_from_severity_line("**Severity: high") is None
    assert rev._sev_from_raw("unknown-level") is None
    assert rev._sev_from_id("", "body") == FindingSeverity.INFO
    assert rev._first_claim_line("# heading\n| table |\n```\n") == ""
    assert rev._parts_for_dash("ID — ", "—") is None


def test_epic_findings_skip_duplicate_and_hints() -> None:
    text = "\n".join(
        [
            "| Epic | Title | Est | AC |",
            "| --- | --- | --- | --- |",
            "| AB-1 | First | 1 | do |",
            "| AB-1 | Dup | 1 | again |",
            "| not-an-epic | X | 1 | y |",
        ]
    )
    findings = rev._findings_from_epic_rows(text, None, set())
    assert [f.id for f in findings] == ["AB-1"]
    assert rev._epic_hint("S3") == "E-Q3"
    assert rev._epic_hint("Z9") == "E-Q4"
