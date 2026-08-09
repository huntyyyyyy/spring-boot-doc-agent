"""Covering callable-absence edge falsifiers."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from doc_engine.core.context import FileEntry, ScanContext
from doc_engine.pipeline.artifacts import Fact
from doc_engine.scanning._orchestrator import CoveringProofError, run_scan
from doc_engine.scanning._scanner_astgrep import AstGrepBackend
from doc_engine.scanning.absence import write_absence_facts
from doc_engine.scanning.covering import (
    COVERING_PROOF_SCHEMA_VERSION,
    build_covering_proof,
    build_receipt,
    inventory_root,
    subset_root,
    verify_covering_proof,
    write_covering_proof,
)
from doc_engine.scanning.facts import (
    covering_writer_facts,
    facts_from_signals,
    write_facts_jsonl,
)
from doc_engine.scanning.gap_probe import (
    CoveringPreconditionError,
    _astgrep_receipt_complete,
    build_gap_report,
    load_and_verify_covering,
    measure_r_absence,
    run_gap_probe,
)
from doc_engine.scanning.recall_delta import (
    collect_arm_entity_keys,
    write_recall_miss_facts,
)
from doc_engine.scanning.spring import AstGrepError, scan
from tests.conftest import FIXTURE_DIR, REPO_ROOT
from tests.support.covering_hard_stops.fixtures import _absence_stamp_pairs, _assert_absence_stamps_match_writer, _complete_receipt, _kafka_signals

class CallableAbsenceFalsifiersTestContinued(unittest.TestCase):
    def test_shared_bucket_rule_id_is_not_foreign_family_presence(self):
            """Deviation: any observability rule_id counted as redis/actuator hits."""
            from doc_engine.scanning.absence import _positive_hits

            signals = {
                "evidence": {
                    "observability": [
                        {
                            "file": "M.java",
                            "line": 1,
                            "match": "@Timed",
                            "rule_id": "observability__timed",
                        }
                    ],
                    "deployment": [],
                    "messaging": [],
                },
                "config_key_sets": {},
            }
            self.assertEqual(_positive_hits("redis", signals), 0)
            self.assertEqual(_positive_hits("actuator", signals), 0)
            facts = write_absence_facts(
                signals,
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=True,
            )
            redis = [f for f in facts if f["subject"] == "family:redis"]
            self.assertEqual(len(redis), 1)
            self.assertEqual(redis[0]["predicate"], "UNPROVEN")

    def test_fully_present_corpus_emits_empty_absence_bag(self):
            """Deviation: ``any(ABSENCE|UNPROVEN)`` required on a fully-present Path A.

            When every absence-writer family has family-scoped hits, the correct
            stamp set is empty. A smoke assert of the form ``any(...)`` would fail
            that healthy case or, worse, pass a bug that invents spurious stamps.
            """
            signals = {
                "evidence": {
                    "deployment": [
                        {
                            "file": "build.gradle",
                            "line": 1,
                            "match": "org.springframework.kafka:spring-kafka",
                            "rule_id": "deployment__build_dependency",
                        },
                        {
                            "file": "build.gradle",
                            "line": 2,
                            "match": "org.springframework.cloud:spring-cloud-starter-openfeign",
                            "rule_id": "deployment__build_dependency",
                        },
                        {
                            "file": "build.gradle",
                            "line": 3,
                            "match": "org.springframework.boot:spring-boot-starter-data-redis",
                            "rule_id": "deployment__build_dependency",
                        },
                        {
                            "file": "build.gradle",
                            "line": 4,
                            "match": "org.springframework.boot:spring-boot-starter-actuator",
                            "rule_id": "deployment__build_dependency",
                        },
                        {
                            "file": "build.gradle",
                            "line": 5,
                            "match": "software.amazon.awssdk:secretsmanager",
                            "rule_id": "deployment__build_dependency",
                        },
                        {
                            "file": "build.gradle",
                            "line": 6,
                            "match": "org.springframework.boot:spring-boot-starter-security",
                            "rule_id": "deployment__build_dependency",
                        },
                    ],
                    "messaging": [
                        {
                            "file": "M.java",
                            "line": 1,
                            "match": "@KafkaListener",
                            "rule_id": "messaging__kafka_listener",
                        }
                    ],
                    "outbound_clients": [
                        {
                            "file": "F.java",
                            "line": 1,
                            "match": "@FeignClient",
                            "rule_id": "outbound_clients__feign",
                        }
                    ],
                    "observability": [
                        {
                            "file": "A.java",
                            "line": 1,
                            "match": "actuator",
                            "rule_id": "observability__actuator",
                        }
                    ],
                    "configuration": [
                        {
                            "file": "R.java",
                            "line": 1,
                            "match": "redis",
                            "rule_id": "configuration__redis",
                        },
                        {
                            "file": "S.java",
                            "line": 1,
                            "match": "secretsmanager",
                            "rule_id": "configuration__aws_secrets",
                        },
                    ],
                    "security": [
                        {
                            "file": "Sec.java",
                            "line": 1,
                            "match": "@EnableWebSecurity",
                            "rule_id": "security__config",
                        }
                    ],
                },
                "config_key_sets": {"application.yml": ["spring.datasource.url"]},
            }
            facts = write_absence_facts(
                signals,
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=True,
            )
            self.assertEqual(facts, [])
            # The invariant the smoke tests must keep: recompute ≡ actual, including ∅.
            _assert_absence_stamps_match_writer(
                self,
                signals,
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=True,
                actual_rows=facts,
            )

    def test_empty_bucket_without_witness_never_absence(self):
            """Deviation: empty messaging bucket alone treated as feature absent."""
            signals = {
                "evidence": {"deployment": [], "messaging": []},
                "config_key_sets": {},
            }
            facts = write_absence_facts(
                signals,
                covering_ok=True,
                covering_root="root",
                scanner_version="sv",
                astgrep_receipt_complete=True,
            )
            messaging = [f for f in facts if f["subject"] == "family:messaging"]
            self.assertEqual(messaging[0]["predicate"], "UNPROVEN")
            self.assertIsNone(messaging[0]["qualifiers"]["family_witness"])
