"""Strategy port + registry for mock generative pipeline stages."""

from __future__ import annotations

from typing import Callable, Protocol

from doc_engine.pipeline.mock_architecture_stage import mock_architecture
from doc_engine.pipeline.mock_docs_stage import mock_docs
from doc_engine.pipeline.mock_file_summaries import mock_file_summaries
from doc_engine.pipeline.mock_gap_interview import mock_gap_and_interview
from doc_engine.pipeline.mock_stage_constants import (
    STAGE_ARCHITECT,
    STAGE_DOC_WRITER,
    STAGE_FILE_SUMMARIZE,
    STAGE_GAP_INTERVIEW,
)


class MockStageStrategy(Protocol):
    """Port: one mock generative stage — shape-faithful artifacts, no LLM."""

    def __call__(self, *args, **kwargs) -> str:
        ...


MockStageHandler = Callable[..., str]


def default_mock_stage_registry() -> dict[str, MockStageHandler]:
    """Map generative stage keys to mock strategy callables (OCP registration)."""
    return {
        STAGE_FILE_SUMMARIZE: mock_file_summaries,
        STAGE_ARCHITECT: mock_architecture,
        STAGE_GAP_INTERVIEW: mock_gap_and_interview,
        STAGE_DOC_WRITER: mock_docs,
    }


def resolve_mock_stage(
    stage_key: str,
    registry: dict[str, MockStageHandler] | None = None,
) -> MockStageHandler:
    """Return the registered mock strategy for *stage_key*."""
    table = registry if registry is not None else default_mock_stage_registry()
    try:
        return table[stage_key]
    except KeyError as exc:
        raise KeyError(
            f"no mock stage strategy registered for {stage_key!r}"
        ) from exc
