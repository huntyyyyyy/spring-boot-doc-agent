"""Cohesive suite from tests/doc_engine/test_compliance.py: CertificationReportCoreTest."""

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

class CertificationReportCoreTest(unittest.TestCase):
    def test_all_ok_certified_true(self):
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
                gates,
                generative_executor="mock",
                allow_mock=True,
            )
            self.assertTrue(report.certified)
            self.assertEqual(report.failures, [])
            self.assertEqual(report.profile_gate_ids, sorted(CERTIFIED_GATE_IDS))
            self.assertEqual(report.completeness_claim, "fold_of_recorded_rows")

    def test_certified_mock_requires_allow_mock(self):
            """Deviation: CERTIFIED+mock folds certified without allow_mock."""
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
                gates,
                generative_executor="mock",
            )
            self.assertFalse(report.certified)
            self.assertIn(
                "generative_executor:mock:allow_mock_required",
                report.failures,
            )

    def test_omitted_required_stage_not_certified(self):
            """Deviation: only signal_scan recorded still certified under CERTIFIED."""
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                [StageRecord(name="signal_scan", status="ok")],
                gates,
                generative_executor="live",
            )
            self.assertFalse(report.certified)
            self.assertTrue(any(f.endswith(":missing") for f in report.failures))
            self.assertIn("stage:partition:missing", report.failures)

    def test_failed_gate_certified_false(self):
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                [StageRecord(name="signal_scan", status="ok")],
                [GateRecord(id="citation_coverage", label="gate", status="fail")],
            )
            self.assertFalse(report.certified)
            self.assertIn("gate:citation_coverage:fail", report.failures)
            # Other profile gates were never recorded → missing, not vacuous pass.
            self.assertIn("gate:validate_artifacts_all:missing", report.failures)

    def test_failed_stage_certified_false(self):
            report = build_certification_report(
                ComplianceProfile.SCAN_ONLY,
                "/repo",
                "/out",
                [
                    StageRecord(name="init_manifest", status="ok"),
                    StageRecord(name="signal_scan", status="fail", detail="exit 1"),
                ],
                [GateRecord(id=SCAN_ONLY_GATE_ID, label="signals", status="ok")],
            )
            self.assertFalse(report.certified)
            self.assertIn("stage:signal_scan:fail", report.failures)

    def test_missing_required_gate_is_not_certified(self):
            """Empty / partial gate audits must not certify against profile_gate_ids."""
            report = build_certification_report(
                ComplianceProfile.SCAN_ONLY,
                "/repo",
                "/out",
                ok_stages_for(ComplianceProfile.SCAN_ONLY),
                [],
            )
            self.assertFalse(report.certified)
            self.assertIn(f"gate:{SCAN_ONLY_GATE_ID}:missing", report.failures)

    def test_profile_required_gate_with_required_false_is_not_certified(self):
            """Deviation: stamping required=False + status=fail forges CERTIFIED."""
            gates = [
                GateRecord(id=gid, label=gid, status="fail", required=False)
                for gid in sorted(CERTIFIED_GATE_IDS)
            ]
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="mock"),
                gates,
                generative_executor="mock",
                allow_mock=True,
            )
            self.assertFalse(report.certified)
            for gid in sorted(CERTIFIED_GATE_IDS):
                self.assertIn(f"gate:{gid}:not_required", report.failures)

    def test_live_gates_exempts_test_pipeline_stages(self):
            """Live path does not rerun pytest; skipped test_pipeline_stages is ok."""
            gates = [
                GateRecord(id=gid, label=gid, status="ok")
                for gid in sorted(CERTIFIED_GATE_IDS - {"test_pipeline_stages"})
            ]
            gates.append(
                GateRecord(
                    id="test_pipeline_stages",
                    label="pytest test_pipeline_stages (not run on live gates path)",
                    status="skipped",
                    required=False,
                )
            )
            report = build_certification_report(
                ComplianceProfile.CERTIFIED,
                "/repo",
                "/out",
                ok_stages_for(ComplianceProfile.CERTIFIED, generative_executor="live"),
                gates,
                generative_executor="live",
            )
            self.assertTrue(report.certified)
            self.assertEqual(report.failures, [])
