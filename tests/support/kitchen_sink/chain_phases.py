"""Kitchen-sink chain phases: manifest bootstrap, mock generative, gates."""

from __future__ import annotations

import datetime
import json
import os

from doc_engine.pipeline.mock_stages import (
    find_existing_readme,
    load_citations,
    mock_architecture,
    mock_docs,
    mock_file_summaries,
    mock_gap_and_interview,
    sweep_todos,
)
from tests.support.kitchen_sink.constants import MAX_TOKENS, PY
from tests.support.kitchen_sink.tool_invoke import run_argv


def _run(argv, **kw):
    return run_argv(argv, **kw)


def _manifest_cmd(*args):
    return [PY, "-m", "doc_engine.tools.run_manifest", *args]


def _record_step(steps, snapshots, manifest, name, proc):
    steps[name] = proc
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as handle:
            snapshots.append((name, json.load(handle)))


def run_manifest_and_scan_phases(repo, out_dir, steps, snapshots):
    manifest = os.path.join(out_dir, "run_manifest.json")
    signals = os.path.join(out_dir, "spring_signals.json")
    groups = os.path.join(out_dir, "groups.json")
    edges = os.path.join(out_dir, "cross_group_edges.json")
    preflight = os.path.join(out_dir, "capacity_preflight_report.json")

    def record(name, proc):
        _record_step(steps, snapshots, manifest, name, proc)

    record("init", _run(_manifest_cmd("init", repo, "--out", manifest)))
    record("start_signal_scan", _run(_manifest_cmd("start-stage", manifest, "signal_scan")))
    record(
        "signal_scan",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.spring_signal_scan",
                repo,
                "--out",
                signals,
                "--scanners",
                "filesystem,ast-grep",
            ]
        ),
    )
    record(
        "end_signal_scan",
        _run(_manifest_cmd("end-stage", manifest, "signal_scan", "--status", "complete")),
    )
    record("start_partition", _run(_manifest_cmd("start-stage", manifest, "partition")))
    record(
        "partition",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.partition_repo",
                repo,
                "--max-tokens",
                MAX_TOKENS,
                "--out",
                groups,
            ]
        ),
    )
    record(
        "end_partition",
        _run(_manifest_cmd("end-stage", manifest, "partition", "--status", "complete")),
    )
    record(
        "cross_group_edges",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.build_cross_group_edges",
                groups,
                signals,
                "--out",
                edges,
            ]
        ),
    )
    record(
        "capacity_preflight",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.capacity_preflight",
                repo,
                "--groups-file",
                groups,
                "--signals-file",
                signals,
                "--max-tokens",
                MAX_TOKENS,
                "--out",
                preflight,
            ]
        ),
    )
    return manifest, signals, groups, edges, preflight


def _noop(*a, **k):
    return None


def run_summarize_and_architect_phases(
    out_dir, steps, snapshots, manifest, signals, groups, edges, pool, quiet, fanout
):
    def record(name, proc):
        _record_step(steps, snapshots, manifest, name, proc)

    groups_data = json.load(open(groups, encoding="utf-8"))
    edges_data = json.load(open(edges, encoding="utf-8"))
    record(
        "start_file_summarize",
        _run(_manifest_cmd("start-stage", manifest, "file_summarize", "--fanout", str(fanout))),
    )
    mock_file_summaries(out_dir, groups_data, pool, edges_data, quiet)
    record(
        "end_file_summarize",
        _run(_manifest_cmd("end-stage", manifest, "file_summarize", "--status", "complete")),
    )
    record(
        "start_architect",
        _run(_manifest_cmd("start-stage", manifest, "architect", "--fanout", str(fanout + 1))),
    )
    mock_architecture(out_dir, groups_data, pool, quiet)
    record(
        "end_architect",
        _run(_manifest_cmd("end-stage", manifest, "architect", "--status", "complete")),
    )


def run_gap_and_docs_phases(
    repo, out_dir, steps, snapshots, manifest, pool, todos, today, quiet
):
    docs = os.path.join(repo, "docs")

    def record(name, proc):
        _record_step(steps, snapshots, manifest, name, proc)

    record(
        "start_gap",
        _run(_manifest_cmd("start-stage", manifest, "gap_analysis_interview", "--fanout", "1")),
    )
    mock_gap_and_interview(out_dir, pool, todos, today, quiet)
    record(
        "end_gap",
        _run(_manifest_cmd("end-stage", manifest, "gap_analysis_interview", "--status", "complete")),
    )
    answers = json.load(open(os.path.join(out_dir, "interview_answers.json"), encoding="utf-8"))
    record(
        "start_doc_writer",
        _run(_manifest_cmd("start-stage", manifest, "doc_writer", "--fanout", "14")),
    )
    mock_docs(docs, pool, todos, answers, today, find_existing_readme(repo), quiet)
    record(
        "end_doc_writer",
        _run(_manifest_cmd("end-stage", manifest, "doc_writer", "--status", "complete")),
    )
    return docs


def run_mock_generative_phases(
    repo, out_dir, steps, snapshots, manifest, signals, groups, edges
):
    signals_data = json.load(open(signals, encoding="utf-8"))
    groups_data = json.load(open(groups, encoding="utf-8"))
    quiet = _noop
    today = datetime.date.today().isoformat()
    pool = load_citations(signals_data, repo)
    todos = sweep_todos(repo)
    fanout = groups_data["num_groups"]
    run_summarize_and_architect_phases(
        out_dir, steps, snapshots, manifest, signals, groups, edges, pool, quiet, fanout
    )
    return run_gap_and_docs_phases(
        repo, out_dir, steps, snapshots, manifest, pool, todos, today, quiet
    )


