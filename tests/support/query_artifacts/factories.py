"""Factories for query_artifacts suite payloads."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from doc_engine.query.envelope import QUERY_RESULT_SCHEMA_VERSION, apply_limit
from doc_engine.query.handlers import dependents, entity, evidence, facts, routes
from doc_engine.query.load import QueryError, QueryMissingError, QueryPathError, load_json, load_jsonl
from doc_engine.query.registry import get_query_handler, run_query
from doc_engine.real_fixture import real_artifacts_dir
FIXTURE_SIGNALS = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "fixtures"
    / "spring_signals"
)

def _signals_doc() -> dict:
    return {
        "schema_version": 2,
        "scanners": ["ast-grep"],
        "evidence": {
            "api_surface": [
                {
                    "file": "src/AController.java",
                    "line": 10,
                    "match": '@GetMapping("/api/a")',
                    "rule_id": "api_surface__mapping",
                },
                {
                    "file": "src/BController.java",
                    "line": 20,
                    "match": '@PostMapping("/api/b")',
                    "rule_id": "api_surface__mapping",
                },
                {
                    "file": "src/AController.java",
                    "line": 1,
                    "match": "@RestController",
                    "rule_id": "api_surface__controller",
                },
            ],
            "security": [
                {
                    "file": "src/AController.java",
                    "line": 9,
                    "match": '@PreAuthorize("hasRole(\'ADMIN\')")',
                    "rule_id": "security__pre_authorize",
                },
            ],
            "persistence": [
                {
                    "file": "src/User.java",
                    "line": 3,
                    "match": "@Entity",
                    "rule_id": "persistence__entity",
                },
            ],
            "references": [
                {
                    "file": "src/AController.java",
                    "line": 1,
                    "match": "package com.example.web;",
                    "rule_id": "references__package",
                },
                {
                    "file": "src/User.java",
                    "line": 1,
                    "match": "package com.example.domain;",
                    "rule_id": "references__package",
                },
                {
                    "file": "src/AController.java",
                    "line": 2,
                    "match": "import com.example.domain.User;",
                    "rule_id": "references__import",
                },
            ],
        },
        "entity_table_map": {
            "User": {
                "file": "src/User.java",
                "table": "users",
                "table_name_source": "annotation",
                "package": "com.example.domain",
                "fqcn": "com.example.domain.User",
                "status": "unique",
                "candidates": [],
            },
            "Order": {
                "file": "pkg_a/Order.java",
                "table": "a_order",
                "table_name_source": "annotation",
                "package": "com.example.a",
                "fqcn": "com.example.a.Order",
                "status": "contested",
                "candidates": [
                    {
                        "file": "pkg_a/Order.java",
                        "table": "a_order",
                        "package": "com.example.a",
                        "fqcn": "com.example.a.Order",
                    },
                    {
                        "file": "pkg_b/Order.java",
                        "table": "b_order",
                        "package": "com.example.b",
                        "fqcn": "com.example.b.Order",
                    },
                ],
            },
        },
    }


def _facts_rows() -> list[dict]:
    return [
        {
            "predicate": "MAPS_TO",
            "subject": "doc-engine spring . com/example/domain/User#",
            "object": "users",
            "qualifiers": {
                "display_name": "User",
                "fqcn": "com.example.domain.User",
                "symbol_kind": "type",
            },
            "file": "src/User.java",
            "line": 3,
            "rule_id": "persistence__entity",
            "scanner": "ast-grep",
        },
        {
            "predicate": "persistence__entity",
            "subject": "src/User.java",
            "object": "@Entity",
            "qualifiers": {},
            "file": "src/User.java",
            "line": 3,
            "rule_id": "persistence__entity",
            "scanner": "ast-grep",
        },
    ]
