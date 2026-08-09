"""Coverage climb batch B3: suite_timing edges + workflow_size predicates.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.suite_timing.* and
workflow_size — asserts bite slowest(limit<=0), bad junit time, cascade+missing
junit, continue-on-error/yaml-absent / non-dict job shapes (not padding).
"""
from __future__ import annotations
from pathlib import Path
from unittest import mock
import pytest
from doc_engine.ci.suite_timing.duration_records import CaseDuration, SuiteTimingReport
from doc_engine.ci.suite_timing.github_timing_summary import append_github_summary, format_timing_markdown, render_from_junit
from doc_engine.ci.suite_timing.junit_duration_parse import parse_junit_durations
from doc_engine.ci import workflow_size as ws
pytestmark = pytest.mark.domain_climb_sensor

def _test_timing_summary_cascade_and_append_newline_prelude(tmp_path: Path):
    missing_cov = tmp_path / 'missing_coverage.xml'
    missing_junit = tmp_path / 'absent.junit.xml'
    text = render_from_junit(missing_junit, coverage_xml=missing_cov, top_n=2)
    assert 'Pre-pytest cascade' in text
    assert 'junit xml missing' in text
    present = tmp_path / 'coverage.xml'
    present.write_text('<coverage line-rate="1"/>', encoding='utf-8')
    empty = format_timing_markdown(SuiteTimingReport.from_records([]), top_n=3, coverage_xml=present)
    assert 'No junit testcase durations found' in empty
    assert 'Pre-pytest cascade' not in empty
    no_cascade = render_from_junit(missing_junit, coverage_xml=present, top_n=1)
    assert 'junit xml missing' in no_cascade
    assert 'Pre-pytest cascade' not in no_cascade
    with_records = format_timing_markdown(SuiteTimingReport.from_records([CaseDuration('t::x', 1.0)]), top_n=1, coverage_xml=missing_cov)
    assert 'Pre-pytest cascade' in with_records
    assert '1.000s' in with_records

def _test_timing_summary_cascade_and_append_newline_core(tmp_path: Path):
    summary = tmp_path / 'summary.md'
    summary.write_text('### prior', encoding='utf-8')
    append_github_summary('### Suite timing\n', summary)
    body = summary.read_text(encoding='utf-8')
    assert body.startswith('### prior\n')
    assert 'Suite timing' in body
    fresh = tmp_path / 'fresh_summary.md'
    append_github_summary('### only\n', fresh)
    assert fresh.read_text(encoding='utf-8') == '### only\n'

def _test_workflow_size_yaml_absent_and_job_shapes_prelude(tmp_path: Path):
    small = tmp_path / 'small'
    small.mkdir()
    (small / 'tiny.yml').write_text('name: t\n', encoding='utf-8')
    hard, advisory = ws.check_workflow_loc(small, label_fn=lambda p: p.name)
    assert hard == [] and advisory == []
    heredoc_dir = tmp_path / 'heredoc'
    heredoc_dir.mkdir()
    (heredoc_dir / 'h2.yml').write_text('run: python <<PY\nprint(1)\nPY\n', encoding='utf-8')
    heredoc = ws.check_no_python_heredocs(heredoc_dir, label_fn=lambda p: p.name)
    assert any(('h2.yml' in e for e in heredoc))
    assert ws._jobs_mapping(None) == {}
    assert ws._jobs_mapping({'jobs': 'nope'}) == {}
    assert ws._jobs_mapping({'jobs': {'a': 1}}) == {'a': 1}
    with mock.patch.object(ws, 'yaml', None):
        errors = ws.check_no_continue_on_error_on_reusable_call(small, label_fn=lambda p: p.name)
    assert errors and 'PyYAML' in errors[0]

def _test_workflow_size_yaml_absent_and_job_shapes_core(tmp_path: Path):
    jobs_dir = tmp_path / 'jobs'
    jobs_dir.mkdir()
    (jobs_dir / 'jobs.yml').write_text('name: J\non: [push]\njobs:\n  plain: 1\n  local:\n    runs-on: ubuntu-latest\n    steps: []\n  reused:\n    uses: ./.github/workflows/y.yml\n  soft:\n    continue-on-error: true\n    uses: ./.github/workflows/x.yml\n', encoding='utf-8')
    bad = ws.check_no_continue_on_error_on_reusable_call(jobs_dir, label_fn=lambda p: p.name)
    assert any(('soft' in e for e in bad))
    assert not any(('reused' in e for e in bad))
    clean = tmp_path / 'clean'
    clean.mkdir()
    (clean / 'ok.yml').write_text('name: ok\non: [push]\n', encoding='utf-8')
    assert ws.check_no_python_heredocs(clean, label_fn=lambda p: p.name) == []

def test_duration_slowest_zero_and_junit_edges(tmp_path: Path) -> None:
    report = SuiteTimingReport.from_records([CaseDuration('a::b', 1.5), CaseDuration('c::d', 0.5)])
    assert report.slowest(0) == ()
    assert report.slowest(-1) == ()
    assert len(report.slowest(1)) == 1
    junit = tmp_path / 'j.xml'
    junit.write_text('<?xml version="1.0"?><testsuite><testcase name="solo" time="not-a-float"/><testcase classname="only.class" time="1"/><testcase time="0.25"/></testsuite>\n', encoding='utf-8')
    parsed = parse_junit_durations(junit)
    node_ids = {row.node_id for row in parsed.records}
    assert 'solo' in node_ids
    assert 'only.class' in node_ids
    assert '(unknown)' in node_ids
    assert all((row.duration_seconds >= 0.0 for row in parsed.records))

def test_timing_summary_cascade_and_append_newline(tmp_path: Path) -> None:
    _test_timing_summary_cascade_and_append_newline_prelude(tmp_path)
    _test_timing_summary_cascade_and_append_newline_core(tmp_path)

def test_workflow_size_yaml_absent_and_job_shapes(tmp_path: Path) -> None:
    _test_workflow_size_yaml_absent_and_job_shapes_prelude(tmp_path)
    _test_workflow_size_yaml_absent_and_job_shapes_core(tmp_path)
