"""Mock generative stages façade — stable import path for pipeline + kitchen.

Implementation lives in concept modules (`mock_citations`, `mock_*_stage`,
`mock_todo_sweep`, `mock_stage_strategy`). This module re-exports the public
and historically imported private helpers so callers need not churn.
"""

from __future__ import annotations

from doc_engine.pipeline.mock_architecture_stage import mock_architecture
from doc_engine.pipeline.mock_citations import (
    confirmed_tag,
    evidenced,
    load_citations,
    per_existing_docs_tag,
    pick,
    unknown_tag,
)
from doc_engine.pipeline.mock_docs_stage import mock_docs
from doc_engine.pipeline.mock_file_summaries import mock_file_summaries
from doc_engine.pipeline.mock_gap_interview import mock_gap_and_interview
from doc_engine.pipeline.mock_stage_constants import (
    BUCKET_PHRASING,
    DOC_BUCKETS,
    DOC_ORDER,
    EM,
    SPRING_ROLE_BY_BUCKET,
    STAGE_ARCHITECT,
    STAGE_DOC_WRITER,
    STAGE_FILE_SUMMARIZE,
    STAGE_GAP_INTERVIEW,
    STAGE_PARTITION,
    STAGE_SIGNAL_SCAN,
)
from doc_engine.pipeline.mock_stage_io import (
    _read_json,
    _write_json,
    _write_text,
    find_existing_readme,
)
from doc_engine.pipeline.mock_stage_strategy import (
    MockStageStrategy,
    default_mock_stage_registry,
    resolve_mock_stage,
)
from doc_engine.pipeline.mock_todo_sweep import sweep_todos

__all__ = [
    "BUCKET_PHRASING",
    "DOC_BUCKETS",
    "DOC_ORDER",
    "EM",
    "MockStageStrategy",
    "SPRING_ROLE_BY_BUCKET",
    "STAGE_ARCHITECT",
    "STAGE_DOC_WRITER",
    "STAGE_FILE_SUMMARIZE",
    "STAGE_GAP_INTERVIEW",
    "STAGE_PARTITION",
    "STAGE_SIGNAL_SCAN",
    "_read_json",
    "_write_json",
    "_write_text",
    "confirmed_tag",
    "default_mock_stage_registry",
    "evidenced",
    "find_existing_readme",
    "load_citations",
    "mock_architecture",
    "mock_docs",
    "mock_file_summaries",
    "mock_gap_and_interview",
    "per_existing_docs_tag",
    "pick",
    "resolve_mock_stage",
    "sweep_todos",
    "unknown_tag",
]
