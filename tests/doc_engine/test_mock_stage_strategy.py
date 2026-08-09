"""Characterization: mock stage Strategy registry (E-MOD1)."""

from __future__ import annotations

import pytest

from doc_engine.pipeline.mock_stage_constants import (
    STAGE_ARCHITECT,
    STAGE_DOC_WRITER,
    STAGE_FILE_SUMMARIZE,
    STAGE_GAP_INTERVIEW,
)
from doc_engine.pipeline.mock_stage_strategy import (
    default_mock_stage_registry,
    resolve_mock_stage,
)
from doc_engine.pipeline.mock_stages import mock_architecture, mock_docs


def test_default_registry_covers_generative_mock_stages():
    registry = default_mock_stage_registry()
    assert set(registry) == {
        STAGE_FILE_SUMMARIZE,
        STAGE_ARCHITECT,
        STAGE_GAP_INTERVIEW,
        STAGE_DOC_WRITER,
    }


def test_resolve_mock_stage_returns_facade_callables():
    assert resolve_mock_stage(STAGE_ARCHITECT) is mock_architecture
    assert resolve_mock_stage(STAGE_DOC_WRITER) is mock_docs


def test_resolve_mock_stage_unknown_key_raises():
    with pytest.raises(KeyError, match="no mock stage strategy"):
        resolve_mock_stage("not_a_real_stage")
