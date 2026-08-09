"""Gate steps for the local-runner full-finish phase."""

from __future__ import annotations

import os
from pathlib import Path

from doc_engine.paths import repo_root
from doc_engine.pipeline import gates
from doc_engine.pipeline.local_runner_phases.support import _py_mod

REPO_ROOT = str(repo_root())


def run_validate_artifact_gates(runner, out_dir: str, repo_path: str) -> None:
    gates.run_gate_via_runner(
        runner,
        "validate_artifacts.py --all (B contract gate)",
        lambda: (gates.run_validate_all_artifacts(out_dir), "OK"),
        gate=True,
        gate_id="validate_artifacts_all",
    )
    gates.run_gate_via_runner(
        runner,
        "pipeline_validators.py (summaries + gap_questions gate)",
        lambda: gates.run_pipeline_validators(out_dir, repo_path),
        gate=True,
        gate_id="pipeline_validators",
    )


def run_check_pipeline_output_gate(log, runner, args, docs_dir: str, repo_path: str) -> None:
    gate_argv = _py_mod(
        "doc_engine.tools.check_pipeline_output",
        docs_dir,
        "--target-repo",
        repo_path,
    )
    if not args.docs_in_target_repo:
        gate_argv.append("--no-write-check")
        log("")
        log("  note: --no-write-check is passed because the docs were written outside")
        log("        the target repo. Re-run with --docs-in-target-repo to exercise")
        log("        the stray-write check for real.")
    runner.run(
        "check_pipeline_output (Stage 4 GATE)",
        gate_argv,
        gate=True,
        gate_id="check_pipeline_output",
    )


def run_citation_and_secrets_gates(
    runner, docs_dir: str, repo_path: str, out_dir: str, *, strict: bool
) -> None:
    cc_argv = _py_mod(
        "doc_engine.tools.citation_coverage",
        docs_dir,
        "--target-repo",
        repo_path,
    )
    if strict:
        cc_argv.append("--strict")
    runner.run(
        "citation_coverage",
        cc_argv,
        gate=strict,
        gate_id="citation_coverage",
    )
    runner.run(
        "check_no_secrets_leaked",
        _py_mod(
            "doc_engine.tools.check_no_secrets_leaked",
            os.path.join(out_dir, "summaries.json"),
            docs_dir,
        ),
        gate=True,
        gate_id="check_no_secrets_leaked",
    )


def run_pipeline_stages_real_suite(
    log, runner, py: str, out_dir: str, repo_path: str, docs_dir: str
) -> None:
    env = dict(os.environ)
    env["PIPELINE_ARTIFACTS_DIR"] = out_dir
    env["PIPELINE_ARTIFACTS_TARGET_REPO"] = repo_path
    if docs_dir != os.path.join(out_dir, "docs"):
        log("")
        log("  note: test_pipeline_stages.py's real-artifacts pass looks for docs/ inside")
        log("        PIPELINE_ARTIFACTS_DIR. With --docs-in-target-repo the docs are")
        log("        elsewhere, so its docs subtest will skip; summaries and gap")
        log("        questions are still validated.")
    # Prefer façade REPO_ROOT so climb tests can monkeypatch full_finish.REPO_ROOT.
    from doc_engine.pipeline.local_runner_phases import full_finish as _ff

    split_suite = sorted(
        (Path(_ff.REPO_ROOT) / "tests" / "doc_engine").glob(
            "test_pipeline_stages_*.py"
        )
    )
    if not split_suite:
        raise RuntimeError(
            "no tests/doc_engine/test_pipeline_stages_*.py suites found "
            "(stub test_pipeline_stages.py collects zero tests)"
        )
    runner.run(
        "pytest tests/doc_engine/test_pipeline_stages_*.py -v "
        "(real suite vs. mock artifacts)",
        [py, "-m", "pytest", *[str(p) for p in split_suite], "-v"],
        gate=True,
        gate_id="test_pipeline_stages",
        env=env,
    )


def run_finalize_manifest(runner, state, docs_dir: str, out_dir: str) -> None:
    runner.run(
        "run_manifest finalize",
        _py_mod(
            "doc_engine.tools.run_manifest",
            "finalize",
            state.manifest,
            "--signals-file",
            state.signals_path,
            "--docs-dir",
            docs_dir,
            "--interview-file",
            os.path.join(out_dir, "interview_answers.json"),
            "--preflight-file",
            state.preflight_path,
        ),
    )
    runner.run(
        "run_manifest summary",
        _py_mod("doc_engine.tools.run_manifest", "summary", state.manifest),
    )
