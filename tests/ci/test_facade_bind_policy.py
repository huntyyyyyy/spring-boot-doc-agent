"""Global lock: lazy `_facade()` binds must match climb poke targets."""

from __future__ import annotations

import importlib

import pytest

from doc_engine.ci.facade_bind_policy import (
    FACADE_BINDS,
    facade_bind_errors,
    resolve_facade,
)
from doc_engine.paths import PathValidationError
from doc_engine.semantic_eval import scan
from doc_engine.tools import semantic_eval as seh
from doc_engine.tools import semantic_eval_helpers as helpers
from doc_engine.tools.semantic_eval_scan import markdown_names

pytestmark = pytest.mark.domain_ci_meta


def test_facade_bind_registry_nonempty() -> None:
    assert FACADE_BINDS, "register at least one climb façade bind"


def test_facade_bind_policy_green_on_tip() -> None:
    assert facade_bind_errors() == []


def test_semantic_eval_scan_facade_is_tools_semantic_eval_not_helpers() -> None:
    """Regression: helpers shim ≠ poke target used by climb B7."""
    assert scan._facade() is seh
    assert scan._facade() is not helpers
    assert resolve_facade("doc_engine.semantic_eval.scan", "_facade") is seh


def test_wrong_helpers_bind_would_miss_monkeypatch(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Adversarial: setattr on seh must bite scan; helpers-only bind would not."""
    (tmp_path / "ok.md").write_text("# hi", encoding="utf-8")
    (tmp_path / "bad.md").write_text("# bad", encoding="utf-8")

    def fake_join(docs_dir: str, name: str):
        if name == "bad.md":
            raise PathValidationError("unsafe")
        return tmp_path / name

    monkeypatch.setattr(seh, "join_under", fake_join)
    # Prove helpers still has the real join_under (would be used by a wrong bind).
    assert helpers.join_under is not fake_join
    assert markdown_names(str(tmp_path)) == ["ok.md"]


def test_facade_bind_errors_detects_wrong_module() -> None:
    def _wrong(_producer: str, _attr: str):
        return helpers

    errors = facade_bind_errors(resolver=_wrong)
    assert errors, "wrong bind must fail closed"
    assert "semantic_eval_helpers" in errors[0] or "want" in errors[0]


def test_every_registered_bind_importable() -> None:
    for producer, attr, expected in FACADE_BINDS:
        importlib.import_module(producer)
        importlib.import_module(expected)
        assert callable(getattr(importlib.import_module(producer), attr))
