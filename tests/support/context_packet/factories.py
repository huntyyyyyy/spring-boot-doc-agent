"""Cohesive suite from tests/doc_engine/test_context_packet.py: _write_run_dir."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.freshness import (
    AssumeIndexed,
    SignatureFreshness,
    label_item_path,
)
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError
from doc_engine.query.packet import CONTEXT_PACKET_SCHEMA_VERSION, run_context_packet
from doc_engine.query.rank import (
    bucket_priority,
    estimate_tokens,
    score_item,
    tokenize,
    trim_to_budget,
)

def _write_run_dir(tmp: Path, *, signatures: dict | None = None) -> Path:
    run = tmp / "run"
    run.mkdir()
    signals = {
        "schema_version": 2,
        "scanners": ["ast-grep"],
        "evidence": {
            "security": [
                {
                    "file": "src/Sec.java",
                    "line": 4,
                    "match": '@PreAuthorize("hasRole(\'ADMIN\')")',
                    "rule_id": "security__pre_authorize",
                }
            ],
            "api_surface": [
                {
                    "file": "src/Api.java",
                    "line": 10,
                    "match": '@GetMapping("/api/onboarding")',
                    "rule_id": "api_surface__mapping",
                }
            ],
            "references": [
                {
                    "file": "src/Api.java",
                    "line": 1,
                    "match": "package com.example;",
                    "rule_id": "references__package",
                }
            ],
        },
        "entity_table_map": {
            "User": {
                "file": "src/User.java",
                "table": "users",
                "fqcn": "com.example.User",
                "status": "contested",
                "candidates": [
                    {"file": "src/User.java", "table": "users", "fqcn": "com.example.User"},
                    {"file": "src/b/User.java", "table": "b_users", "fqcn": "com.example.b.User"},
                ],
            }
        },
        "redaction_zones": [{"file": "src/Sec.java", "line": 20, "reason": "credential"}],
        "file_signatures": signatures if signatures is not None else {},
    }
    (run / "spring_signals.json").write_text(json.dumps(signals), encoding="utf-8")
    facts = [
        {
            "predicate": "MAPS_TO",
            "subject": "doc-engine spring . com/example/User#",
            "object": "users",
            "qualifiers": {
                "display_name": "User",
                "fqcn": "com.example.User",
                "symbol_kind": "type",
                "status": "contested",
            },
            "file": "src/User.java",
            "line": 3,
            "rule_id": "persistence__entity",
            "scanner": "ast-grep",
        }
    ]
    (run / "facts.jsonl").write_text(
        "\n".join(json.dumps(f) for f in facts) + "\n", encoding="utf-8"
    )
    return run
