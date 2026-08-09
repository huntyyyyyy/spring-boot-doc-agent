"""Evidence-bucket fact projection for the dual-emit ledger."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from doc_engine.scanning.facts_core import fact


def evidence_hit_fact(
    hit: Mapping[str, Any],
    *,
    bucket: Any,
    default_scanner: Optional[str],
) -> Optional[Dict[str, Any]]:
    file_path = hit.get("file")
    if file_path is None:
        return None
    rule_id = hit.get("rule_id")
    match = hit.get("match")
    return fact(
        predicate=str(rule_id) if rule_id else "EVIDENCE",
        subject=str(file_path),
        object_=None if match is None else str(match),
        qualifiers={"bucket": bucket} if bucket else {},
        file=str(file_path),
        line=hit.get("line") if isinstance(hit.get("line"), int) else None,
        rule_id=None if rule_id is None else str(rule_id),
        scanner=hit.get("scanner") or default_scanner,
    )


def append_evidence_hit(
    facts: List[Dict[str, Any]],
    hit: Any,
    *,
    bucket: Any,
    default_scanner: Optional[str],
) -> None:
    if not isinstance(hit, Mapping):
        return
    row = evidence_hit_fact(hit, bucket=bucket, default_scanner=default_scanner)
    if row is not None:
        facts.append(row)


def facts_from_bucket(
    bucket: Any,
    hits: Any,
    default_scanner: Optional[str],
) -> List[Dict[str, Any]]:
    if not isinstance(hits, list):
        return []
    facts: List[Dict[str, Any]] = []
    for hit in hits:
        append_evidence_hit(
            facts, hit, bucket=bucket, default_scanner=default_scanner,
        )
    return facts


def facts_from_evidence(
    evidence: Mapping[str, Any],
    default_scanner: Optional[str],
) -> List[Dict[str, Any]]:
    facts: List[Dict[str, Any]] = []
    for bucket, hits in evidence.items():
        facts.extend(facts_from_bucket(bucket, hits, default_scanner))
    return facts
