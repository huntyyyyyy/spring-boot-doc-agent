"""G1: code SCHEMA_VERSION vs committed ratchet JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G1, StalkerFinding

_PAIRS = (
    ("scripts/ci/check_code_quality.py", "scripts/ratchets/code_quality_baseline.json"),
    ("src/doc_engine/ci/size_ratchet.py", "scripts/ratchets/size_baseline.json"),
    (
        "src/doc_engine/ci/complexity_policy.py",
        "scripts/ratchets/complexipy_baseline.json",
    ),
)
_SCHEMA_ASSIGN = re.compile(r"^SCHEMA_VERSION\s*=\s*(\d+)\s*$", re.M)


def _code_schema_version(path: Path) -> int | None:
    match = _SCHEMA_ASSIGN.search(path.read_text(encoding="utf-8"))
    return int(match.group(1)) if match else None


def _skew_for_pair(root: Path, code_rel: str, json_rel: str) -> StalkerFinding | None:
    code_path = root / code_rel
    json_path = root / json_rel
    if not code_path.is_file() or not json_path.is_file():
        return StalkerFinding(KIND_G1, f"missing pair {code_rel} / {json_rel}", "path absent")
    code_ver = _code_schema_version(code_path)
    if code_ver is None:
        return StalkerFinding(KIND_G1, f"no SCHEMA_VERSION in {code_rel}", code_rel)
    json_ver = json.loads(json_path.read_text(encoding="utf-8")).get("schema_version")
    if code_ver == json_ver:
        return None
    return StalkerFinding(
        KIND_G1,
        f"{code_rel} SCHEMA_VERSION={code_ver} != {json_rel} schema_version={json_ver!r}",
        f"regenerate baseline with --update (code={code_ver})",
    )


def scan_schema_skew(root: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    for code_rel, json_rel in _PAIRS:
        item = _skew_for_pair(root, code_rel, json_rel)
        if item is not None:
            findings.append(item)
    return findings
