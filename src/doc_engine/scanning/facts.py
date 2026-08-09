"""Project spring_signals.json into a thin dual-emit fact ledger (facts.jsonl).

Phase 1 sidecar: does not replace entity_table_map or evidence bags.
See claude/research/fact-store-phase1-decision-memo-2026-07-30.md §3.

L3: MAPS_TO subjects are SCIP-inspired type symbols (see scanning.symbol);
Path A entity_table_map keys remain simple class names.

Concept modules: ``facts_core``, ``facts_maps_to``, ``facts_evidence``,
``facts_covering``, ``facts_emit``. This façade keeps the stable
``doc_engine.scanning.facts`` import path.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

from doc_engine.scanning.facts_core import (
    PathLike,
    default_scanner as _default_scanner,
    fact as _fact,
    facts_path_for_signals_out,
    sort_key as _sort_key,
    type_symbol_quals as _type_symbol_quals,
)
from doc_engine.scanning.facts_covering import (
    astgrep_receipt_complete as _astgrep_receipt_complete,
    covering_state as _covering_state,
    covering_writer_facts,
    first_oracle_arm as _first_oracle_arm,
    recall_facts_from_meta as _recall_facts_from_meta,
)
from doc_engine.scanning.facts_emit import (
    EMIT_COUNT_KEYS as _EMIT_COUNT_KEYS,
    bump_emit_count as _bump_emit_count,
    bump_maps_to_count as _bump_maps_to_count,
    fact_emit_counts,
    require_maps_to_type_symbol as _require_maps_to_type_symbol,
    write_facts_jsonl,
)
from doc_engine.scanning.facts_evidence import (
    append_evidence_hit as _append_evidence_hit,
    evidence_hit_fact as _evidence_hit_fact,
    facts_from_bucket as _facts_from_bucket,
    facts_from_evidence as _facts_from_evidence,
)
from doc_engine.scanning.facts_maps_to import (
    contested_table_name_source as _contested_table_name_source,
    is_contested_entry as _is_contested_entry,
    maps_to_fact_from_source as _maps_to_fact_from_source,
    maps_to_from_contested_entry as _maps_to_from_contested_entry,
    maps_to_from_entity_table_map as _maps_to_from_entity_table_map,
    maps_to_from_one_entry as _maps_to_from_one_entry,
    maps_to_from_settled_entry as _maps_to_from_settled_entry,
)


def facts_from_signals(signals: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """Project a spring_signals dict into sorted fact records."""
    default_scanner = _default_scanner(signals)
    facts: List[Dict[str, Any]] = []
    evidence = signals.get("evidence") or {}
    if isinstance(evidence, Mapping):
        facts.extend(_facts_from_evidence(evidence, default_scanner))
    entity_table_map = signals.get("entity_table_map") or {}
    if isinstance(entity_table_map, Mapping):
        facts.extend(_maps_to_from_entity_table_map(entity_table_map, default_scanner))
    facts.extend(covering_writer_facts(signals))
    facts.sort(key=_sort_key)
    return facts


__all__ = [
    "PathLike",
    "covering_writer_facts",
    "fact_emit_counts",
    "facts_from_signals",
    "facts_path_for_signals_out",
    "write_facts_jsonl",
]
