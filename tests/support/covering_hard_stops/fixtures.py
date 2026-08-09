"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: _kafka_signals, _complete_receipt, _absence_stamp_pairs, _assert_absence_stamps_match_writer, shutil_which."""

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

def _kafka_signals(*, messaging_hits: int = 0) -> dict:
    messaging = []
    for i in range(messaging_hits):
        messaging.append(
            {
                "file": f"M{i}.java",
                "line": i + 1,
                "match": "@KafkaListener",
                "rule_id": "messaging__kafka_listener",
            }
        )
    return {
        "evidence": {
            "deployment": [
                {
                    "file": "build.gradle",
                    "line": 1,
                    "match": "org.springframework.kafka:spring-kafka",
                    "rule_id": "deployment__build_dependency",
                }
            ],
            "messaging": messaging,
        },
        "config_key_sets": {},
        "entity_table_map": {},
        "scanner_version": "sv-test",
        "scanners": ["filesystem", "ast-grep"],
    }


def _complete_receipt(scanner: str, file_signatures: dict) -> dict:
    """Build a complete receipt whose subset roots match ``scope`` recomputation."""
    from doc_engine.scanning.covering import expected_subset_root_for_scope

    scope = "java" if scanner != "filesystem" else "all_signatures"
    root = expected_subset_root_for_scope(file_signatures, scope)
    return build_receipt(
        scanner=scanner,
        version_hash="v",
        scope=scope,
        expected_subset_root=root,
        acked_subset_root=root,
        status="complete",
    )


def _absence_stamp_pairs(rows) -> set[tuple[str, str]]:
    return {
        (str(r["predicate"]), str(r["subject"]))
        for r in rows
        if r.get("predicate") in {"ABSENCE", "UNPROVEN"}
    }


def _assert_absence_stamps_match_writer(
    test: unittest.TestCase,
    signals: dict,
    *,
    covering_ok: bool,
    covering_root: str | None,
    scanner_version: str | None,
    astgrep_receipt_complete: bool,
    actual_rows,
) -> None:
    """Dual-emit ABSENCE/UNPROVEN must equal write_absence_facts on the same inputs.

    Unlike ``any(ABSENCE|UNPROVEN)``, this passes for a fully-present corpus
    (both sides empty) and fails if stamps are wrong, not merely missing.
    """
    expected = write_absence_facts(
        signals,
        covering_ok=covering_ok,
        covering_root=covering_root,
        scanner_version=scanner_version,
        astgrep_receipt_complete=astgrep_receipt_complete,
    )
    test.assertEqual(
        _absence_stamp_pairs(actual_rows),
        _absence_stamp_pairs(expected),
    )


def shutil_which(name: str):
    import shutil

    return shutil.which(name)
