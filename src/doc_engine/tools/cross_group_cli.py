"""CLI for build_cross_group_edges."""

from __future__ import annotations

import argparse
import json
import sys

from doc_engine.tools.cross_group_emit import build_report


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("groups_file", help="groups.json from partition_repo.py")
    ap.add_argument("signals_file", help="spring_signals.json from spring_signal_scan.py")
    ap.add_argument("--out", default="cross_group_edges.json")
    args = ap.parse_args()

    try:
        groups_data = json.load(open(args.groups_file, encoding="utf-8"))
        signals_data = json.load(open(args.signals_file, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    report = build_report(groups_data, signals_data)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)

    s = report["stats"]
    print(
        f"Wrote {args.out}. {report['num_groups']} groups, "
        f"{s.get('cut_arcs', 0)} cut arcs "
        f"(exact={s.get('confidence_exact', 0)}, fanout={s.get('confidence_package-fanout', 0)}), "
        f"{s.get('same_package_adjacency_rows', 0)} same-package adjacency rows. "
        f"{s['rows_shipped']} rows shipped vs {s['broadcast_rows_avoided']} broadcast"
        # reduction_factor is None when nothing was shipped (a single-group
        # repo has no cut by definition), and interpolating that printed
        # "Nonex reduction". The JSON was always correct; only this line lied.
        + (f" ({s['reduction_factor']}x reduction)." if s.get("reduction_factor") else ".")
    )
    return 0
