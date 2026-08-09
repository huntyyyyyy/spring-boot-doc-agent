"""Artifact inventory and drift-check helpers for local-runner phases."""

from __future__ import annotations

import os
import sys


def py_mod(module: str, *args: str) -> list[str]:
    return [sys.executable, "-m", module, *args]


def artifact_inventory(log, out_dir):
    log.rule("ARTIFACT INVENTORY")
    for root, dirs, files in os.walk(out_dir):
        dirs.sort()
        for name in sorted(files):
            abspath = os.path.join(root, name)
            rel = os.path.relpath(abspath, out_dir).replace(os.sep, "/")
            log(f"  {os.path.getsize(abspath):>9,} B  {rel}")


def run_drift_check(log, runner, repo_path, manifest, out_dir, args, signals_path):
    if args.skip_drift:
        return
    log.rule("DRIFT CHECK (real) — pre-flight for a future re-run")
    baseline = os.path.abspath(args.prior_signals) if args.prior_signals else signals_path
    if not args.prior_signals:
        log("  note: drift is measured against this run's own scan, so 'no drift' is")
        log("        the expected result — it exercises the script, it doesn't tell")
        log("        you anything about the repo. Use --prior-signals for a real check.")
    runner.run(
        "spring_drift_check",
        py_mod(
            "doc_engine.tools.spring_drift_check",
            repo_path,
            baseline,
            "--manifest",
            manifest,
            "--out",
            os.path.join(out_dir, "drift_report.json"),
        ),
    )
