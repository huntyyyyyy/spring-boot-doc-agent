"""Ratchet file LOC and function statement-count ceilings (must not rise).

Usage:
    doc-engine size-ratchet
    python -m doc_engine.ci.size_ratchet --update

Heuristics (CONTRIBUTING.md):
    Prefer files ~200–500 LOC; smell at >1000. Prefer functions one-screen
    (~20–50 statements). Soft ceilings print advisories; hard ceilings are
    enforced via a committed ratchet baseline like complexipy.

Hard fail when:
    - a new file exceeds FILE_LOC_HARD, or a baselined file's LOC grows
    - a new function exceeds FN_STMTS_HARD, or a baselined function's
      statement count grows
    - hard-offender *counts* rise vs the baseline

Improvements are allowed without ``--update``; re-baseline downward after
remediation batches. Soft-threshold advisories never affect the exit code.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from doc_engine.ci.gate_tools import REPO_ROOT, checked_path_under_repo

PACKAGE_ROOTS = ("src/doc_engine", "src/stf")
FILE_LOC_HARD = 1000
FILE_LOC_SOFT = 500
FN_STMTS_HARD = 50
FN_STMTS_SOFT = 20
DEFAULT_BASELINE = REPO_ROOT / "scripts" / "ratchets" / "size_baseline.json"
SCHEMA_VERSION = 1


def _line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _strip_leading_docstring(body: list) -> list:
    if not body:
        return body
    first = body[0]
    if not isinstance(first, ast.Expr):
        return body
    value = getattr(first, "value", None)
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return body[1:]
    return body


def _is_definition(stmt: ast.AST) -> bool:
    return isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))


def statement_count(node: ast.AST) -> int:
    """Count statements in *node*, excluding docstring and nested defs."""
    total = 0
    stack = list(_strip_leading_docstring(list(getattr(node, "body", []))))
    while stack:
        stmt = stack.pop()
        if _is_definition(stmt):
            continue
        total += 1
        stack.extend(_nested_blocks(stmt))
    return total


def _nested_blocks(stmt: ast.AST) -> list:
    nested: list = []
    for field in ("body", "orelse", "finalbody", "handlers"):
        nested.extend(getattr(stmt, field, []) or [])
    return nested


def _record_function(
    child: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> str:
    qual = f"{prefix}{child.name}"
    key = f"{relpath}::{qual}"
    stmts = statement_count(child)
    prior = out.get(key)
    out[key] = stmts if prior is None else max(prior, stmts)
    return qual


def _visit_child(
    child: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> None:
    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
        qual = _record_function(child, prefix, relpath, out)
        _visit_functions(child, f"{qual}.", relpath, out)
        return
    if isinstance(child, ast.ClassDef):
        _visit_functions(child, f"{prefix}{child.name}.", relpath, out)
        return
    _visit_functions(child, prefix, relpath, out)


def _visit_functions(
    node: ast.AST, prefix: str, relpath: str, out: Dict[str, int]
) -> None:
    for child in ast.iter_child_nodes(node):
        _visit_child(child, prefix, relpath, out)


def _py_files_under(root: Path) -> List[Path]:
    return [
        path
        for path in sorted(root.rglob("*.py"))
        if "__pycache__" not in path.parts
    ]


def iter_package_py_files(roots: Iterable[str] = PACKAGE_ROOTS) -> List[Path]:
    """Return sorted ``.py`` paths under package roots (skip ``__pycache__``)."""
    files: List[Path] = []
    for root_name in roots:
        root = REPO_ROOT / root_name
        if root.is_dir():
            files.extend(_py_files_under(root))
    return files


def measure_tree(
    roots: Iterable[str] = PACKAGE_ROOTS,
) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Return (file_loc, function_statements) keyed by repo-relative paths."""
    file_loc: Dict[str, int] = {}
    functions: Dict[str, int] = {}
    for path in iter_package_py_files(roots):
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        file_loc[rel] = _line_count(text)
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        _visit_functions(tree, "", rel, functions)
    return file_loc, functions


def hard_file_offenders(file_loc: Dict[str, int]) -> Dict[str, int]:
    return {k: v for k, v in sorted(file_loc.items()) if v > FILE_LOC_HARD}


def hard_fn_offenders(functions: Dict[str, int]) -> Dict[str, int]:
    return {k: v for k, v in sorted(functions.items()) if v > FN_STMTS_HARD}


def _soft_file_notes(file_loc: Dict[str, int]) -> List[str]:
    return [
        f"[advisory] file {path} has loc={loc} (soft>{FILE_LOC_SOFT})"
        for path, loc in sorted(file_loc.items())
        if FILE_LOC_SOFT < loc <= FILE_LOC_HARD
    ]


def _soft_fn_notes(functions: Dict[str, int]) -> List[str]:
    return [
        f"[advisory] function {key} has statements={stmts} (soft>{FN_STMTS_SOFT})"
        for key, stmts in sorted(functions.items())
        if FN_STMTS_SOFT < stmts <= FN_STMTS_HARD
    ]


def soft_advisories(
    file_loc: Dict[str, int], functions: Dict[str, int]
) -> List[str]:
    return _soft_file_notes(file_loc) + _soft_fn_notes(functions)


def _offender_delta(kind: str, key: str, prior: int | None, value: int) -> str | None:
    if prior is None:
        return f"new {kind} offender {key}={value}"
    if value > prior:
        return f"{kind} offender grew: {key} {prior} -> {value}"
    return None


def compare_offenders(
    kind: str,
    baseline: Dict[str, int],
    current: Dict[str, int],
) -> List[str]:
    """Hard failures for new offenders or growth of baselined values."""
    issues: List[str] = []
    if len(current) > len(baseline):
        issues.append(
            f"{kind} hard-offender count rose {len(baseline)} -> {len(current)}"
        )
    for key, value in sorted(current.items()):
        note = _offender_delta(kind, key, baseline.get(key), value)
        if note is not None:
            issues.append(note)
    return issues


def build_baseline_payload(
    file_offenders: Dict[str, int], fn_offenders: Dict[str, int]
) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "package_roots": list(PACKAGE_ROOTS),
        "file_loc_hard": FILE_LOC_HARD,
        "file_loc_soft": FILE_LOC_SOFT,
        "fn_stmts_hard": FN_STMTS_HARD,
        "fn_stmts_soft": FN_STMTS_SOFT,
        "file_offender_count": len(file_offenders),
        "fn_offender_count": len(fn_offenders),
        "files": file_offenders,
        "functions": fn_offenders,
        "note": (
            "Hard ceilings: file LOC > "
            f"{FILE_LOC_HARD}, function statements > {FN_STMTS_HARD}. "
            "Soft advisories print above "
            f"{FILE_LOC_SOFT} LOC / {FN_STMTS_SOFT} statements. "
            "Ratchet offender maps downward only — never raise. "
            "Remeasure with: doc-engine size-ratchet --update"
        ),
    }


def write_baseline(
    path: Path, file_offenders: Dict[str, int], fn_offenders: Dict[str, int]
) -> None:
    path = checked_path_under_repo(path)
    payload = build_baseline_payload(file_offenders, fn_offenders)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_baseline(path: Path) -> dict:
    path = checked_path_under_repo(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        print(
            f"error: baseline schema_version {data.get('schema_version')!r} "
            f"!= {SCHEMA_VERSION}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return data


def compare(baseline: dict, file_loc: Dict[str, int], functions: Dict[str, int]) -> List[str]:
    """Return hard-failure messages for size-ratchet regressions."""
    file_off = hard_file_offenders(file_loc)
    fn_off = hard_fn_offenders(functions)
    issues: List[str] = []
    issues.extend(compare_offenders("file", baseline.get("files", {}), file_off))
    issues.extend(compare_offenders("function", baseline.get("functions", {}), fn_off))
    return issues


def _print_soft_advisories(advisories: List[str]) -> None:
    if not advisories:
        return
    print(f"size soft advisories ({len(advisories)}):")
    for note in advisories[:40]:
        print(f"  {note}")
    if len(advisories) > 40:
        print(f"  … {len(advisories) - 40} more")


def _print_issues(issues: List[str]) -> None:
    print(f"size ratchet failed ({len(issues)} issue(s)):", file=sys.stderr)
    for issue in issues:
        print(f"  - {issue}", file=sys.stderr)


def _note_if_dropped(baseline: dict, file_off: Dict[str, int], fn_off: Dict[str, int]) -> None:
    file_drop = len(file_off) < int(baseline.get("file_offender_count", 0))
    fn_drop = len(fn_off) < int(baseline.get("fn_offender_count", 0))
    if file_drop or fn_drop:
        print(
            "note: hard-offender count dropped; "
            "re-baseline with --update to ratchet downward"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="committed baseline JSON path",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="rewrite baseline from the current hard-offender maps",
    )
    args = parser.parse_args(argv)

    file_loc, functions = measure_tree()
    file_off = hard_file_offenders(file_loc)
    fn_off = hard_fn_offenders(functions)

    if args.update:
        write_baseline(args.baseline, file_off, fn_off)
        print(
            f"baseline written: {args.baseline} "
            f"(files={len(file_off)}, functions={len(fn_off)})"
        )
        return 0

    if not args.baseline.is_file():
        print(
            f"error: no baseline at {args.baseline}; create one with --update",
            file=sys.stderr,
        )
        return 2

    baseline = load_baseline(args.baseline)
    print(
        f"size ratchet: file_offenders={len(file_off)} "
        f"(ceiling={baseline.get('file_offender_count')}) "
        f"fn_offenders={len(fn_off)} "
        f"(ceiling={baseline.get('fn_offender_count')}) "
        f"(file_loc_hard={FILE_LOC_HARD}, fn_stmts_hard={FN_STMTS_HARD})"
    )
    issues = compare(baseline, file_loc, functions)
    _print_soft_advisories(soft_advisories(file_loc, functions))
    if issues:
        _print_issues(issues)
        return 1
    _note_if_dropped(baseline, file_off, fn_off)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
