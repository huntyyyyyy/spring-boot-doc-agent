"""ETL partition adversarial suites."""

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

class TestCrossGroupEdgesAdversarial:
    """Deviation: empty refs / empty groups still write a report — must not look healthy."""

    def test_empty_groups_report_is_vacuous_not_healthy(self) -> None:
        report = build_cross_group_edges.build_report(
            {"schema_version": 1, "groups": []},
            {
                "schema_version": 7,
                "repo_path": str(FIXTURE_DIR),
                "evidence": {"references": []},
                "entity_table_map": {},
            },
        )
        assert report["num_groups"] == 0
        assert report["references_rows"] == 0
        # Vacuous: zero shipped rows — callers must not treat this as a successful join.
        assert report["stats"]["rows_shipped"] == 0
        assert report["stats"].get("reduction_factor") is None

    def test_groups_with_no_references_ship_zero_cut_arcs(self) -> None:
        report = build_cross_group_edges.build_report(
            {
                "schema_version": 1,
                "groups": [
                    {"id": 0, "files": ["a/A.java"], "est_tokens": 10},
                    {"id": 1, "files": ["b/B.java"], "est_tokens": 10},
                ],
            },
            {
                "schema_version": 7,
                "repo_path": str(FIXTURE_DIR),
                "evidence": {"references": []},
                "entity_table_map": {},
            },
        )
        assert report["num_groups"] == 2
        assert report["stats"].get("cut_arcs", 0) == 0


class TestCorruptFactsFailValidation:
    """Deviation: malformed facts.jsonl must not pass the facts boundary."""

    def test_invalid_jsonl_line_raises(self, tmp_path: Path) -> None:
        from doc_engine.pipeline.validation import validate_artifact_file

        path = tmp_path / "facts.jsonl"
        path.write_text("{not-json\n", encoding="utf-8")
        with pytest.raises(ArtifactValidationError):
            validate_artifact_file("facts", path)


class TestSignalsFileReuseRequiresSiblings:
    """Deviation: --signals-file copied Path A alone and skipped Stage-0 dual-emit."""

    def test_local_runner_materializes_siblings_when_reusing_signals(
        self, tmp_path: Path
    ) -> None:
        signals = tmp_path / "spring_signals.json"
        signals.write_text(json.dumps(_minimal_signals()), encoding="utf-8")
        out = tmp_path / "out"
        out.mkdir()
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.pipeline.local_runner",
                str(FIXTURE_DIR),
                "--out-dir",
                str(out),
                "--deterministic-only",
                "--signals-file",
                str(signals),
                "--skip-drift",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert (out / "facts.jsonl").is_file()
        assert (out / "covering_proof.json").is_file()
        combined = proc.stderr + proc.stdout
        run_log = out / "run.log"
        if run_log.is_file():
            combined += run_log.read_text(encoding="utf-8")
        assert "facts not found" not in combined

    def test_local_runner_rejects_signals_without_file_signatures(
        self, tmp_path: Path
    ) -> None:
        signals = tmp_path / "spring_signals.json"
        signals.write_text(
            json.dumps(_minimal_signals(file_signatures={})), encoding="utf-8"
        )
        out = tmp_path / "out"
        out.mkdir()
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.pipeline.local_runner",
                str(FIXTURE_DIR),
                "--out-dir",
                str(out),
                "--deterministic-only",
                "--signals-file",
                str(signals),
                "--skip-drift",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode != 0
        combined = proc.stderr + proc.stdout
        assert "Stage-0 siblings" in combined or "file_signatures" in combined
