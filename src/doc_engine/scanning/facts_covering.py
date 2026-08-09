"""Covering / absence / recall fact writers for the dual-emit ledger."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional


def astgrep_receipt_complete(proof: Mapping[str, Any]) -> bool:
    for receipt in proof.get("receipts") or []:
        if (
            isinstance(receipt, Mapping)
            and receipt.get("scanner") == "ast-grep"
            and receipt.get("status") == "complete"
        ):
            return True
    return False


def covering_state(signals: Mapping[str, Any]) -> tuple[bool, Optional[str], bool]:
    """Return (covering_ok, covering_root, astgrep_receipt_complete)."""
    from doc_engine.scanning.covering import verify_covering_proof

    proof = signals.get("_covering_proof")
    if not isinstance(proof, Mapping):
        return False, None, False
    covering_root = proof.get("inventory_root")
    scanner_version = signals.get("scanner_version")
    sigs = signals.get("file_signatures") or {}
    covering_ok = False
    if isinstance(sigs, Mapping) and scanner_version:
        covering_ok, _ = verify_covering_proof(
            proof,
            file_signatures=sigs,
            scanner_version=str(scanner_version),
        )
    return (
        covering_ok,
        covering_root if isinstance(covering_root, str) else None,
        astgrep_receipt_complete(proof),
    )


def first_oracle_arm(
    entity_keys: Mapping[str, Any],
) -> Optional[tuple[str, set[str]]]:
    for arm in ("codeql", "multipass", "metamodel"):
        oracle = set(entity_keys.get(arm) or [])
        if oracle:
            return arm, oracle
    return None


def recall_facts_from_meta(
    signals: Mapping[str, Any],
    meta: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    from doc_engine.scanning.recall_delta import write_recall_miss_facts

    entity_keys = meta.get("entity_keys_by_scanner") or {}
    if not isinstance(entity_keys, Mapping):
        return []
    selected = first_oracle_arm(entity_keys)
    if selected is None:
        return []
    arm, oracle = selected
    return write_recall_miss_facts(
        signals,
        native_entity_keys=set(entity_keys.get("ast-grep") or []),
        oracle_entity_keys=oracle,
        oracle_arm=arm,
    )


def covering_writer_facts(signals: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """ABSENCE/UNPROVEN + RECALL_MISS from covering proof + per-arm entity keys.

    Internal keys ``_covering_proof`` / ``_scan_partials_meta`` are consumed when
    present (orchestrator). Without a proof, absence stamps are all UNPROVEN and
    recall is omitted.
    """
    from doc_engine.scanning.absence import write_absence_facts

    covering_ok, covering_root, astgrep_ok = covering_state(signals)
    scanner_version = signals.get("scanner_version")
    facts = write_absence_facts(
        signals,
        covering_ok=covering_ok,
        covering_root=covering_root,
        scanner_version=str(scanner_version) if scanner_version else None,
        astgrep_receipt_complete=astgrep_ok,
    )
    meta = signals.get("_scan_partials_meta") or {}
    if isinstance(meta, Mapping):
        facts.extend(recall_facts_from_meta(signals, meta))
    return facts
