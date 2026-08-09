"""Argparse surface for in-repo quality / size / coverage gate commands."""

from __future__ import annotations

from typing import Any, Callable


def _configure_coverage_measure_parser(
    measure_ap: Any,
    *,
    cmd_coverage_measure: Callable[..., int],
) -> None:
    measure_ap.add_argument(
        "--mode",
        choices=("oracle", "climb"),
        default=None,
        help="oracle=whole-repo SoT (default); climb=scoped sensor",
    )
    measure_ap.add_argument(
        "--scope",
        default=None,
        help="Package for climb --cov=<scope> (required with --mode climb)",
    )
    measure_ap.add_argument("--floor", type=float, default=None)
    measure_ap.add_argument("--worst", type=int, default=None)
    measure_ap.add_argument("--skip-pytest", action="store_true")
    measure_ap.add_argument("--no-gap-report", action="store_true")
    measure_ap.add_argument(
        "pytest_args",
        nargs="*",
        help="Extra pytest args after standard cov flags",
    )
    measure_ap.set_defaults(func=cmd_coverage_measure)


def add_quality_gate_parsers(
    sub: Any,
    *,
    cmd_quality_gates: Callable[..., int],
    cmd_coverage_gap_average: Callable[..., int],
    cmd_coverage_measure: Callable[..., int],
    cmd_complexipy_ratchet: Callable[..., int],
    cmd_size_ratchet: Callable[..., int],
) -> None:
    qg_ap = sub.add_parser(
        "quality-gates",
        help=(
            "Hard in-repo gates: new-code coverage, jscpd, complexipy <=5, "
            "size ratchet, tach (same on Mac/Windows/Linux)"
        ),
    )
    qg_ap.add_argument(
        "--compare-ref",
        required=True,
        help="Git ref for new-code baseline (PR base SHA, origin/main, HEAD~1)",
    )
    qg_ap.add_argument(
        "--coverage-xml",
        default=None,
        help="Cobertura XML from pytest-cov (default: ./coverage.xml)",
    )
    qg_ap.add_argument(
        "--skip-coverage",
        action="store_true",
        help="Skip diff-cover (local debug only)",
    )
    qg_ap.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Run every gate even after a failure",
    )
    qg_ap.set_defaults(func=cmd_quality_gates)

    gap_ap = sub.add_parser(
        "coverage-gap-average",
        help="Report Cover% averaged only over files still below the floor",
    )
    gap_ap.add_argument("--coverage-xml", default=None)
    gap_ap.add_argument("--floor", type=float, default=None)
    gap_ap.add_argument("--worst", type=int, default=None)
    gap_ap.add_argument("--markdown", action="store_true")
    gap_ap.add_argument("--append-github-summary", action="store_true")
    gap_ap.set_defaults(func=cmd_coverage_gap_average)

    measure_ap = sub.add_parser(
        "coverage-measure",
        help=(
            "Clean single-tree coverage measure "
            "(oracle SoT or climb sensor; policy 16-A)"
        ),
    )
    _configure_coverage_measure_parser(
        measure_ap, cmd_coverage_measure=cmd_coverage_measure
    )

    ratchet_ap = sub.add_parser(
        "complexipy-ratchet",
        help="Ratchet complexipy offender count vs scripts/ratchets baseline",
    )
    ratchet_ap.add_argument("--baseline", default=None)
    ratchet_ap.add_argument("--update", action="store_true")
    ratchet_ap.set_defaults(func=cmd_complexipy_ratchet)

    size_ap = sub.add_parser(
        "size-ratchet",
        help="Ratchet file LOC / function statement hard ceilings vs baseline",
    )
    size_ap.add_argument("--baseline", default=None)
    size_ap.add_argument("--update", action="store_true")
    size_ap.set_defaults(func=cmd_size_ratchet)
