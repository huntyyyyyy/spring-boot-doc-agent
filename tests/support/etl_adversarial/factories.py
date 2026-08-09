"""Cohesive suite from tests/doc_engine/test_etl_adversarial.py: _product_scan_tree, _minimal_signals."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.paths import repo_root
from doc_engine.pipeline.artifacts import ARTIFACT_FILENAMES
from doc_engine.pipeline.stages import build_stage_specs
from doc_engine.pipeline.validation import (
    ArtifactValidationError,
    require_stage0_siblings,
    validate_artifacts_in_dir,
)
from doc_engine.real_fixture import require_real_repo
from doc_engine.tools import build_cross_group_edges, validate_artifacts
from doc_engine.tools import partition_repo
from tests.conftest import FIXTURE_DIR
REPO_ROOT = repo_root()

def _product_scan_tree() -> Path:
    """Real Spring tree for product-truth ETL scans (not the hermetic fixture)."""
    try:
        return require_real_repo()
    except FileNotFoundError as exc:
        pytest.skip(str(exc))


def _minimal_signals(**overrides) -> dict:
    base = {
        "schema_version": 7,
        "scanner_version": "etl-adv",
        "repo_path": str(FIXTURE_DIR),
        "files_scanned": {"java": 1, "yml": 0},
        "entity_table_map": {},
        "evidence": {"references": []},
        "file_signatures": {"A.java": "abc"},
    }
    base.update(overrides)
    return base
