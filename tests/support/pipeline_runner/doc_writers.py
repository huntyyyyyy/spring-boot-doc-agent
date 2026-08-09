"""Cohesive suite from tests/doc_engine/test_pipeline_runner.py: _write_summaries, _write_arch, _write_interview, _write_doc."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
import pytest
from doc_engine.pipeline.context import PipelineContext, StageKind, StageSpec
from doc_engine.pipeline.executor import MockStageExecutor, SubprocessStageRunner
from doc_engine.pipeline.runner import PipelineRunner
from doc_engine.pipeline.stages import build_stage_specs
from doc_engine.pipeline.validation import validate_artifact_file
from tests.conftest import FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH

def _write_summaries(ctx: PipelineContext) -> str:
    path = ctx.out_dir / "summaries.json"
    path.write_text(
        json.dumps([{
            "file": "src/main/java/com/example/billing/Invoice.java",
            "cluster": [],
            "summary": "test",
            "relationships": [],
            "cross_group_relationships": [],
            "group_function": "billing",
            "spring_role": "entity",
            "evidence": [{"line": 1, "what": "entity"}],
        }]),
        encoding="utf-8",
    )
    return "1 summary"


def _write_arch(ctx: PipelineContext) -> str:
    (ctx.out_dir / "architecture_merged.md").write_text("# arch\n", encoding="utf-8")
    return "architecture"


def _write_interview(ctx: PipelineContext) -> str:
    path = ctx.out_dir / "interview_answers.json"
    path.write_text(
        json.dumps([{
            "id": "q1",
            "question": "q?",
            "status": "answered",
            "answer": "a",
            "date": ctx.today,
        }]),
        encoding="utf-8",
    )
    return "1 answer"


def _write_doc(ctx: PipelineContext) -> str:
    (ctx.docs_dir / "readme.md").write_text("# readme\n", encoding="utf-8")
    return "readme"
