"""Run Rust ast-grep vacuity rules over test trees."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

# Rules ship beside this module (not via repo-relative path) so plant trees
# under pytest tmp_path still load the same YAML tip CI uses.
RULES_FILE = Path(__file__).with_name("astgrep_rules.yml")
DEFAULT_ROOTS = ("tests/ci", "tests/adapters")


@dataclass(frozen=True)
class VacuityHit:
    """One vacuous structural match."""

    rule_id: str
    path: str
    line: int
    text: str


def rules_path(_repo: Path | None = None) -> Path:
    return RULES_FILE


def run_astgrep_vacuity(
    repo: Path,
    roots: Sequence[str] = DEFAULT_ROOTS,
    *,
    ast_grep: str = "ast-grep",
) -> list[VacuityHit]:
    """Invoke ast-grep scan --json=compact; tool errors are hard findings."""
    rule = rules_path(repo)
    if not rule.is_file():
        return [
            VacuityHit(
                "vacuous__missing_rules",
                str(rule),
                0,
                "astgrep_rules.yml missing",
            )
        ]
    targets = [str(repo / root) for root in roots if (repo / root).is_dir()]
    if not targets:
        return []
    completed = subprocess.run(
        [
            ast_grep,
            "scan",
            "-r",
            str(rule),
            "--json=compact",
            *targets,
        ],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        return [
            VacuityHit(
                "vacuous__astgrep_error",
                "ast-grep",
                0,
                (completed.stderr or completed.stdout or "ast-grep failed")[:500],
            )
        ]
    return list(_parse_compact_json(completed.stdout))


def _parse_compact_json(stdout: str) -> Iterable[VacuityHit]:
    text = stdout.strip()
    if not text:
        return []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return list(_parse_ndjson(text))
    return _hits_from_payload(payload)


def _hits_from_payload(payload: object) -> list[VacuityHit]:
    if isinstance(payload, list):
        return [_hit_from_row(row) for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        return [_hit_from_row(payload)]
    return []


def _parse_ndjson(text: str) -> Iterable[VacuityHit]:
    for line in text.splitlines():
        row = _load_json_object(line.strip())
        if row is not None:
            yield _hit_from_row(row)


def _load_json_object(line: str) -> dict | None:
    if not line:
        return None
    try:
        row = json.loads(line)
    except json.JSONDecodeError:
        return None
    return row if isinstance(row, dict) else None


def _range_start_line(row: dict) -> int:
    range_obj = row.get("range")
    if not isinstance(range_obj, dict):
        return int(row.get("line") or 0)
    start_obj = range_obj.get("start")
    if not isinstance(start_obj, dict):
        return int(row.get("line") or 0)
    # ast-grep lines are 0-based in range.start.line
    return int(start_obj.get("line", 0)) + 1


def _hit_from_row(row: dict) -> VacuityHit:
    return VacuityHit(
        rule_id=str(row.get("ruleId") or row.get("id") or "vacuous__unknown"),
        path=str(row.get("file") or row.get("path") or ""),
        line=_range_start_line(row),
        text=str(row.get("text") or row.get("lines") or "")[:200],
    )
