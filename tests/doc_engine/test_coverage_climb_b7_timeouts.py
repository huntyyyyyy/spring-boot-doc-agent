"""Coverage climb B7: core.timeouts positive env parse.

Q2 adequacy witness: mutmut_slice on doc_engine.core.timeouts — asserts bite
positive integer env return path (not only error branches).
"""

from __future__ import annotations

import pytest

from doc_engine.core import timeouts as to

pytestmark = pytest.mark.domain_climb_sensor


def test_env_seconds_positive_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "42")
    assert to.tool_timeout_seconds() == 42
    monkeypatch.setenv("DOC_ENGINE_CODEQL_TIMEOUT", "99")
    assert to.codeql_database_timeout_seconds() == 99


def test_env_seconds_rejects_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "0")
    with pytest.raises(ValueError, match="positive"):
        to.tool_timeout_seconds()
