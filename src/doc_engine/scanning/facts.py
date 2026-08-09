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
    facts_path_for_signals_out,
)
from doc_engine.scanning.facts_core import (
    default_scanner as _default_scanner,
)
from doc_engine.scanning.facts_core import (
    sort_key as _sort_key,
)
from doc_engine.scanning.facts_covering import covering_writer_facts
from doc_engine.scanning.facts_emit import fact_emit_counts, write_facts_jsonl
from doc_engine.scanning.facts_evidence import (
    facts_from_evidence as _facts_from_evidence,
)
from doc_engine.scanning.facts_maps_to import (
    maps_to_from_entity_table_map as _maps_to_from_entity_table_map,
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
