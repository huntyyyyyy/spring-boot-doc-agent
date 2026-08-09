"""Claim-gate suites (split by concern for the 225 LOC ratchet).

Canonical coverage lives in ``test_repo_claims_*.py`` under this directory.
This file keeps ``suite_layout.suite_file_for_module`` paired with
``scripts/ci/check_repo_claims.py`` (same pattern as ``test_run_manifest.py``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.domain_ci_meta

_SPLIT_PREFIX = "test_repo_claims_"


def test_split_suites_cover_check_repo_claims() -> None:
    """The module must retain at least one split suite under tests/ci/."""
    here = Path(__file__).resolve().parent
    splits = sorted(here.glob(f"{_SPLIT_PREFIX}*.py"))
    assert splits, f"expected {_SPLIT_PREFIX}*.py next to {here.name}"
