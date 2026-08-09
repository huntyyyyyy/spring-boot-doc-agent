"""CLI: python -m stf …"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from stf.adapters.gh_handoff import handoff_gh, write_handoff_checklist
from stf.cli_parser import build_parser as _build_stf_parser
from stf.ingest.review import findings_to_spec_seed, ingest_review_path
from stf.runners.implement import constitution_excerpts, plan_gate, run_waves, verify_gate
from stf.runners.store import SpecStore, TasksStore, write_change_pack
from stf.schemas.tasks import LedgerState, TaskBlock, TasksDocument
from stf.validators.lint_tasks import lint_summary, lint_tasks_document, mutate_tasks


def _cmd_ingest(args: argparse.Namespace) -> int:
    findings = ingest_review_path(Path(args.review))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = [f.model_dump(mode="json") for f in findings]
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.spec_dir:
        seed = findings_to_spec_seed(
            findings, target=args.target, source_review=str(args.review)
        )
        store = SpecStore(Path(args.spec_dir))
        store.write_spec(seed)
        write_change_pack(
            Path(args.spec_dir),
            added=[f"{f.id}: {f.title}" for f in findings if f.id.startswith("C")],
            modified=[f"{f.id}: {f.title}" for f in findings if f.id.startswith(("H", "N"))],
            removed=["Caller-supplied MCP root", "AssumeIndexed as default freshness lie"],
        )
    print(json.dumps({"findings": len(findings), "out": str(out)}, indent=2))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    tasks = store.load_tasks()
    spec = None
    spec_path = Path(args.target_dir) / "SPEC.json"
    if spec_path.is_file():
        spec = SpecStore(Path(args.target_dir)).load_spec()
    results = lint_tasks_document(tasks, spec, root=Path(args.root) if args.root else None)
    summary = lint_summary(results)
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


def _cmd_plan_gate(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    tasks = store.load_tasks()
    spec = SpecStore(Path(args.target_dir)).load_spec() if (Path(args.target_dir) / "SPEC.json").is_file() else None
    try:
        result = plan_gate(tasks, spec)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    print(json.dumps({"ok": True, "waves": result["waves"], "finding_coverage": result["finding_coverage"]}))
    return 0


def _cmd_seed_tasks(args: argparse.Namespace) -> int:
    """Create a minimal valid TASKS.json from SPEC for remediation targets."""
    spec = SpecStore(Path(args.target_dir)).load_spec()
    tasks_list = [
        TaskBlock(
            id="T0",
            title="Pre-flight probes",
            goal="Reproduce critical findings with fail bars",
            inputs=[{"origin": "new", "datum": "probe harness"}],
            depends=[],
            gates=[f"INV-{fid}" for fid in spec.finding_ids if fid.startswith("C")][:3] or [],
            tests="Record baseline pytest node ids for C1/C2",
            verify="python -m pytest tests/doc_engine/test_query_artifacts.py -q --collect-only",
            acceptance="Critical probes documented; suite baseline recorded",
            data_modeling="n/a — probe",
            locate="n/a",
            implement="n/a — probe only",
        )
    ]
    wave1_deps = ["T0"]
    for i, row in enumerate(spec.inventory[:8], start=1):
        tid = f"T{i}"
        tasks_list.append(
            TaskBlock(
                id=tid,
                title=row.data_need[:80],
                goal=f"Address {row.id}",
                inputs=[{"origin": row.id, "datum": row.data_need}],
                depends=list(wave1_deps),
                tests=f"Deviation test for {row.id}",
                verify=f"python -m pytest tests/stf -q -k {row.id.replace('-', '_')}",
                acceptance=f"{row.id} remediated",
                locate=row.origin if "/" in row.origin else "src/doc_engine/query/",
                implement=f"Fix {row.id}",
                data_modeling="n/a",
            )
        )
    doc = TasksDocument(
        target=spec.target,
        source_spec=str(Path(args.target_dir) / "SPEC.md"),
        why_this_order="T0 probes first; inventory remediation depends on T0; critical before polish.",
        decisions=spec.decisions,
        tasks=tasks_list,
        ledger=LedgerState.PLAN,
    )
    TasksStore(Path(args.target_dir)).write_tasks(doc)
    print(json.dumps({"tasks": len(tasks_list), "target": spec.target}))
    return 0


def _cmd_implement(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    if args.plan_gate:
        spec = SpecStore(Path(args.target_dir)).load_spec()
        plan_gate(store.load_tasks(), spec)
    result = run_waves(store, start_wave=args.resume_wave)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_reviewer_token(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    token = store.issue_validation_token()
    print(json.dumps({"validation_token": token}))
    return 0


def _cmd_mark_done(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    try:
        store.mark_done(validation_token=args.token)
    except PermissionError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    print(json.dumps({"ok": True, "ledger": "done"}))
    return 0


def _cmd_handoff(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    tasks = store.load_tasks()
    if args.checklist:
        path = write_handoff_checklist(Path(args.checklist), tasks)
        print(json.dumps({"checklist": str(path)}))
    else:
        created = handoff_gh(tasks, dry_run=not args.create)
        print(json.dumps(created, indent=2))
    return 0


def _cmd_constitution(args: argparse.Namespace) -> int:
    text = constitution_excerpts(Path(args.repo_root))
    Path(args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"chars": len(text), "out": args.out}))
    return 0


def _cmd_mutate(args: argparse.Namespace) -> int:
    store = TasksStore(Path(args.target_dir))
    mutated = mutate_tasks(store.load_tasks(), args.mode)
    out = Path(args.out) if args.out else Path(args.target_dir) / f"TASKS.mutant.{args.mode}.json"
    out.write_text(mutated.model_dump_json(indent=2), encoding="utf-8")
    results = lint_tasks_document(mutated)
    summary = lint_summary(results)
    print(json.dumps({"mode": args.mode, "lint_ok": summary["ok"], "fail": summary["fail"]}))
    # mutants should fail lint
    return 0 if not summary["ok"] else 1


def _cmd_verify_gate(args: argparse.Namespace) -> int:
    cmds = args.cmd or []
    try:
        result = verify_gate(verify_commands=cmds)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    print(json.dumps(result))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Public CLI parser; handlers stay wired in this module."""
    return _build_stf_parser(
        commands={
            "ingest": _cmd_ingest,
            "validate": _cmd_validate,
            "plan_gate": _cmd_plan_gate,
            "seed_tasks": _cmd_seed_tasks,
            "implement": _cmd_implement,
            "reviewer_token": _cmd_reviewer_token,
            "mark_done": _cmd_mark_done,
            "handoff": _cmd_handoff,
            "constitution": _cmd_constitution,
            "mutate": _cmd_mutate,
            "verify_gate": _cmd_verify_gate,
        }
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
