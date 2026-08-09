"""Cohesive suite from tests/doc_engine/test_compliance.py: CertificationReportLiveTest, FinishMessagingTest, ScanOnlyIntegrationTest."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from pydantic import ValidationError
from doc_engine.config.loader import load_repo_config
from doc_engine.config.settings import Settings
from doc_engine.pipeline.compliance import (
    CERTIFIED_GATE_IDS,
    SCAN_ONLY_GATE_ID,
    ComplianceProfile,
    GateRecord,
    StageRecord,
    build_certification_report,
    gates_required_for_profile,
    resolve_compliance_profile,
    stages_for_profile,
    write_certification_json,
)
from doc_engine.pipeline.stages import build_stage_specs
from tests.conftest import FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from tests.doc_engine.cert_helpers import ok_stages_for

import pytest

pytestmark = pytest.mark.domain_compliance

class CertificationReportLiveTest(unittest.TestCase):
    def test_write_certification_json(self):
            with tempfile.TemporaryDirectory() as tmp:
                report = build_certification_report(
                    ComplianceProfile.SCAN_ONLY,
                    "/repo",
                    tmp,
                    ok_stages_for(ComplianceProfile.SCAN_ONLY),
                    [GateRecord(id=SCAN_ONLY_GATE_ID, label="signals", status="ok")],
                )
                path = write_certification_json(tmp, report)
                self.assertTrue(path.is_file())
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(data["schema_version"], 1)
                self.assertEqual(data["compliance_profile"], "scan_only")
                self.assertTrue(data["certified"])
                self.assertEqual(data["completeness_claim"], "fold_of_recorded_rows")
                self.assertIn("executor", data["stages"][0])

    def test_failed_stage_with_empty_gates_not_certified(self):
            """Vacuously empty gate list must not imply certified when a stage failed."""
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                [StageRecord(name="doc_writer", status="fail", detail="mock raised")],
                [],
                generative_executor="mock",
            )
            self.assertFalse(report.certified)
            self.assertIn("stage:doc_writer:fail", report.failures)
            self.assertTrue(any(f.endswith(":missing") for f in report.failures))

    def test_skipped_required_stage_fails(self):
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                [
                    StageRecord(name="signal_scan", status="ok"),
                    StageRecord(name="doc_writer", status="skipped", executor="none"),
                ],
                gates,
                generative_executor="mock",
            )
            self.assertFalse(report.certified)
            self.assertIn("stage:doc_writer:skipped", report.failures)

    def test_skipped_non_required_stage_does_not_fail_scan_only(self):
            report = build_certification_report(
                ComplianceProfile.SCAN_ONLY,
                "/repo",
                "/out",
                [
                    *ok_stages_for(ComplianceProfile.SCAN_ONLY),
                    StageRecord(name="doc_writer", status="skipped", executor="none"),
                ],
                [GateRecord(id=SCAN_ONLY_GATE_ID, label="signals", status="ok")],
            )
            self.assertTrue(report.certified)
            self.assertEqual(report.failures, [])

    def test_mock_under_live_consistency(self):
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                [
                    StageRecord(name="signal_scan", status="ok"),
                    StageRecord(name="doc_writer", status="ok", executor="mock"),
                ],
                gates,
                generative_executor="live",
            )
            self.assertFalse(report.certified)
            self.assertIn("stage:doc_writer:mock_under_live", report.failures)

    def test_stage_records_from_runner_preserve_mock_executor(self):
            from doc_engine.pipeline.compliance import stage_records_from_runner_results

            rows = stage_records_from_runner_results(
                [
                    ("pipeline:signal_scan", "OK", 0.1, "exit 0"),
                    ("pipeline:doc_writer", "MOCK", 0.2, "mocked"),
                ]
            )
            by_name = {r.name: r for r in rows}
            self.assertEqual(by_name["signal_scan"].executor, "deterministic")
            self.assertEqual(by_name["doc_writer"].status, "ok")
            self.assertEqual(by_name["doc_writer"].executor, "mock")

    def test_stages_for_live_certification_strips_generative_and_appends_external(self):
            from doc_engine.pipeline.compliance import (
                GENERATIVE_EXTERNAL_STAGE,
                stages_for_live_certification,
            )

            prior = [
                StageRecord(name="signal_scan", status="ok"),
                StageRecord(name="doc_writer", status="ok", executor="mock"),
                StageRecord(name="architect", status="skipped", executor="none"),
                # Legacy v1 shape: generative name, default executor=deterministic
                StageRecord(name="file_summarize", status="ok"),
            ]
            derived = stages_for_live_certification(prior)
            names = [s.name for s in derived]
            self.assertEqual(names.count("signal_scan"), 1)
            self.assertNotIn("doc_writer", names)
            self.assertNotIn("architect", names)
            self.assertNotIn("file_summarize", names)
            self.assertEqual(names[-1], GENERATIVE_EXTERNAL_STAGE)
            self.assertEqual(derived[-1].executor, "live")

    def test_citations_are_strict_matches_local_runner_rule(self):
            from doc_engine.pipeline.compliance import citations_are_strict

            self.assertTrue(citations_are_strict(ComplianceProfile.CERTIFIED))
            self.assertFalse(citations_are_strict(ComplianceProfile.SCAN_ONLY))
            self.assertFalse(citations_are_strict(ComplianceProfile.DETERMINISTIC_ONLY))
            self.assertTrue(
                citations_are_strict(
                    ComplianceProfile.SCAN_ONLY, force_strict=True
                )
            )

class FinishMessagingTest(unittest.TestCase):
    def test_success_lines_only_when_certified(self):
        from doc_engine.pipeline.local_runner import Log, Runner, _write_certification_and_finish

        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "run.log")
            log = Log(log_path)
            runner = Runner(log, keep_going=False)
            runner.record("pipeline:doc_writer", "FAIL", 0.0, "mock failed")
            code = _write_certification_and_finish(
                log,
                runner,
                ComplianceProfile.CERTIFIED,
                "/repo",
                tmp,
                "mock",
                show_table=False,
                success_lines=["RESULT: every gate passed."],
            )
            transcript = Path(log_path).read_text(encoding="utf-8")
            self.assertEqual(code, 1)
            self.assertNotIn("every gate passed", transcript)
            self.assertIn("certification failed", transcript)

class ScanOnlyIntegrationTest(unittest.TestCase):
    def test_scan_only_with_signals_file_writes_certification(self):
        from doc_engine.pipeline.local_runner import run_pipeline

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = os.path.join(tmp, "run")
            args = Namespace(
                repo_path=str(FIXTURE_DIR),
                out_dir=out_dir,
                max_tokens=120000,
                docs_in_target_repo=False,
                prior_signals=None,
                skip_drift=True,
                respect_gitignore=False,
                strict_citations=False,
                keep_going=False,
                compliance_profile="scan_only",
                deterministic_only=False,
                signals_file=str(FIXTURE_SNAPSHOT_PATH),
            )
            code = run_pipeline(args)
            cert_path = os.path.join(out_dir, "certification.json")
            self.assertTrue(os.path.isfile(cert_path))
            with open(cert_path, encoding="utf-8") as f:
                cert = json.load(f)
            self.assertEqual(cert["compliance_profile"], "scan_only")
            self.assertTrue(cert["certified"])
            self.assertEqual(code, 0)
