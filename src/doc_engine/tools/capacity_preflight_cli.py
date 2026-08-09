"""CLI adapter for capacity preflight (argv → compute/calibrate → report).

Looks up compute helpers and path validators via the ``capacity_preflight``
façade so characterization tests can monkeypatch the public module surface.
"""

from __future__ import annotations

import argparse
import json
import sys


def _build_arg_parser():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("repo_path", help="Path to the target repository root")
    ap.add_argument("--max-tokens", type=int, default=120000,
                     help="Same meaning as partition_repo.py's --max-tokens (default: 120000)")
    ap.add_argument("--overlap", type=float, default=0.10,
                     help="Same meaning as partition_repo.py's --overlap (default: 0.10)")
    ap.add_argument("--groups-file", default=None,
                     help=("Existing groups.json (Stage 0 path: partition input; "
                           "L2b: optional proxy compare from group est_tokens — "
                           "ignored for the ratio if --stage0-preflight-report is also set)"))
    ap.add_argument("--signals-file", default=None,
                     help="Existing spring_signals.json to join against instead of re-scanning")
    ap.add_argument("--edges-file", default=None,
                     help="Existing cross_group_edges.json to read instead of re-running the join (Stage 0 already writes this)")
    ap.add_argument("--summaries-file", default=None,
                     help=("L2b: existing summaries.json — when set, run post-artifact "
                           "Stage-4 measurement (measured_stage4_inputs) instead of "
                           "Stage-0 partial_proxy_pre_stage4"))
    ap.add_argument("--interview-answers-file", default=None,
                     help="L2b: existing interview_answers.json (optional; omitted if absent)")
    ap.add_argument("--stage0-preflight-report", default=None,
                     help=("L2b: prior capacity_preflight_report.json from Stage 0 for "
                           "derived proxy-vs-measured comparison (wins over --groups-file "
                           "when both are set; emits a warning)"))
    ap.add_argument("--group-warn-threshold", type=int, default=15,
                     help="Warn if num_groups exceeds this (default: 15, a stated heuristic guess)")
    ap.add_argument("--fanout-warn-threshold", type=int, default=40,
                     help="Warn if total subagent fan-out exceeds this (default: 40, a stated heuristic guess)")
    ap.add_argument("--slice-tokens-warn-threshold", type=int, default=30_000,
                     help=("Warn if the largest single Stage-1 edge slice exceeds this "
                           "(default: 30000 — a quarter of the default 120000 per-group "
                           "budget; a stated guess with one real-repo data point behind "
                           "it, not a calibrated ceiling). Replaces the old "
                           "--references-tokens-warn-threshold, whose 500000 default "
                           "measured the removed broadcast and does not carry over."))
    ap.add_argument("--stage4-shared-tokens-warn-threshold", type=int, default=80_000,
                     help=("Warn if Stage-4 shared-pool est. tokens exceed this "
                           "(default: 80000 — stated guess pending documented mid-size "
                           "calibration; Stage-0 uses partial_proxy; L2b measured mode "
                           "warns on on-disk input sizes. Interview/returns omitted at "
                           "Stage 0; returns still omitted when measuring)."))
    ap.add_argument("--out", default=None, help="Optional path to write the report as JSON")
    return ap


def _maybe_write_report(path, report):
    from doc_engine.tools import capacity_preflight as cap

    if path:
        out = cap.checked_output_path(path)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)


def _print_warnings(report):
    if report["warnings"]:
        print(f"{len(report['warnings'])} warning(s):")
        for w in report["warnings"]:
            print(f"  - [{w['dimension']}] {w['message']}")
        return
    print("No thresholds crossed.")


def _load_optional_json(path):
    from doc_engine.tools import capacity_preflight as cap

    if not path:
        return None
    validated = cap.checked_path(path, want="file")
    with open(validated, encoding="utf-8") as f:
        return json.load(f)


def _print_l2b_summary(report):
    cmp_ = report.get("stage4_proxy_comparison")
    cmp_note = ""
    if cmp_ and cmp_.get("measured_over_proxy_ratio") is not None:
        cmp_note = (
            f"; measured/proxy ratio≈{cmp_['measured_over_proxy_ratio']:.3f}"
        )
    interview_note = (
        " omitted" if report["stage4_interview_answers_omitted"] else ""
    )
    signals_note = " omitted" if report["stage4_signals_omitted"] else ""
    print(
        f"capacity-preflight (L2b measured_stage4_inputs): shared-pool ~"
        f"{report['stage4_shared_pool_upper_bound_est_tokens']} est. tokens "
        f"(summaries≈{report['stage4_summaries_est_tokens']}, "
        f"interview≈{report['stage4_interview_answers_est_tokens']}"
        f"{interview_note}, "
        f"signals≈{report['stage4_signals_est_tokens']}"
        f"{signals_note}; "
        f"omitted: {', '.join(report['stage4_omitted_not_estimated'])}"
        f"{cmp_note})."
    )
    _print_warnings(report)


def _run_l2b_calibration(args, repo_path):
    """L2b path: measure Stage-4 inputs from on-disk summaries (+ optional extras)."""
    from doc_engine.tools import capacity_preflight as cap

    summaries_path = cap.checked_path(args.summaries_file, want="file")
    with open(summaries_path, encoding="utf-8") as f:
        summaries_data = json.load(f)
    interview_answers = _load_optional_json(args.interview_answers_file)
    signals_data = _load_optional_json(args.signals_file)
    groups_data = None
    if args.groups_file:
        groups_data = cap._load_or_build_groups(
            repo_path, args.max_tokens, args.overlap, args.groups_file,
        )
    stage0_report = _load_optional_json(args.stage0_preflight_report)
    report = cap.compute_stage4_calibration(
        repo_path,
        summaries_data=summaries_data,
        interview_answers=interview_answers,
        signals_data=signals_data,
        groups_data=groups_data,
        stage0_preflight_report=stage0_report,
        stage4_shared_tokens_warn_threshold=args.stage4_shared_tokens_warn_threshold,
    )
    _maybe_write_report(args.out, report)
    _print_l2b_summary(report)


def _print_stage0_summary(report):
    reduction = report["edge_join_stats"].get("reduction_factor")
    reduction_note = f", {reduction}x smaller than broadcasting" if reduction else ""
    signals_omitted_note = (
        "; signals_omitted" if report["stage4_signals_omitted"] else ""
    )
    print(f"capacity-preflight: {report['num_groups']} groups, "
          f"{report['total_fanout']} total subagent dispatches, "
          f"largest Stage-1 edge slice ~{report['stage1_slice_est_tokens_max']} est. tokens "
          f"(~{report['stage1_slice_est_tokens_total']} across all groups{reduction_note}); "
          f"Stage-4 shared-pool partial_proxy_pre_stage4 ~"
          f"{report['stage4_shared_pool_upper_bound_est_tokens']} "
          f"(omitted: {', '.join(report['stage4_omitted_not_estimated'])}"
          f"{signals_omitted_note}).")
    _print_warnings(report)


def _run_stage0_preflight(args, repo_path):
    """Stage-0 path: partition + edge join + partial Stage-4 proxy."""
    from doc_engine.tools import capacity_preflight as cap

    groups_data = cap._load_or_build_groups(
        repo_path, args.max_tokens, args.overlap, args.groups_file,
    )
    signals_data = _load_optional_json(args.signals_file)
    try:
        # Order matters here in a way it did not before: the join consumes
        # the partition, so groups_data must be built first.
        edges = cap._load_or_build_edges(
            repo_path, args.signals_file, groups_data, args.edges_file,
        )
    except cap.spring_signal_scan.AstGrepError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    report = cap.compute_preflight(
        repo_path, max_tokens=args.max_tokens, overlap=args.overlap,
        groups_data=groups_data, edges=edges, signals_data=signals_data,
        group_warn_threshold=args.group_warn_threshold,
        fanout_warn_threshold=args.fanout_warn_threshold,
        slice_tokens_warn_threshold=args.slice_tokens_warn_threshold,
        stage4_shared_tokens_warn_threshold=args.stage4_shared_tokens_warn_threshold,
    )
    _maybe_write_report(args.out, report)
    _print_stage0_summary(report)


def main():
    from doc_engine.tools import capacity_preflight as cap

    args = _build_arg_parser().parse_args()
    try:
        repo_path = str(cap.checked_path(args.repo_path, want="dir"))
    except cap.PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.summaries_file:
            cap._run_l2b_calibration(args, repo_path)
            return
        cap._run_stage0_preflight(args, repo_path)
    except cap.PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
