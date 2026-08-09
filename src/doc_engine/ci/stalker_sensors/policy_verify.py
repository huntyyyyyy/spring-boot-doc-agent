"""G6: policy verify pack health (imports + baselines parse)."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G6, StalkerFinding

_BASELINES = (
    "scripts/ratchets/code_quality_baseline.json",
    "scripts/ratchets/size_baseline.json",
    "scripts/ratchets/complexipy_baseline.json",
)
_IMPORTS = (
    "doc_engine.ci.size_ratchet",
    "doc_engine.ci.complexipy_ratchet",
)


def _baseline_finding(root: Path, rel: str) -> StalkerFinding | None:
    path = root / rel
    if not path.is_file():
        return StalkerFinding(KIND_G6, f"baseline missing {rel}", rel)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return StalkerFinding(KIND_G6, f"baseline JSON bad {rel}", str(exc))
    if "schema_version" not in data:
        return StalkerFinding(KIND_G6, f"baseline lacks schema_version {rel}", rel)
    return None


def _import_finding(mod_name: str) -> StalkerFinding | None:
    try:
        importlib.import_module(mod_name)
    except Exception as exc:  # noqa: BLE001 — sensor must not crash scan
        return StalkerFinding(KIND_G6, f"import failed {mod_name}", repr(exc))
    return None


def _append_if(findings: list[StalkerFinding], item: StalkerFinding | None) -> None:
    if item is not None:
        findings.append(item)


def scan_policy_verify(root: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    for rel in _BASELINES:
        _append_if(findings, _baseline_finding(root, rel))
    for mod_name in _IMPORTS:
        _append_if(findings, _import_finding(mod_name))
    g2 = root / "tests" / "ci" / "test_g2_prelude_core_scope.py"
    if not g2.is_file():
        findings.append(StalkerFinding(KIND_G6, "G2 witness test missing", str(g2)))
    return findings
