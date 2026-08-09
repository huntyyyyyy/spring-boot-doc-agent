"""Fact record construction helpers for the dual-emit ledger."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Optional

from doc_engine.scanning.symbol import format_type, fqcn_of

PathLike = str | Path


def facts_path_for_signals_out(out_path: PathLike) -> Path:
    """Return sibling ``facts.jsonl`` next to a spring_signals ``--out`` path."""
    return Path(out_path).resolve().parent / "facts.jsonl"


def default_scanner(signals: Mapping[str, Any]) -> Optional[str]:
    scanners = signals.get("scanners") or []
    if not scanners:
        return None
    return ",".join(str(scanner) for scanner in scanners)


def fact(
    *,
    predicate: str,
    subject: str,
    object_: Optional[str] = None,
    qualifiers: Optional[MutableMapping[str, Any]] = None,
    file: Optional[str] = None,
    line: Optional[int] = None,
    rule_id: Optional[str] = None,
    scanner: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "predicate": predicate,
        "subject": subject,
        "object": object_,
        "qualifiers": dict(qualifiers) if qualifiers else {},
        "file": file,
        "line": line,
        "rule_id": rule_id,
        "scanner": scanner,
    }


def sort_key(fact_row: Mapping[str, Any]) -> tuple:
    line = fact_row.get("line")
    return (
        str(fact_row.get("predicate") or ""),
        str(fact_row.get("subject") or ""),
        str(fact_row.get("object") or ""),
        str(fact_row.get("file") or ""),
        -1 if line is None else int(line),
    )


def type_symbol_quals(
    class_name: str,
    source: Mapping[str, Any],
    *,
    base_quals: Optional[MutableMapping[str, Any]] = None,
) -> tuple[str, Dict[str, Any]]:
    """Build type symbol subject + display/fqcn qualifiers from a map entry or candidate."""
    package = source.get("package")
    package_s = str(package) if package is not None else None
    fqcn = source.get("fqcn")
    if fqcn is None:
        fqcn = fqcn_of(package_s, class_name)
    else:
        fqcn = str(fqcn)
    subject = format_type(package_s, class_name)
    quals: Dict[str, Any] = dict(base_quals) if base_quals else {}
    quals["display_name"] = class_name
    quals["fqcn"] = fqcn
    quals["symbol_kind"] = "type"
    return subject, quals
