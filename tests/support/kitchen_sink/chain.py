"""Kitchen-sink command-chain runner (manifest → scan → mock stages → gates)."""

from __future__ import annotations

import datetime
import json
import os
import subprocess

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

def _run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)



def _git(repo, *args):
    return _run(["git"] + list(args), cwd=repo)



def run_chain(repo, out_dir):
    """The documented command series, as real subprocesses.

    Step-by-step rather than delegating to run_pipeline_local.py, so each
    step's own exit code is observable. The four LLM stages are filled in by
    calling that script's mock builders in-process — they are the only part of
    the chain a plain Python process cannot run for real.
    """
    steps = {}
    manifest = os.path.join(out_dir, "run_manifest.json")
    signals = os.path.join(out_dir, "spring_signals.json")
    groups = os.path.join(out_dir, "groups.json")
    edges = os.path.join(out_dir, "cross_group_edges.json")
    preflight = os.path.join(out_dir, "capacity_preflight_report.json")
    docs = os.path.join(repo, "docs")
    snapshots = []

    def record(name, proc):
        steps[name] = proc
        if os.path.isfile(manifest):
            with open(manifest, encoding="utf-8") as f:
                snapshots.append((name, json.load(f)))

    def manifest_cmd(*args):
        return [PY, "-m", "doc_engine.tools.run_manifest", *args]

    record("init", _run(manifest_cmd("init", repo, "--out", manifest)))
    record("start_signal_scan", _run(manifest_cmd("start-stage", manifest, "signal_scan")))
    record("signal_scan", _run([
        PY, "-m", "doc_engine.tools.spring_signal_scan", repo, "--out", signals,
        "--scanners", "filesystem,ast-grep",
    ]))
    record("end_signal_scan",
           _run(manifest_cmd("end-stage", manifest, "signal_scan", "--status", "complete")))
    record("start_partition", _run(manifest_cmd("start-stage", manifest, "partition")))
    record("partition", _run([PY, "-m", "doc_engine.tools.partition_repo", repo,
                              "--max-tokens", MAX_TOKENS, "--out", groups]))
    record("end_partition",
           _run(manifest_cmd("end-stage", manifest, "partition", "--status", "complete")))
    record("cross_group_edges", _run([PY, "-m", "doc_engine.tools.build_cross_group_edges",
                                      groups, signals, "--out", edges]))
    record("capacity_preflight", _run([PY, "-m", "doc_engine.tools.capacity_preflight", repo,
                                       "--groups-file", groups, "--signals-file", signals,
                                       "--max-tokens", MAX_TOKENS, "--out", preflight]))

    signals_data = json.load(open(signals, encoding="utf-8"))
    groups_data = json.load(open(groups, encoding="utf-8"))
    edges_data = json.load(open(edges, encoding="utf-8"))

    quiet = lambda *a, **k: None  # noqa: E731
    today = datetime.date.today().isoformat()
    pool = load_citations(signals_data, repo)
    todos = sweep_todos(repo)
    n = groups_data["num_groups"]

    record("start_file_summarize",
           _run(manifest_cmd("start-stage", manifest, "file_summarize", "--fanout", str(n))))
    mock_file_summaries(out_dir, groups_data, pool, edges_data, quiet)
    record("end_file_summarize",
           _run(manifest_cmd("end-stage", manifest, "file_summarize", "--status", "complete")))

    record("start_architect",
           _run(manifest_cmd("start-stage", manifest, "architect", "--fanout", str(n + 1))))
    mock_architecture(out_dir, groups_data, pool, quiet)
    record("end_architect",
           _run(manifest_cmd("end-stage", manifest, "architect", "--status", "complete")))

    record("start_gap", _run(manifest_cmd("start-stage", manifest,
                                          "gap_analysis_interview", "--fanout", "1")))
    mock_gap_and_interview(out_dir, pool, todos, today, quiet)
    record("end_gap", _run(manifest_cmd("end-stage", manifest,
                                        "gap_analysis_interview", "--status", "complete")))

    answers = json.load(open(os.path.join(out_dir, "interview_answers.json"), encoding="utf-8"))
    record("start_doc_writer",
           _run(manifest_cmd("start-stage", manifest, "doc_writer", "--fanout", "14")))
    mock_docs(docs, pool, todos, answers, today,
              find_existing_readme(repo), quiet)
    record("end_doc_writer",
           _run(manifest_cmd("end-stage", manifest, "doc_writer", "--status", "complete")))

    record("gate", _run([PY, "-m", "doc_engine.tools.check_pipeline_output", docs, "--target-repo", repo]))
    record("citation_coverage", _run([PY, "-m", "doc_engine.tools.citation_coverage", docs,
                                      "--target-repo", repo]))
    record("secrets", _run([PY, "-m", "doc_engine.tools.check_no_secrets_leaked",
                            os.path.join(out_dir, "summaries.json"), docs]))
    record("finalize", _run(manifest_cmd(
        "finalize", manifest, "--signals-file", signals, "--docs-dir", docs,
        "--interview-file", os.path.join(out_dir, "interview_answers.json"),
        "--preflight-file", preflight)))
    # Deliberately after finalize: --manifest reads file_signatures, which is
    # written by finalize. Earlier would compare against nothing.
    record("drift", _run([PY, "-m", "doc_engine.tools.spring_drift_check", repo, signals,
                          "--manifest", manifest,
                          "--out", os.path.join(out_dir, "drift_report.json")]))
    return steps, snapshots


