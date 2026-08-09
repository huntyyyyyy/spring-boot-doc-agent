"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: _w, _wb, _controller, _service, _entity."""

from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS
from doc_engine.pipeline.mock_stages import (
    find_existing_readme,
    load_citations,
    mock_architecture,
    mock_docs,
    mock_file_summaries,
    mock_gap_and_interview,
    sweep_todos,
)
from doc_engine.tools import partition_repo, run_manifest, spring_signal_scan
from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES
from doc_engine.scanning.covering import verify_covering_proof
SCRIPT_DIR = SCRIPTS_DIR
PY = sys.executable
MAX_TOKENS = "2000"
SMALL_FILE_BYTES = "4096"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
BILLING = "services/billing-service/src/main/java/com/acme/billing"
LEDGER = "services/ledger-service/src/main/java/com/acme/ledger"
LEGACY = "services/legacy-batch/src/main/java/com/acme/legacy"
RES = "services/billing-service/src/main/resources"
TWO_ENTITIES = f"{BILLING}/TwoEntities.java"
MIXED_ENTITIES = f"{BILLING}/MixedEntities.java"
NESTED_ENTITY = f"{BILLING}/NestedEntity.java"
DUP_BILLING = f"{BILLING}/Invoice.java"
DUP_LEDGER = f"{LEDGER}/Invoice.java"
UNICODE_QUERY = f"{LEDGER}/LedgerRepository.java"
HUGE_JAVA = f"{LEGACY}/Huge.java"
EMPTY_JAVA = f"{LEGACY}/Empty.java"
LATIN1_JAVA = f"{LEGACY}/Latin1.java"
NUL_JAVA = f"{LEGACY}/NulInside.java"
CRLF_JAVA = f"{LEGACY}/Crlf.java"
BOM_YML = f"{RES}/application-prod.yml"
NOBOM_YML = f"{RES}/application-nobom.yml"
PLACEHOLDER_YML = f"{RES}/application.yml"
SECRETS_YML = f"{RES}/application-secrets.yml"
MULTI_SEG_YML = f"{RES}/application-dev-local.yml"
CRLF_PROPS = f"{RES}/application-legacy.properties"
LF_PROPS = f"{RES}/application-lfprops.properties"
EMPTY_YML = f"{RES}/application-empty.yml"
SPACE_PATH = "docs and notes/guide.md"
UNICODE_DIR_JAVA = "módulo-común/src/main/java/com/acme/uni/UniController.java"
DEEP_JAVA = "deep/" + "/".join(f"l{i:02d}" for i in range(30)) + "/Leaf.java"
GITIGNORED_DIR = "generated"
PLANTED_EXCLUDED_DIRS = ["target", "build", "node_modules", "vendor", "venv",
                         "dist", "out", "coverage"]
_STATE = {}

def _w(root, rel, text):
    path = os.path.join(root, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _wb(root, rel, data):
    """Bytes, for the files whose whole point is their encoding — never text
    mode, since the default encoding is exactly what is under test."""
    path = os.path.join(root, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def _controller(pkg, name, seg):
    return f"""package {pkg};

import org.springframework.web.bind.annotation.*;
import org.springframework.security.access.prepost.PreAuthorize;

@RestController
@RequestMapping("/api/{seg}")
public class {name} {{
    @GetMapping("/{{id}}")
    @PreAuthorize(
        "hasRole('{seg.upper()}_READ')"
    )
    public String get(@PathVariable Long id) {{ return "ok"; }}

    @PostMapping
    public String create(@RequestBody String body) {{
        // TODO: validate payload before persisting
        return "created";
    }}
}}
"""


def _service(pkg, name):
    return (f"package {pkg};\n\nimport org.springframework.stereotype.Service;\n\n"
            f"@Service\npublic class {name} {{\n"
            f"    public String handle(String in) {{ return in.trim(); }}\n}}\n")


def _entity(pkg, name, table):
    return (f"package {pkg};\n\nimport jakarta.persistence.*;\n\n"
            f"@Entity\n@Table(name = \"{table}\")\npublic class {name} {{\n"
            f"    @Id\n    private Long id;\n    private String status;\n}}\n")
