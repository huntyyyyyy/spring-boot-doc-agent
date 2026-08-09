"""CLI adapter for run_manifest (argv → lifecycle mutations → atomic writes).

Looks up lifecycle helpers via the ``run_manifest`` façade so characterization
tests can monkeypatch the public module surface (e.g. ``load_file_signatures``).
"""

from __future__ import annotations

import argparse
import sys

from doc_engine.core.jsonio import load_json as _read_json
from doc_engine.tools.run_manifest_constants import END_STAGE_STATUSES


def _cmd_init(args):
    from doc_engine.tools import run_manifest as rm

    if not rm.os.path.isdir(args.repo_path):
        print(f"error: not a directory: {args.repo_path}", file=sys.stderr)
        sys.exit(1)
    manifest = rm.build_init_manifest(args.repo_path, now_ms=args.now_ms)
    rm._write_json_atomic(args.out, manifest)
    tr = manifest["target_repo"]
    print(
        f"Wrote {args.out}. run_id={manifest['run_id']} target_repo={tr['path']} "
        f"commit_hash={tr['commit_hash']} dirty={tr['dirty']}"
    )


def _cmd_start_stage(args):
    from doc_engine.tools import run_manifest as rm

    manifest = _read_json(args.manifest_path)
    rm.start_stage(
        manifest, args.stage_name, fanout=args.fanout, now_ms=args.now_ms
    )
    rm._write_json_atomic(args.manifest_path, manifest)
    print(f"stage '{args.stage_name}' started")


def _cmd_end_stage(args):
    from doc_engine.tools import run_manifest as rm

    manifest = _read_json(args.manifest_path)
    try:
        rm.end_stage(
            manifest,
            args.stage_name,
            args.status,
            error=args.error,
            now_ms=args.now_ms,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    rm._write_json_atomic(args.manifest_path, manifest)
    print(f"stage '{args.stage_name}' ended: {args.status}")


def _finalize_side_inputs(args, manifest):
    from doc_engine.tools import run_manifest as rm

    if args.signals_file:
        file_signatures = rm.load_file_signatures(signals_file=args.signals_file)
    else:
        file_signatures = rm.load_file_signatures(
            repo_path=manifest.get("target_repo", {}).get("path"),
        )
    evidence_tag_counts = (
        rm.compute_evidence_tag_counts(args.docs_dir) if args.docs_dir else None
    )
    interview = (
        rm.parse_interview_file(args.interview_file) if args.interview_file else None
    )
    capacity_preflight = (
        rm.compute_capacity_preflight_tie_in(args.preflight_file)
        if args.preflight_file
        else None
    )
    return file_signatures, evidence_tag_counts, interview, capacity_preflight


def _cmd_finalize(args):
    from doc_engine.tools import run_manifest as rm

    manifest = _read_json(args.manifest_path)
    file_signatures, evidence_tag_counts, interview, capacity_preflight = (
        _finalize_side_inputs(args, manifest)
    )
    manifest, warnings = rm.finalize_manifest(
        manifest,
        status=args.status,
        file_signatures=file_signatures,
        evidence_tag_counts=evidence_tag_counts,
        interview=interview,
        capacity_preflight=capacity_preflight,
        now_ms=args.now_ms,
    )
    rm._write_json_atomic(args.manifest_path, manifest)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    print(rm.format_summary(manifest))


def _cmd_summary(args):
    from doc_engine.tools import run_manifest as rm

    manifest = _read_json(args.manifest_path)
    print(rm.format_summary(manifest))


def _build_arg_parser():
    from doc_engine.tools import run_manifest as rm

    ap = argparse.ArgumentParser(
        description=rm.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new run_manifest.json for a pipeline run")
    p_init.add_argument("repo_path")
    p_init.add_argument("--out", default="run_manifest.json")
    p_init.add_argument("--now-ms", type=int, default=None, help=argparse.SUPPRESS)

    p_start = sub.add_parser("start-stage", help="Record a stage's start")
    p_start.add_argument("manifest_path")
    p_start.add_argument("stage_name")
    p_start.add_argument(
        "--fanout",
        type=int,
        default=None,
        help="Actual subagent dispatch count for this stage, if applicable",
    )
    p_start.add_argument("--now-ms", type=int, default=None, help=argparse.SUPPRESS)

    p_end = sub.add_parser("end-stage", help="Record a stage's end")
    p_end.add_argument("manifest_path")
    p_end.add_argument("stage_name")
    p_end.add_argument("--status", required=True, choices=END_STAGE_STATUSES)
    p_end.add_argument("--error", default=None)
    p_end.add_argument("--now-ms", type=int, default=None, help=argparse.SUPPRESS)

    p_fin = sub.add_parser(
        "finalize", help="Close out a run_manifest.json at the end of a pipeline run"
    )
    p_fin.add_argument("manifest_path")
    p_fin.add_argument(
        "--status",
        choices=["complete", "failed", "partial"],
        default=None,
        help="Override the inferred overall status (default: inferred from stage outcomes)",
    )
    p_fin.add_argument(
        "--signals-file",
        default=None,
        help="Reuse an existing spring_signals.json's file_signatures instead of re-hashing",
    )
    p_fin.add_argument(
        "--docs-dir",
        default=None,
        help="Directory containing the fourteen generated doc-writer output files",
    )
    p_fin.add_argument(
        "--interview-file", default=None, help="Path to interview_answers.json"
    )
    p_fin.add_argument(
        "--preflight-file",
        default=None,
        help="Path to a capacity_preflight_report.json",
    )
    p_fin.add_argument("--now-ms", type=int, default=None, help=argparse.SUPPRESS)

    p_sum = sub.add_parser(
        "summary", help="Print a human-readable summary of an existing manifest"
    )
    p_sum.add_argument("manifest_path")
    return ap


_COMMAND_HANDLERS = {
    "init": _cmd_init,
    "start-stage": _cmd_start_stage,
    "end-stage": _cmd_end_stage,
    "finalize": _cmd_finalize,
    "summary": _cmd_summary,
}


def main():
    args = _build_arg_parser().parse_args()
    _COMMAND_HANDLERS[args.command](args)
