"""Run G1–G6 sensors and optional ledger write."""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.stalker_sensors.collect_syntax import scan_collect_syntax
from doc_engine.ci.stalker_sensors.facade_api import scan_facade_api
from doc_engine.ci.stalker_sensors.finding_records import StalkerFinding
from doc_engine.ci.stalker_sensors.ledger_write import write_findings_ledger
from doc_engine.ci.stalker_sensors.parallel_tip import scan_parallel_tip
from doc_engine.ci.stalker_sensors.policy_verify import scan_policy_verify
from doc_engine.ci.stalker_sensors.schema_skew import scan_schema_skew
from doc_engine.ci.stalker_sensors.split_scope import scan_split_scope


def run_all_sensors(root: Path) -> list[StalkerFinding]:
    findings: list[StalkerFinding] = []
    findings.extend(scan_schema_skew(root))
    findings.extend(scan_split_scope(root))
    findings.extend(scan_facade_api(root))
    findings.extend(scan_collect_syntax(root))
    findings.extend(scan_parallel_tip(root))
    findings.extend(scan_policy_verify(root))
    return findings


def scan_and_write(root: Path, *, write_ledger: bool = True) -> list[StalkerFinding]:
    findings = run_all_sensors(root)
    if write_ledger:
        write_findings_ledger(root, findings)
    return findings
