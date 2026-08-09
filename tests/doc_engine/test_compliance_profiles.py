"""Cohesive suite from tests/doc_engine/test_compliance.py: ResolveProfileTest, LoadConfigTest, StagesForProfileTest, GatesRequiredForProfileTest."""

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

class ResolveProfileTest(unittest.TestCase):
    def test_default_is_certified(self):
        args = Namespace(compliance_profile=None, deterministic_only=False)
        self.assertEqual(resolve_compliance_profile(None, args), ComplianceProfile.CERTIFIED)

    def test_deterministic_only_flag(self):
        args = Namespace(compliance_profile=None, deterministic_only=True)
        self.assertEqual(
            resolve_compliance_profile(None, args),
            ComplianceProfile.DETERMINISTIC_ONLY,
        )

    def test_explicit_cli_beats_yaml(self):
        config = Settings(compliance_profile=ComplianceProfile.SCAN_ONLY)
        args = Namespace(
            compliance_profile="certified",
            deterministic_only=False,
        )
        self.assertEqual(resolve_compliance_profile(config, args), ComplianceProfile.CERTIFIED)

    def test_explicit_cli_beats_deterministic_only(self):
        config = Settings(compliance_profile=ComplianceProfile.SCAN_ONLY)
        args = Namespace(
            compliance_profile="certified",
            deterministic_only=True,
        )
        self.assertEqual(resolve_compliance_profile(config, args), ComplianceProfile.CERTIFIED)

    def test_yaml_used_when_no_cli_override(self):
        config = Settings(compliance_profile=ComplianceProfile.DETERMINISTIC_ONLY)
        args = Namespace(compliance_profile=None, deterministic_only=False)
        self.assertEqual(
            resolve_compliance_profile(config, args),
            ComplianceProfile.DETERMINISTIC_ONLY,
        )


class LoadConfigTest(unittest.TestCase):
    def test_yaml_round_trip_compliance_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = os.path.join(tmp, ".doc-engine.yml")
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write("compliance_profile: scan_only\n")
            cfg = load_repo_config(tmp)
            self.assertIsNotNone(cfg)
            self.assertEqual(cfg.compliance_profile, ComplianceProfile.SCAN_ONLY)

    def test_invalid_profile_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = os.path.join(tmp, ".doc-engine.json")
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump({"compliance_profile": "not_a_profile"}, f)
            with self.assertRaises(ValidationError):
                load_repo_config(tmp)


class StagesForProfileTest(unittest.TestCase):
    def test_scan_only_stage_names(self):
        specs = stages_for_profile(ComplianceProfile.SCAN_ONLY, build_stage_specs())
        names = {s.name for s in specs}
        self.assertEqual(names, {"init_manifest", "signal_scan"})

    def test_deterministic_only_excludes_generative(self):
        specs = stages_for_profile(ComplianceProfile.DETERMINISTIC_ONLY, build_stage_specs())
        self.assertTrue(all(s.kind.name == "DETERMINISTIC" for s in specs))
        self.assertGreater(len(specs), 2)

    def test_certified_includes_generative(self):
        specs = stages_for_profile(ComplianceProfile.CERTIFIED, build_stage_specs())
        kinds = {s.kind.name for s in specs}
        self.assertIn("DETERMINISTIC", kinds)
        self.assertIn("GENERATIVE", kinds)

    def test_skip_signal_scan(self):
        specs = stages_for_profile(
            ComplianceProfile.SCAN_ONLY,
            build_stage_specs(),
            skip_signal_scan=True,
        )
        self.assertEqual([s.name for s in specs], ["init_manifest"])

    def test_until_truncates_inclusive(self):
        specs = stages_for_profile(
            ComplianceProfile.DETERMINISTIC_ONLY,
            build_stage_specs(),
            until_stage="partition",
        )
        self.assertEqual(
            [s.name for s in specs],
            ["init_manifest", "signal_scan", "gap_probe", "partition"],
        )

    def test_until_unknown_raises(self):
        with self.assertRaises(ValueError):
            stages_for_profile(
                ComplianceProfile.CERTIFIED,
                build_stage_specs(),
                until_stage="not_a_real_stage",
            )


class GatesRequiredForProfileTest(unittest.TestCase):
    def test_scan_only_gate_id(self):
        self.assertEqual(
            gates_required_for_profile(ComplianceProfile.SCAN_ONLY),
            frozenset({SCAN_ONLY_GATE_ID}),
        )

    def test_certified_gate_ids(self):
        self.assertEqual(
            gates_required_for_profile(ComplianceProfile.CERTIFIED),
            CERTIFIED_GATE_IDS,
        )
