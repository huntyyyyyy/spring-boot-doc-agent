"""Coverage climb B5: recall_delta + gap_probe join/collision miss edges."""
from __future__ import annotations
from typing import Any
import pytest
from doc_engine.scanning import recall_delta as rd
from doc_engine.scanning.gap_probe import join as join_mod
from doc_engine.scanning.gap_probe import symbol_collision as coll_mod
from doc_engine.scanning.symbol import format_field, format_type
pytestmark = pytest.mark.domain_climb_sensor

def _test_join_identity_and_unmatched_edges_prelude():
    keys: set[str] = set()
    join_mod._add_display_keys(keys, None, 'com.acme')
    assert keys == set()
    assert join_mod._subject_package('not-a-symbol') is None
    type_subj = format_type('com.acme', 'Order')
    assert join_mod._subject_package(type_subj) == 'com.acme'
    assert join_mod._subject_package(format_type(None, 'Solo')) is None
    assert join_mod._fact_identity_keys({'qualifiers': ['bad']}) == set()
    assert join_mod._contested_candidate_sources({'candidates': []})[0]['candidates'] == []
    assert join_mod._contested_candidate_sources({'candidates': 'x'})[0]['candidates'] == 'x'
    fallback = join_mod._contested_candidate_sources({'status': 'contested', 'candidates': ['x', 1]})
    assert fallback[0]['status'] == 'contested'
    expanded = join_mod._entity_join_sources({'status': 'contested', 'candidates': [{'fqcn': 'com.acme.A'}, {'fqcn': 'com.acme.B'}]})
    assert len(expanded) == 2
    matched, failure = join_mod._score_one_entity('X', 'not-map', set())
    assert matched is False and failure is None

def _test_join_identity_and_unmatched_edges_core():
    type_sym = format_type('com.acme', 'Order')
    facts: list[dict[str, Any]] = [{'predicate': 'MAPS_TO', 'subject': type_sym, 'object': 'orders', 'qualifiers': {'fqcn': 'com.acme.Order', 'display_name': 'Order'}}]
    report = join_mod.measure_r_join({'entity_table_map': {'Order': {'fqcn': 'com.acme.Order', 'package': 'com.acme', 'file': 'Order.java'}, 'Orphan': {'file': 'Orphan.java'}, 'Bad': 'skip', 'Dup': {'status': 'contested', 'file': 'Dup.java', 'candidates': [{'fqcn': 'com.acme.Order', 'package': 'com.acme'}]}}}, facts)
    assert report['numerator'] >= 2
    assert any((f['simple_name'] == 'Orphan' for f in report['failures']))
    bad_map = join_mod.measure_r_join({'entity_table_map': 123}, facts)
    assert bad_map['denominator'] == 0

def test_recall_delta_entity_keys_and_verdicts() -> None:
    keys = rd._entity_keys({'entity_table_map': {'Order': {'fqcn': 'com.acme.Order'}}, 'entity_table_map_candidates': {'Legacy': {}}})
    assert keys == {'Order', 'Legacy'}
    assert rd._entity_keys({}) == set()
    assert rd._recall_verdict({}, name='X', oracle_arm='multipass') == 'STRUCTURAL'
    signals = {'entity_table_map': {'User': {'fqcn': 'com.acme.User', 'file': 'U.java'}}}
    assert rd._recall_verdict(signals, name='User', oracle_arm='codeql') == 'STRUCTURAL'
    assert rd._recall_verdict(signals, name='FooImpl', oracle_arm='codeql') == 'EVIDENTIARY'
    assert rd._recall_verdict(signals, name='Other', oracle_arm='codeql') == 'STRUCTURAL'
    facts = rd.write_recall_miss_facts(signals, native_entity_keys=set(), oracle_entity_keys={'User'}, oracle_arm='codeql')
    assert facts[0]['qualifiers']['verdict'] == 'STRUCTURAL'
    assert rd.write_recall_miss_facts({}, native_entity_keys=set(), oracle_entity_keys=set(), oracle_arm='codeql') == []

def test_collect_arm_entity_keys_branches() -> None:
    native, oracle, arm = rd.collect_arm_entity_keys([{'entity_table_map': {'A': {}}}, {'entity_table_map': {'B': {}}}, {'entity_table_map': {'C': {}}}], scanner_names=['ast-grep', 'codeql', 'semgrep'])
    assert native == {'A'}
    assert oracle == {'B'}
    assert arm == 'codeql'

def test_symbol_collision_non_type_and_bad_map() -> None:
    field = format_field('com.acme', 'User', 'email')
    out = coll_mod.measure_r_sym([{'predicate': 'MAPS_TO', 'subject': field, 'object': 'users', 'file': 'User.java'}])
    assert out['failures']
    assert out['failures'][0]['reason_class'] == 'unparseable_or_non_type'
    contested = coll_mod.measure_r_coll({'entity_table_map': {'SkipMe': 'not-a-mapping', 'Dup': {'status': 'contested', 'candidates': [{}, {}], 'file': 'D.java'}}})
    assert contested['numerator'] == 1
    assert len(contested['failures']) == 1
    empty = coll_mod.measure_r_coll({'entity_table_map': ['not', 'a', 'map']})
    assert empty['denominator'] == 0

def test_join_identity_and_unmatched_edges() -> None:
    _test_join_identity_and_unmatched_edges_prelude()
    _test_join_identity_and_unmatched_edges_core()
