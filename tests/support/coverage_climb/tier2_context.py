"""Shared context factory for coverage-climb tier2 suites."""

from __future__ import annotations

from pathlib import Path

from doc_engine.pipeline.context import PipelineContext


def _ctx(tmp_path: Path) -> PipelineContext:
    out = tmp_path / "out"
    docs = out / "docs"
    out.mkdir(exist_ok=True)
    docs.mkdir(exist_ok=True)
    return PipelineContext(
        repo_path=tmp_path,
        out_dir=out,
        manifest_path=out / "run_manifest.json",
        docs_dir=docs,
        python="python",
        today="2026-08-08",
        respect_gitignore=False,
        max_tokens=120000,
        log=lambda _msg: None,
    )
