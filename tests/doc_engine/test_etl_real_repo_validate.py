"""Cohesive suite from tests/doc_engine/test_etl_adversarial.py: TestRealRepoEtlValidate."""

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

pytestmark = pytest.mark.domain_stage0

REPO_ROOT = repo_root()
from tests.support.etl_adversarial.factories import (
    _minimal_signals,
    _product_scan_tree,
)

class TestRealRepoEtlValidate():
    """Product-truth ETL against DOC_ENGINE_REAL_REPO / local-runs/real-repo.path.

Hermetic FIXTURE_DIR is not a stand-in for mid-size Spring distributions —
these scans must hit the operator's real tree."""
    def test_real_scan_then_validate_all(self, tmp_path: Path) -> None:
        repo = _product_scan_tree()
        out_signals = tmp_path / "spring_signals.json"
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.tools.spring_signal_scan",
                str(repo),
                "--out",
                str(out_signals),
                "--scanners",
                "filesystem,ast-grep",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            pytest.fail(f"real-repo scan failed:\n{proc.stderr}\n{proc.stdout}")
        assert (tmp_path / "facts.jsonl").is_file()
        assert (tmp_path / "covering_proof.json").is_file()
        require_stage0_siblings(tmp_path)
        gap = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.tools.gap_probe",
                "--signals",
                str(out_signals),
                "--facts",
                str(tmp_path / "facts.jsonl"),
                "--covering",
                str(tmp_path / "covering_proof.json"),
                "--out",
                str(tmp_path / "gap_report"),
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert gap.returncode == 0, gap.stderr
        assert (tmp_path / "gap_report" / "gap_report.json").is_file()
        from doc_engine.pipeline.validation import require_gap_probe_artifact

        require_gap_probe_artifact(tmp_path)
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 0

    def test_validate_all_rejects_signals_without_gap_report(self, tmp_path: Path) -> None:
        """Deviation: Path A + siblings greened without gap_probe measurement."""
        repo = _product_scan_tree()
        out_signals = tmp_path / "spring_signals.json"
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.tools.spring_signal_scan",
                str(repo),
                "--out",
                str(out_signals),
                "--scanners",
                "filesystem,ast-grep",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            pytest.fail(f"real-repo scan failed:\n{proc.stderr}\n{proc.stdout}")
        require_stage0_siblings(tmp_path)
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 1

    def test_planted_empty_gap_report_fails_validate_all(self, tmp_path: Path) -> None:
        """Deviation: existence-only gap_report greened planted {}."""
        repo = _product_scan_tree()
        out_signals = tmp_path / "spring_signals.json"
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.tools.spring_signal_scan",
                str(repo),
                "--out",
                str(out_signals),
                "--scanners",
                "filesystem,ast-grep",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            pytest.fail(f"real-repo scan failed:\n{proc.stderr}\n{proc.stdout}")
        gap_dir = tmp_path / "gap_report"
        gap_dir.mkdir()
        (gap_dir / "gap_report.json").write_text("{}", encoding="utf-8")
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 1
