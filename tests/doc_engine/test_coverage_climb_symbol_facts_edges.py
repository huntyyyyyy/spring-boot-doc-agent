"""Coverage climb: claim-symbol + facts ledger miss edges."""
from __future__ import annotations
from pathlib import Path
import pytest
from doc_engine.scanning import facts as facts_mod
from doc_engine.scanning import symbol as sym
pytestmark = pytest.mark.domain_climb_sensor

def _test_symbol_parse_member_error_paths_prelude(monkeypatch: pytest.MonkeyPatch):
    with pytest.raises(sym.SymbolError):
        sym._strip_method_member('nohash().', 'bad')
    with pytest.raises(sym.SymbolError):
        sym._strip_method_member('Outer#notmethod.', 'bad')
    with pytest.raises(sym.SymbolError):
        sym._strip_field_member('Outer#bad().', 'bad')
    none_member, unchanged = sym._strip_field_member('Outer#.', 'sym')
    assert none_member is None and unchanged == 'Outer#.'
    kind, member, body = sym._split_member_suffix('Outer#', 'x')
    assert kind == 'type' and member is None and (body == 'Outer#')
    assert sym._split_ns_and_type_part('Outer#') == ((), 'Outer#')
    with pytest.raises(sym.SymbolError):
        sym._parse_type_names('Outer', 'sym')
    with pytest.raises(sym.SymbolError):
        sym._parse_type_names('#', 'sym')
    field = sym.format_field(None, 'User', 'email')
    return field

def _test_symbol_parse_member_error_paths_core(monkeypatch: pytest.MonkeyPatch, field):
    assert sym.display(field) == 'User.email'
    method = sym.format_method(None, 'User', 'run')
    assert sym.display(method).endswith('()')
    assert sym.fqcn_of(None, 'Solo') == 'Solo'
    with pytest.raises(sym.SymbolError):
        sym.parse('not-a-claim-symbol')
    with pytest.raises(sym.SymbolError):
        sym._split_package_segments('')
    forged = sym.ParsedSymbol(kind='other', namespaces=(), type_names=('X',))
    monkeypatch.setattr(sym, 'parse', lambda _s: forged)
    with pytest.raises(sym.SymbolError, match='unknown kind'):
        sym.display('anything')
    assert sym.fqcn_of('com.acme', 'User') == 'com.acme.User'

def _test_covering_and_recall_and_maps_to_guard_prelude(tmp_path: Path):
    assert facts_mod._astgrep_receipt_complete({}) is False
    assert facts_mod._astgrep_receipt_complete({'receipts': [{'scanner': 'ast-grep', 'status': 'complete'}]})
    ok, root, astg = facts_mod._covering_state({'_covering_proof': 'bad'})
    assert ok is False and root is None and (astg is False)
    assert facts_mod._first_oracle_arm({}) is None
    assert facts_mod._first_oracle_arm({'codeql': ['A']})[0] == 'codeql'
    assert facts_mod._recall_facts_from_meta({}, {'entity_keys_by_scanner': 'bad'}) == []
    assert facts_mod._recall_facts_from_meta({}, {'entity_keys_by_scanner': {}}) == []
    out = facts_mod.facts_from_signals({'evidence': {}, 'entity_table_map': {}, 'scanner_version': 'v1'})
    assert isinstance(out, list)
    assert facts_mod._facts_from_evidence({}, None) == []
    assert facts_mod._maps_to_from_entity_table_map({}, None) == []
    with pytest.raises(sym.SymbolError):
        facts_mod._require_maps_to_type_symbol({'predicate': 'MAPS_TO', 'subject': 'not-a-symbol'})
    field_subj = sym.format_field('com.acme', 'User', 'email')
    return field_subj

def _test_covering_and_recall_and_maps_to_guard_core(tmp_path: Path, field_subj):
    with pytest.raises(sym.SymbolError, match='type symbol'):
        facts_mod._require_maps_to_type_symbol({'predicate': 'MAPS_TO', 'subject': field_subj})
    facts_mod._require_maps_to_type_symbol({'predicate': 'OTHER', 'subject': 'x'})
    path = tmp_path / 'facts.jsonl'
    type_sym = sym.format_type('com.acme', 'User')
    facts_mod.write_facts_jsonl(path, [{'predicate': 'MAPS_TO', 'subject': type_sym, 'object': 'users', 'qualifiers': {}, 'file': 'User.java', 'line': 1, 'rule_id': 'persistence__entity', 'scanner': 'ast-grep'}])
    assert path.is_file()

def test_symbol_validation_and_package_edges() -> None:
    assert sym.ParsedSymbol(kind='type', namespaces=(), type_names=('Solo',)).fqcn == 'Solo'
    with pytest.raises(sym.SymbolError):
        sym._validate_java_ident('', what='type name')
    with pytest.raises(sym.SymbolError):
        sym._validate_java_ident('1bad', what='type name')
    with pytest.raises(sym.SymbolError):
        sym._validate_java_ident('bad-name', what='type name')
    with pytest.raises(sym.SymbolError):
        sym._split_package_segments('.com.acme')
    with pytest.raises(sym.SymbolError):
        sym._split_package_segments('com..acme')
    assert sym._namespaces_from_package(None) == ()
    assert sym._namespaces_from_package('') == ()
    assert sym._path_prefix((), ('Order',)) == 'Order#'
    assert 'acme' in sym._path_prefix(('com', 'acme'), ('User',))

def test_symbol_parse_member_error_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    field = _test_symbol_parse_member_error_paths_prelude(monkeypatch)
    _test_symbol_parse_member_error_paths_core(monkeypatch, field)

def test_facts_maps_to_and_evidence_skips() -> None:
    contested = facts_mod._maps_to_from_contested_entry('User', {'rule_id': 'persistence__entity'}, [{'table': 'u'}, 'skip-me', {'table': 'v', 'table_name_source': 'ann'}], 'ast-grep')
    assert len(contested) == 2
    assert all((f['predicate'] == 'MAPS_TO' for f in contested))
    settled = facts_mod._maps_to_from_settled_entry('User', {'table': 'users', 'status': 'ok', 'table_name_source': 'ann'}, 'ast-grep')
    assert settled['qualifiers']['status'] == 'ok'
    assert facts_mod._maps_to_from_one_entry('X', 'not-a-map', None) == []
    assert facts_mod._maps_to_from_one_entry('X', {'status': 'contested', 'candidates': [{'table': 't'}]}, None)
    assert facts_mod._evidence_hit_fact({}, bucket='api', default_scanner=None) is None
    facts_mod._append_evidence_hit([], 'bad', bucket='api', default_scanner=None)
    assert facts_mod._facts_from_bucket('api', 'not-list', None) == []
    rows = facts_mod._facts_from_bucket('api', [{'file': 'A.java', 'line': 1, 'match': 'm', 'rule_id': 'api__x'}], 'ast-grep')
    assert len(rows) == 1

def test_covering_and_recall_and_maps_to_guard(tmp_path: Path) -> None:
    field_subj = _test_covering_and_recall_and_maps_to_guard_prelude(tmp_path)
    _test_covering_and_recall_and_maps_to_guard_core(tmp_path, field_subj)
