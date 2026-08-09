"""Project spring_signals.json into a thin dual-emit fact ledger (facts.jsonl).

Phase 1 sidecar: does not replace entity_table_map or evidence bags.
See claude/research/fact-store-phase1-decision-memo-2026-07-30.md §3.

L3: MAPS_TO subjects are SCIP-inspired type symbols (see scanning.symbol);
Path A entity_table_map keys remain simple class names.

Concept modules: ``facts_core``, ``facts_maps_to``, ``facts_evidence``,
``facts_covering``, ``facts_emit``. This façade keeps the stable
``doc_engine.scanning.facts`` import path (including climb-poked ``_`` aliases).
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

from doc_engine.scanning.facts_core import (
    PathLike,
    facts_path_for_signals_out,
)
from doc_engine.scanning.facts_core import (
    default_scanner as _default_scanner,
)
from doc_engine.scanning.facts_core import (
    fact as _fact,
)
from doc_engine.scanning.facts_core import (
    sort_key as _sort_key,
)
from doc_engine.scanning.facts_core import (
    type_symbol_quals as _type_symbol_quals,
)
from doc_engine.scanning.facts_covering import (
    astgrep_receipt_complete as _astgrep_receipt_complete,
)
from doc_engine.scanning.facts_covering import (
    covering_state as _covering_state,
)
from doc_engine.scanning.facts_covering import (
    covering_writer_facts,
)
from doc_engine.scanning.facts_covering import (
    first_oracle_arm as _first_oracle_arm,
)
from doc_engine.scanning.facts_covering import (
    recall_facts_from_meta as _recall_facts_from_meta,
)
from doc_engine.scanning.facts_emit import (
    EMIT_COUNT_KEYS as _EMIT_COUNT_KEYS,
)
from doc_engine.scanning.facts_emit import (
    bump_emit_count as _bump_emit_count,
)
from doc_engine.scanning.facts_emit import (
    bump_maps_to_count as _bump_maps_to_count,
)
from doc_engine.scanning.facts_emit import (
    fact_emit_counts,
    write_facts_jsonl,
)
from doc_engine.scanning.facts_emit import (
    require_maps_to_type_symbol as _require_maps_to_type_symbol,
)
from doc_engine.scanning.facts_evidence import (
    append_evidence_hit as _append_evidence_hit,
)
from doc_engine.scanning.facts_evidence import (
    evidence_hit_fact as _evidence_hit_fact,
)
from doc_engine.scanning.facts_evidence import (
    facts_from_bucket as _facts_from_bucket,
)
from doc_engine.scanning.facts_evidence import (
    facts_from_evidence as _facts_from_evidence,
)
from doc_engine.scanning.facts_maps_to import (
    contested_table_name_source as _contested_table_name_source,
)
from doc_engine.scanning.facts_maps_to import (
    is_contested_entry as _is_contested_entry,
)
from doc_engine.scanning.facts_maps_to import (
    maps_to_fact_from_source as _maps_to_fact_from_source,
)
from doc_engine.scanning.facts_maps_to import (
    maps_to_from_contested_entry as _maps_to_from_contested_entry,
)
from doc_engine.scanning.facts_maps_to import (
    maps_to_from_entity_table_map as _maps_to_from_entity_table_map,
)
from doc_engine.scanning.facts_maps_to import (
    maps_to_from_one_entry as _maps_to_from_one_entry,
)
from doc_engine.scanning.facts_maps_to import (
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
    "_EMIT_COUNT_KEYS",
    "_append_evidence_hit",
    "_astgrep_receipt_complete",
    "_bump_emit_count",
    "_bump_maps_to_count",
    "_contested_table_name_source",
    "_covering_state",
    "_default_scanner",
    "_evidence_hit_fact",
    "_fact",
    "_facts_from_bucket",
    "_facts_from_evidence",
    "_first_oracle_arm",
    "_is_contested_entry",
    "_maps_to_fact_from_source",
    "_maps_to_from_contested_entry",
    "_maps_to_from_entity_table_map",
    "_maps_to_from_one_entry",
    "_maps_to_from_settled_entry",
    "_recall_facts_from_meta",
    "_require_maps_to_type_symbol",
    "_sort_key",
    "_type_symbol_quals",
]
