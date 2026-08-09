"""Argparse surface for ``python -m stf`` (subcommands + defaults)."""

from __future__ import annotations

import argparse
from typing import Any, Callable


def _add_ingest_and_validate(
    sub: Any,
    *,
    cmd_ingest: Callable,
    cmd_validate: Callable,
) -> None:
    ing = sub.add_parser(
        "ingest-review", help="Review MD → Findings JSON (+ optional SPEC seed)"
    )
    ing.add_argument("--review", required=True)
    ing.add_argument("--out", required=True)
    ing.add_argument("--spec-dir")
    ing.add_argument("--target", default="pr-94-query-surface")
    ing.set_defaults(func=cmd_ingest)

    val = sub.add_parser("validate", help="Lint TASKS.json (+ SPEC.json)")
    val.add_argument("--target-dir", required=True)
    val.add_argument("--root", help="fixture root for Locate anchors")
    val.set_defaults(func=cmd_validate)


def _add_plan_and_seed(
    sub: Any,
    *,
    cmd_plan_gate: Callable,
    cmd_seed_tasks: Callable,
) -> None:
    pg = sub.add_parser("plan-gate", help="SPOQ plan gate before Wave 1")
    pg.add_argument("--target-dir", required=True)
    pg.set_defaults(func=cmd_plan_gate)

    st = sub.add_parser("seed-tasks", help="Seed TASKS.json from SPEC.json")
    st.add_argument("--target-dir", required=True)
    st.set_defaults(func=cmd_seed_tasks)


def _add_implement_and_tokens(
    sub: Any,
    *,
    cmd_implement: Callable,
    cmd_reviewer_token: Callable,
    cmd_mark_done: Callable,
) -> None:
    imp = sub.add_parser("implement", help="Run topological waves")
    imp.add_argument("--target-dir", required=True)
    imp.add_argument("--plan-gate", action="store_true")
    imp.add_argument("--resume-wave", type=int, default=None)
    imp.set_defaults(func=cmd_implement)

    tok = sub.add_parser("reviewer-token", help="Issue 2+N validation token")
    tok.add_argument("--target-dir", required=True)
    tok.set_defaults(func=cmd_reviewer_token)

    done = sub.add_parser("mark-done", help="Mark DONE with Reviewer token")
    done.add_argument("--target-dir", required=True)
    done.add_argument("--token", required=True)
    done.set_defaults(func=cmd_mark_done)


def _add_handoff_and_constitution(
    sub: Any,
    *,
    cmd_handoff: Callable,
    cmd_constitution: Callable,
) -> None:
    ho = sub.add_parser("handoff-gh", help="Create gh issues or checklist")
    ho.add_argument("--target-dir", required=True)
    ho.add_argument("--create", action="store_true", help="actually call gh")
    ho.add_argument("--checklist", help="write markdown checklist path")
    ho.set_defaults(func=cmd_handoff)

    con = sub.add_parser("constitution", help="Emit CONSTRAINTS+CLAUDE excerpts")
    con.add_argument("--repo-root", default=".")
    con.add_argument("--out", required=True)
    con.set_defaults(func=cmd_constitution)


def _add_mutate_and_verify(
    sub: Any,
    *,
    cmd_mutate: Callable,
    cmd_verify_gate: Callable,
) -> None:
    mut = sub.add_parser("mutate", help="Apply named lint mutant")
    mut.add_argument("--target-dir", required=True)
    mut.add_argument("--mode", required=True)
    mut.add_argument("--out")
    mut.set_defaults(func=cmd_mutate)

    vg = sub.add_parser("verify-gate", help="Run verify gate (dry-run if no exec)")
    vg.add_argument("--cmd", action="append", default=[])
    vg.set_defaults(func=cmd_verify_gate)


def build_parser(*, commands: dict[str, Callable]) -> argparse.ArgumentParser:
    """Build the stf CLI parser; ``commands`` maps names to handlers."""
    p = argparse.ArgumentParser(prog="stf", description="Spec Task Framework CLI")
    sub = p.add_subparsers(dest="command", required=True)
    _add_ingest_and_validate(
        sub, cmd_ingest=commands["ingest"], cmd_validate=commands["validate"]
    )
    _add_plan_and_seed(
        sub, cmd_plan_gate=commands["plan_gate"], cmd_seed_tasks=commands["seed_tasks"]
    )
    _add_implement_and_tokens(
        sub,
        cmd_implement=commands["implement"],
        cmd_reviewer_token=commands["reviewer_token"],
        cmd_mark_done=commands["mark_done"],
    )
    _add_handoff_and_constitution(
        sub,
        cmd_handoff=commands["handoff"],
        cmd_constitution=commands["constitution"],
    )
    _add_mutate_and_verify(
        sub, cmd_mutate=commands["mutate"], cmd_verify_gate=commands["verify_gate"]
    )
    return p
