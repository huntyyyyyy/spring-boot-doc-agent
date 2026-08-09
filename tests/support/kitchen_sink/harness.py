"""Kitchen-sink module lifecycle and assertion helpers."""

from __future__ import annotations

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

def setUpModule():
    if not shutil.which("ast-grep"):
        raise unittest.SkipTest("ast-grep not on PATH")
    if not shutil.which("git"):
        raise unittest.SkipTest("git not on PATH")

    tmp = tempfile.mkdtemp(prefix="kitchensink_")
    repo = os.path.join(tmp, "repo")
    out_dir = os.path.join(tmp, "run")
    os.makedirs(out_dir)
    build_enterprise_repo(repo)

    # Identity on the command line, never ambient config — a bare commit on a
    # runner with no configured identity fails.
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=kitchensink@example.invalid",
         "-c", "user.name=kitchensink", "commit", "-qm", "init")

    steps, snapshots = run_chain(repo, out_dir)

    def load(name):
        with open(os.path.join(out_dir, name), encoding="utf-8") as f:
            return json.load(f)

    def load_facts():
        path = os.path.join(out_dir, "facts.jsonl")
        if not os.path.isfile(path):
            return []
        rows = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    _STATE.update({
        "tmp": tmp, "repo": repo, "out": out_dir, "steps": steps,
        "snapshots": snapshots, "docs": os.path.join(repo, "docs"),
        "signals": load("spring_signals.json"),
        "covering_proof": load("covering_proof.json"),
        "facts": load_facts(),
        "groups": load("groups.json"),
        "edges": load("cross_group_edges.json"),
        "manifest": load("run_manifest.json"),
        "preflight": load("capacity_preflight_report.json"),
    })



def tearDownModule():
    tmp = _STATE.get("tmp")
    if tmp and os.path.isdir(tmp):
        # ignore_errors: .git's read-only object files make rmtree fail on
        # Windows, and a leftover temp dir is harmless while a teardown
        # exception is a confusing red run.
        shutil.rmtree(tmp, ignore_errors=True)



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

