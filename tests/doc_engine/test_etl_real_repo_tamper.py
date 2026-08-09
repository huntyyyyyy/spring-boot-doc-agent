"""Cohesive suite from tests/doc_engine/test_etl_adversarial.py: TestRealRepoEtlTamper."""

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

class TestRealRepoEtlTamper():
    """Product-truth ETL against DOC_ENGINE_REAL_REPO / local-runs/real-repo.path.

Hermetic FIXTURE_DIR is not a stand-in for mid-size Spring distributions —
these scans must hit the operator's real tree."""
def test_planted_unverified_gap_report_fails_validate_all(self, tmp_path: Path) -> None:
        """Deviation: schema-valid but s1_covering.verified=false greened --all."""
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
        (gap_dir / "gap_report.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "s1_covering": {"verified": False, "proof_present": True},
                    "oracle": {
                        "arm_present": False,
                        "claim": "omitted_without_oracle",
                        "R_recall": None,
                    },
                    "rates": {
                        "R_recall": {
                            "claim": "omitted_without_oracle",
                            "numerator": None,
                            "denominator": None,
                            "rate": None,
                        }
                    },
                    "uncertainty": {"U": 0.0},
                }
            ),
            encoding="utf-8",
        )
        code = validate_artifacts.main(["--all", str(tmp_path)])
        assert code == 1

def test_until_signal_scan_not_certified_even_with_planted_gap(self, tmp_path: Path) -> None:
        """Deviation: --until signal_scan + planted gap_report greened det cert."""
        repo = _product_scan_tree()
        out = tmp_path / "run"
        out.mkdir()
        gap_dir = out / "gap_report"
        gap_dir.mkdir()
        (gap_dir / "gap_report.json").write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "s1_covering": {"verified": True, "proof_present": True},
                    "oracle": {
                        "arm_present": False,
                        "claim": "omitted_without_oracle",
                        "R_recall": None,
                    },
                    "rates": {
                        "R_recall": {
                            "claim": "omitted_without_oracle",
                            "rate": None,
                        }
                    },
                    "uncertainty": {"U": 0.0},
                }
            ),
            encoding="utf-8",
        )
        env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "doc_engine.pipeline.local_runner",
                str(repo),
                "--out-dir",
                str(out),
                "--deterministic-only",
                "--until",
                "signal_scan",
                "--skip-drift",
            ],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        cert_path = out / "certification.json"
        assert cert_path.is_file(), proc.stderr + proc.stdout
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
        assert cert["certified"] is False
        assert any("gap_probe" in f for f in cert["failures"])
        assert proc.returncode != 0

def test_tampered_covering_fails_gap_probe(self, tmp_path: Path) -> None:
        from doc_engine.scanning.gap_probe import CoveringPreconditionError, run_gap_probe

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
        covering = tmp_path / "covering_proof.json"
        payload = json.loads(covering.read_text(encoding="utf-8"))
        payload["inventory_root"] = "deadbeef"
        covering.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises(CoveringPreconditionError):
            run_gap_probe(
                out_signals,
                tmp_path / "facts.jsonl",
                tmp_path / "gap",
                covering_path=covering,
            )
