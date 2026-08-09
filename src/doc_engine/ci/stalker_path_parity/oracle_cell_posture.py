"""G8: local oracle posture vs remote 3.11 Cover% cell (E-TEL2)."""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.stalker_sensors.finding_records import KIND_G8, StalkerFinding


def _missing_policy(policy: Path) -> list[StalkerFinding]:
    return [
        StalkerFinding(
            KIND_G8,
            "oracle_push_policy missing",
            str(policy),
            backlog_pointer="E-HOOK2",
        )
    ]


def _pre_pr_findings(pre_pr: Path, pre_text: str) -> list[StalkerFinding]:
    if "oracle_coverage" in pre_text or "should_remesure_oracle" in pre_text:
        return []
    return [
        StalkerFinding(
            KIND_G8,
            "pre_pr does not wire oracle remesure",
            str(pre_pr),
            backlog_pointer="E-HOOK2",
        )
    ]


def _quality_gates_findings(qg: Path, qg_text: str) -> list[StalkerFinding]:
    if "skip_coverage" not in qg_text or "coverage.xml" in qg_text:
        return []
    return [
        StalkerFinding(
            KIND_G8,
            "quality-gates suite never consults coverage.xml",
            str(qg),
            backlog_pointer="E-HOOK2",
        )
    ]


def scan_oracle_cell_posture(root: Path) -> list[StalkerFinding]:
    """Flag intentional local skip of oracle when quality-gates still skip cov."""
    policy = root / "src/doc_engine/ci/oracle_push_policy.py"
    if not policy.is_file():
        return _missing_policy(policy)
    pre_pr = root / "scripts/ci/pre_pr.py"
    qg = root / "scripts/ci/pre_pr_quality_gates_suite.py"
    pre_text = pre_pr.read_text(encoding="utf-8") if pre_pr.is_file() else ""
    qg_text = qg.read_text(encoding="utf-8") if qg.is_file() else ""
    return _pre_pr_findings(pre_pr, pre_text) + _quality_gates_findings(qg, qg_text)
