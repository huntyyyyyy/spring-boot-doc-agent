"""Kitchen-sink module lifecycle and assertion helpers."""

from __future__ import annotations

import atexit
import json
import os
import shutil
import tempfile
import unittest

from tests.support.kitchen_sink.chain import _git, _run, run_chain
from tests.support.kitchen_sink.constants import _STATE
from tests.support.kitchen_sink.repo_builder import build_enterprise_repo

# Re-export chain helpers for existing test imports.
__all__ = [
    "_STATE",
    "_run",
    "_git",
    "run_chain",
    "setUpModule",
    "tearDownModule",
    "_evidence_files",
    "_grouped",
    "_copy_docs",
    "_miscase_first_tag",
    "_has_segment",
    "_kitchen_sink_real_repo",
    "build_enterprise_repo",
]

_ATEXIT_CLEANUP_REGISTERED = False


def _cleanup_kitchen_sink_state() -> None:
    tmp = _STATE.pop("tmp", None)
    _STATE.clear()
    if tmp and os.path.isdir(tmp):
        # ignore_errors: .git's read-only object files make rmtree fail on
        # Windows, and a leftover temp dir is harmless while a teardown
        # exception is a confusing red run.
        shutil.rmtree(tmp, ignore_errors=True)


def _require_kitchen_sink_tools() -> None:
    if not shutil.which("ast-grep"):
        raise unittest.SkipTest("ast-grep not on PATH")
    if not shutil.which("git"):
        raise unittest.SkipTest("git not on PATH")


def _load_kitchen_json(out_dir: str, name: str):
    with open(os.path.join(out_dir, name), encoding="utf-8") as handle:
        return json.load(handle)


def _load_kitchen_facts(out_dir: str):
    path = os.path.join(out_dir, "facts.jsonl")
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _git_init_kitchen_repo(repo: str) -> None:
    # Identity on the command line, never ambient config — a bare commit on a
    # runner with no configured identity fails.
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(
        repo,
        "-c",
        "user.email=kitchensink@example.invalid",
        "-c",
        "user.name=kitchensink",
        "commit",
        "-qm",
        "init",
    )


def _build_kitchen_sink_state() -> None:
    """Create the shared enterprise repo + full chain artifacts in ``_STATE``."""
    global _ATEXIT_CLEANUP_REGISTERED
    _require_kitchen_sink_tools()
    tmp = tempfile.mkdtemp(prefix="kitchensink_")
    repo = os.path.join(tmp, "repo")
    out_dir = os.path.join(tmp, "run")
    os.makedirs(out_dir)
    build_enterprise_repo(repo)
    _git_init_kitchen_repo(repo)
    steps, snapshots = run_chain(repo, out_dir)
    _STATE.update({
        "tmp": tmp, "repo": repo, "out": out_dir, "steps": steps,
        "snapshots": snapshots, "docs": os.path.join(repo, "docs"),
        "signals": _load_kitchen_json(out_dir, "spring_signals.json"),
        "covering_proof": _load_kitchen_json(out_dir, "covering_proof.json"),
        "facts": _load_kitchen_facts(out_dir),
        "groups": _load_kitchen_json(out_dir, "groups.json"),
        "edges": _load_kitchen_json(out_dir, "cross_group_edges.json"),
        "manifest": _load_kitchen_json(out_dir, "run_manifest.json"),
        "preflight": _load_kitchen_json(out_dir, "capacity_preflight_report.json"),
    })
    if not _ATEXIT_CLEANUP_REGISTERED:
        atexit.register(_cleanup_kitchen_sink_state)
        _ATEXIT_CLEANUP_REGISTERED = True


def setUpModule():
    """Build+chain once; chapter modules share ``_STATE`` for the process.

    Each ``test_kitchen_sink_ch*.py`` re-exports this as its unittest
    ``setUpModule``. Without sharing, every chapter paid ~15s for the same
    ``run_chain`` (signal_scan → partition → … → drift).
    """
    if _STATE.get("tmp"):
        return
    _build_kitchen_sink_state()


def tearDownModule():
    # Shared across kitchen-sink chapter modules; atexit owns the rmtree so a
    # mid-suite tearDown does not force the next chapter to rebuild (~15s).
    return


def _evidence_files(signals):
    for rows in (signals.get("evidence") or {}).values():
        for row in rows:
            yield row["file"]


def _grouped(groups):
    return {f for g in groups["groups"] for f in g["files"]}


def _copy_docs():
    scratch = tempfile.mkdtemp(prefix="ks_docs_")
    shutil.copytree(_STATE["docs"], os.path.join(scratch, "docs"))
    return scratch, os.path.join(scratch, "docs")


def _miscase_first_tag(case, path):
    """Lowercase the first tag word in a doc, asserting the mutation landed.

    Without the assertion these tests pass vacuously against a document whose
    evidence bucket happened to be empty — the injected fault would simply not
    exist, and 'the gate did not fail' would prove nothing.
    """
    text = open(path, encoding="utf-8").read()
    mutated = text.replace("[Evidenced —", "[evidenced —", 1)
    case.assertNotEqual(text, mutated, f"{os.path.basename(path)} carried no tag to miscase")
    with open(path, "w", encoding="utf-8") as f:
        f.write(mutated)


def _has_segment(rel, name):
    """Segment-wise membership. A substring check would call
    'outbound/Client.java' an 'out' directory."""
    return name in rel.split("/")


def _kitchen_sink_real_repo() -> str | None:
    from doc_engine.real_fixture import real_repo_path

    path = real_repo_path()
    return str(path) if path is not None else None
