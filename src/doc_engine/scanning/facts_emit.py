"""Write-time validation and emit counters for facts.jsonl."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping

from doc_engine.scanning.facts_core import PathLike
from doc_engine.scanning.symbol import SymbolError, parse

EMIT_COUNT_KEYS = {
    "ABSENCE": "facts_absence",
    "UNPROVEN": "facts_unproven",
    "RECALL_MISS": "facts_recall_miss",
}


def require_maps_to_type_symbol(fact_row: Mapping[str, Any]) -> None:
    if fact_row.get("predicate") != "MAPS_TO":
        return
    subject = fact_row.get("subject")
    try:
        parsed = parse(str(subject))
    except SymbolError as exc:
        raise SymbolError(
            f"MAPS_TO subject is not a claim-symbol: {subject!r}"
        ) from exc
    if parsed.kind != "type":
        raise SymbolError(
            f"MAPS_TO subject must be a type symbol, got kind={parsed.kind!r}: {subject!r}"
        )


def write_facts_jsonl(path: PathLike, facts: List[Mapping[str, Any]]) -> None:
    """Write fact records as UTF-8 JSON Lines (one object per line).

    Each row is validated against the closed ``Fact`` contract before encode
    (write-time bite; see schema-contracts-decision-memo-2026-07-30 slice 1).

    ``MAPS_TO`` subjects must parse as claim-symbols (grammar memo); bare
    simple names / FQCNs are rejected so illegal identity cannot land on disk.
    """
    from doc_engine.pipeline.artifacts import Fact

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        for fact_row in facts:
            require_maps_to_type_symbol(fact_row)
            validated = Fact.model_validate(dict(fact_row)).model_dump()
            fh.write(json.dumps(validated, ensure_ascii=False, sort_keys=True))
            fh.write("\n")


def bump_maps_to_count(counts: Dict[str, int], fact_row: Mapping[str, Any]) -> None:
    counts["facts_maps_to"] += 1
    quals = fact_row.get("qualifiers") or {}
    if isinstance(quals, Mapping) and quals.get("status") == "contested":
        counts["facts_maps_to_contested"] += 1


def bump_emit_count(counts: Dict[str, int], fact_row: Mapping[str, Any]) -> None:
    predicate = fact_row.get("predicate")
    if predicate == "MAPS_TO":
        bump_maps_to_count(counts, fact_row)
        return
    key = EMIT_COUNT_KEYS.get(str(predicate) if predicate is not None else "")
    if key is None:
        counts["facts_evidence"] += 1
        return
    counts[key] += 1


def fact_emit_counts(facts: List[Mapping[str, Any]]) -> Dict[str, int]:
    """Return counters for dual-emit observability (gap/error analysis)."""
    counts = {
        "facts_total": len(facts),
        "facts_maps_to": 0,
        "facts_maps_to_contested": 0,
        "facts_evidence": 0,
        "facts_absence": 0,
        "facts_unproven": 0,
        "facts_recall_miss": 0,
    }
    for fact_row in facts:
        bump_emit_count(counts, fact_row)
    return counts
