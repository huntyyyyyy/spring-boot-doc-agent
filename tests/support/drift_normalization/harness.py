"""Cohesive suite from tests/ratchets/test_drift_normalization.py: _report_basename, Outcome, _fixtures_usable, _citation_count, _run_scenario, _apply_to_java, _semantic_edits, _locate_getmapping_line."""
from __future__ import annotations
import os
import shutil
import sys
import tempfile
import unittest
from typing import Callable, Dict, List, NamedTuple, Optional
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.scanning import java_extract
from doc_engine.scanning import _scanner_astgrep as astgrep_backend
from doc_engine.tools import spring_drift_check, spring_signal_scan
import drift_match_normalizers as norms
import java_perturbations as perturb
SCRIPT_DIR = SCRIPTS_DIR
FIXTURES = os.path.join(SCRIPT_DIR, 'fixtures', 'spring_signals')
_BILLING = os.path.join('src', 'main', 'java', 'com', 'example', 'billing')
CONTROLLER_REL = os.path.join(_BILLING, 'InvoiceController.java')
LEDGER_REL = os.path.join(_BILLING, 'PaymentLedger.java')
CONFIRMING = ('confirmed_still_present', 'unchanged')
CONTROLLER_BASENAME = 'InvoiceController.java'
LEDGER_BASENAME = 'PaymentLedger.java'
SEMANTIC_TOUCHED = frozenset({CONTROLLER_BASENAME, LEDGER_BASENAME})
_TMP: Optional[str] = None
OUTCOMES: Dict[str, 'Outcome'] = {}
GETMAPPING_LINE: Optional[int] = None

def _setUpModule_prelude():
    global _TMP, GETMAPPING_LINE
    if not os.path.isdir(FIXTURES):
        raise AssertionError(f'committed spring_signals fixtures missing at {FIXTURES}')
    if not os.path.isfile(os.path.join(FIXTURES, CONTROLLER_REL)):
        raise AssertionError(f'fixture layout drift: expected nested {CONTROLLER_REL} under {FIXTURES}')
    if shutil.which('ast-grep') is None:
        raise unittest.SkipTest('ast-grep not on PATH')
    _TMP = tempfile.mkdtemp(prefix='drift_norm_')
    GETMAPPING_LINE = _locate_getmapping_line()
    original_extract = java_extract.first_line_match
    original_backend = astgrep_backend.first_line_match

def _setUpModule_core():
    try:
        for cand_name, fn in norms.CANDIDATES.items():
            java_extract.first_line_match = fn
            astgrep_backend.first_line_match = fn
            for p_name, transform in perturb.FORMATTING_ONLY.items():
                OUTCOMES[f'{cand_name}/{p_name}'] = _run_scenario(f'{cand_name}_{p_name}', _apply_to_java(transform))
            OUTCOMES[f'{cand_name}/semantic'] = _run_scenario(f'{cand_name}_semantic', _semantic_edits)
        java_extract.first_line_match = original_extract
        astgrep_backend.first_line_match = original_backend
        for p_name, transform in perturb.DELIBERATELY_BROKEN.items():
            OUTCOMES[f'broken/{p_name}'] = _run_scenario(f'broken_{p_name}', _apply_to_java(transform))
    finally:
        java_extract.first_line_match = original_extract
        astgrep_backend.first_line_match = original_backend

def _report_basename(path: str) -> str:
    """Drift reports use repo-relative paths; older pins used flat basenames."""
    return os.path.basename(path.replace('\\', '/'))

class Outcome(NamedTuple):
    """One perturbation, scanned before and after, then drift-checked.

    `valid` is the instrument check: a formatting-only edit must leave the same
    number of citations discoverable by a fresh scan. False means the edit
    changed what is detectable, so its drift report says nothing about the
    checker and must not be scored."""
    report: dict
    citations_before: int
    citations_after: int

    @property
    def valid(self) -> bool:
        return self.citations_before == self.citations_after

    def drifted(self) -> List[dict]:
        return [r for r in self.report['results'] if r['status'] == 'drifted']

def _fixtures_usable() -> bool:
    """True when the committed fixture tree exists and ast-grep is on PATH.

    Do not call a removed ``spring_signal_scan.find_ast_grep`` helper — that
    AttributeError was swallowed here and silently skipped the whole suite
    in CI (19 dark tests) while ast-grep was verified elsewhere in the job.
    """
    if not os.path.isdir(FIXTURES):
        return False
    if not os.path.isfile(os.path.join(FIXTURES, CONTROLLER_REL)):
        return False
    return shutil.which('ast-grep') is not None

def _citation_count(signals: dict) -> int:
    return sum((len(v) for v in signals['evidence'].values()))

def _run_scenario(name: str, mutate: Callable[[str], None]) -> Outcome:
    """Copy the fixtures, scan, mutate, re-scan, drift-check."""
    root = os.path.join(_TMP, name)
    shutil.copytree(FIXTURES, root)
    before = spring_signal_scan.scan(root)
    mutate(root)
    after = spring_signal_scan.scan(root)
    report = spring_drift_check.check_drift(root, before)
    return Outcome(report, _citation_count(before), _citation_count(after))

def _apply_to_java(transform: Callable[[str], str]) -> Callable[[str], None]:

    def go(root: str) -> None:
        for dirpath, _dirs, files in os.walk(root):
            for fname in sorted(files):
                if not fname.endswith('.java'):
                    continue
                path = os.path.join(dirpath, fname)
                with open(path, encoding='utf-8') as f:
                    src = f.read()
                new = transform(src)
                if new != src:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new)
    return go

def _semantic_edits(root: str) -> None:
    """Three content changes that keep the citation COUNT identical, so the
    same validity gate as arm 1 applies unchanged.

    Asserted rather than best-effort: if a fixture is edited so one of these
    no longer applies, this suite must fail loudly instead of quietly measuring
    a corpus where nothing changed."""
    ctrl = os.path.join(root, CONTROLLER_REL)
    with open(ctrl, encoding='utf-8') as f:
        src = f.read()
    assert '"/{id}"' in src, 'fixture no longer has the /{id} mapping to change'
    assert '@GetMapping' in src, 'fixture no longer has @GetMapping to change'
    with open(ctrl, 'w', encoding='utf-8') as f:
        f.write(src.replace('"/{id}"', '"/{invoiceId}"').replace('@GetMapping', '@PutMapping'))
    led = os.path.join(root, LEDGER_REL)
    with open(led, encoding='utf-8') as f:
        src = f.read()
    assert 'name = "payment_ledger"' in src, 'fixture no longer has the table name to rename'
    with open(led, 'w', encoding='utf-8') as f:
        f.write(src.replace('name = "payment_ledger"', 'name = "ledger_v2"'))

def _locate_getmapping_line() -> int:
    """The line of the @GetMapping this suite mutates, read from the fixture
    rather than hardcoded, so inserting a line above it does not silently make
    the expected-drift label point at the wrong citation."""
    with open(os.path.join(FIXTURES, CONTROLLER_REL), encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            if '@GetMapping' in line:
                return i
    raise AssertionError('no @GetMapping in InvoiceController.java')

def setUpModule() -> None:
    """Every scenario costs two full scans and a drift check, each of which
    shells out to ast-grep. Run them once here and let the test methods assert
    over the results, rather than re-deriving per method."""
    _setUpModule_prelude()
    _setUpModule_core()

def tearDownModule() -> None:
    if _TMP and os.path.isdir(_TMP):
        shutil.rmtree(_TMP, ignore_errors=True)
