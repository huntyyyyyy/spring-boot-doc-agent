"""Kitchen-sink command-chain runner (manifest → scan → mock stages → gates).

Signal scan argv is pinned to ``filesystem,ast-grep`` (no CodeQL) so chapter
tests stay hermetic and do not pretend to exercise the CodeQL cache/DB path.
"""

from __future__ import annotations

from tests.support.kitchen_sink.chain_gate_phases import run_gate_and_finalize_phases
from tests.support.kitchen_sink.chain_phases import (
    _run,
    run_manifest_and_scan_phases,
    run_mock_generative_phases,
)
from tests.support.kitchen_sink.tool_invoke import run_argv


def _git(repo, *args):
    return _run(["git"] + list(args), cwd=repo)


def run_chain(repo, out_dir):
    """The documented command series, with per-step exit codes observable."""
    steps = {}
    snapshots = []
    manifest, signals, groups, edges, preflight = run_manifest_and_scan_phases(
        repo, out_dir, steps, snapshots
    )
    docs = run_mock_generative_phases(
        repo, out_dir, steps, snapshots, manifest, signals, groups, edges
    )
    run_gate_and_finalize_phases(
        repo, out_dir, steps, snapshots, manifest, signals, preflight, docs
    )
    return steps, snapshots
