"""Cohesive suite from tests/doc_engine/test_real_fixture_adversarial.py: _minimal_signals, _maps_to_fact, _real_artifacts_available, real_artifacts_bundle."""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest import mock
import pytest
from doc_engine.paths import repo_root
from doc_engine.real_fixture import real_artifacts_dir, real_repo_path
from doc_engine.scanning.covering import (
    build_covering_proof,
    build_receipt,
    inventory_root,
    verify_covering_proof,
)
from doc_engine.scanning.gap_probe import (
    CoveringPreconditionError,
    build_gap_report,
    measure_r_coll,
)
from doc_engine.scanning.symbol import format_type
from doc_engine.tools import spring_drift_check
REPO_ROOT = repo_root()
BASELINE = REPO_ROOT / "scripts" / "coverage" / "real_repo_gap_baseline.json"

def _minimal_signals(**overrides):
    base = {
        "schema_version": 7,
        "scanner_version": "adv",
        "entity_table_map": {
            "Order": {
                "file": "Order.java",
                "table": "orders",
                "package": "com.example",
                "fqcn": "com.example.Order",
            }
        },
        "evidence": {"raw_queries": [], "deployment": []},
        "file_signatures": {"Order.java": "abc"},
    }
    base.update(overrides)
    return base


def _maps_to_fact(package: str, name: str, table: str) -> dict:
    return {
        "predicate": "MAPS_TO",
        "subject": format_type(package, name),
        "object": table,
        "qualifiers": {
            "display_name": name,
            "fqcn": f"{package}.{name}",
            "symbol_kind": "type",
        },
        "file": f"{name}.java",
        "line": None,
        "rule_id": None,
        "scanner": None,
    }


def _real_artifacts_available() -> bool:
    root = real_artifacts_dir(prefer_default=False)
    if root is None:
        root = real_artifacts_dir(prefer_default=True)
    return bool(root and (root / "spring_signals.json").is_file())


def real_artifacts_bundle() -> tuple[dict, list, Path]:
    root = real_artifacts_dir(prefer_default=False)
    if root is None:
        root = real_artifacts_dir(prefer_default=True)
    assert root is not None
    signals = json.loads((root / "spring_signals.json").read_text(encoding="utf-8"))
    facts = [
        json.loads(line)
        for line in (root / "facts.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return signals, facts, root
