"""Kitchen-sink chain gate/finalize/drift phases."""

from __future__ import annotations

import os

from tests.support.kitchen_sink.chain_phases import _manifest_cmd, _record_step, _run


def run_gate_and_finalize_phases(
    repo, out_dir, steps, snapshots, manifest, signals, preflight, docs
):
    def record(name, proc):
        _record_step(steps, snapshots, manifest, name, proc)

    record(
        "gate",
        _run([PY, "-m", "doc_engine.tools.check_pipeline_output", docs, "--target-repo", repo]),
    )
    record(
        "citation_coverage",
        _run([PY, "-m", "doc_engine.tools.citation_coverage", docs, "--target-repo", repo]),
    )
    record(
        "secrets",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.check_no_secrets_leaked",
                os.path.join(out_dir, "summaries.json"),
                docs,
            ]
        ),
    )
    record(
        "finalize",
        _run(
            _manifest_cmd(
                "finalize",
                manifest,
                "--signals-file",
                signals,
                "--docs-dir",
                docs,
                "--interview-file",
                os.path.join(out_dir, "interview_answers.json"),
                "--preflight-file",
                preflight,
            )
        ),
    )
    record(
        "drift",
        _run(
            [
                PY,
                "-m",
                "doc_engine.tools.spring_drift_check",
                repo,
                signals,
                "--manifest",
                manifest,
                "--out",
                os.path.join(out_dir, "drift_report.json"),
            ]
        ),
    )
