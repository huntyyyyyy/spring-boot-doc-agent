"""ETL validate-all fail-closed suites."""

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
from tests.support.etl_adversarial.factories import (
    _minimal_signals,
    _product_scan_tree,
)

class TestValidateAllFailClosed:
    """Deviation: validate --all greened empty dirs / signals-only dumps."""

    def test_empty_dir_exits_nonzero(self, tmp_path: Path) -> None:
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 1

    def test_signals_without_facts_sibling_fails(self, tmp_path: Path) -> None:
        (tmp_path / "spring_signals.json").write_text(
            json.dumps(_minimal_signals()), encoding="utf-8"
        )
        with pytest.raises(ArtifactValidationError) as ctx:
            require_stage0_siblings(tmp_path)
        assert "facts.jsonl" in str(ctx.value)

    def test_signals_without_covering_sibling_fails(self, tmp_path: Path) -> None:
        (tmp_path / "spring_signals.json").write_text(
            json.dumps(_minimal_signals()), encoding="utf-8"
        )
        (tmp_path / "facts.jsonl").write_text("{}\n", encoding="utf-8")
        with pytest.raises(ArtifactValidationError) as ctx:
            require_stage0_siblings(tmp_path)
        assert "covering_proof.json" in str(ctx.value)

    def test_complete_siblings_pass_require(self, tmp_path: Path) -> None:
        (tmp_path / "spring_signals.json").write_text(
            json.dumps(_minimal_signals()), encoding="utf-8"
        )
        (tmp_path / "facts.jsonl").write_text("{}\n", encoding="utf-8")
        (tmp_path / "covering_proof.json").write_text("{}", encoding="utf-8")
        require_stage0_siblings(tmp_path)  # does not raise

    def test_cli_all_rejects_signals_only(self, tmp_path: Path) -> None:
        (tmp_path / "spring_signals.json").write_text(
            json.dumps(_minimal_signals()), encoding="utf-8"
        )
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 1


class TestStageSpecOutputsComplete:
    """Deviation: capacity/edges/covering absent from stage outputs → silent miss."""

    def test_signal_scan_requires_covering_and_facts(self) -> None:
        spec = next(s for s in build_stage_specs() if s.name == "signal_scan")
        assert "facts.jsonl" in spec.outputs
        assert "covering_proof.json" in spec.outputs
        assert ARTIFACT_FILENAMES["spring_signals"] in spec.outputs

    def test_capacity_requires_report_output(self) -> None:
        spec = next(s for s in build_stage_specs() if s.name == "capacity_preflight")
        assert "capacity_preflight_report.json" in spec.outputs

    def test_edges_output_is_registered_filename(self) -> None:
        spec = next(s for s in build_stage_specs() if s.name == "cross_group_edges")
        assert spec.outputs == (ARTIFACT_FILENAMES["cross_group_edges"],)

    def test_gap_probe_is_required_deterministic_stage(self) -> None:
        """Deviation: gap_probe lived as opt-in CLI; Path A certified without U."""
        names = [s.name for s in build_stage_specs()]
        assert "gap_probe" in names
        idx_scan = names.index("signal_scan")
        idx_gap = names.index("gap_probe")
        assert idx_gap == idx_scan + 1
        spec = next(s for s in build_stage_specs() if s.name == "gap_probe")
        assert "gap_report/gap_report.json" in spec.outputs


class TestPartitionAdversarial:
    """Deviation: partition could emit empty / inconsistent groups unnoticed."""

    def test_empty_repo_tree_produces_zero_groups_not_crash(self, tmp_path: Path) -> None:
        repo = tmp_path / "empty"
        repo.mkdir()
        files = partition_repo.dfs_file_list(
            str(repo),
            partition_repo.DEFAULT_EXCLUDED_DIRS,
            partition_repo.DEFAULT_EXCLUDED_EXTS,
            partition_repo.DEFAULT_EXCLUDED_FILES,
        )
        assert files == []
        groups = partition_repo.build_groups([], max_tokens=2000, overlap_ratio=0.1)
        assert groups == []

    def test_single_oversized_file_still_emitted(self, tmp_path: Path) -> None:
        # One file larger than max_tokens must still form a group (atomic files).
        groups = partition_repo.build_groups(
            [("Huge.java", 50_000)], max_tokens=100, overlap_ratio=0.1
        )
        assert len(groups) == 1
        assert groups[0][0][0] == "Huge.java"
