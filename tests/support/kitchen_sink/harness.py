"""Kitchen-sink assertion helpers (ports stay in chain / tool_invoke)."""

from __future__ import annotations

import os

from tests.support.kitchen_sink.chain import _git, _run, run_chain
from tests.support.kitchen_sink.repo_builder import build_enterprise_repo

__all__ = [
    "_run",
    "_git",
    "run_chain",
    "_evidence_files",
    "_grouped",
    "_miscase_first_tag",
    "_has_segment",
    "_kitchen_sink_real_repo",
    "build_enterprise_repo",
]


def _evidence_files(signals):
    for rows in (signals.get("evidence") or {}).values():
        for row in rows:
            yield row["file"]


def _grouped(groups):
    return {f for g in groups["groups"] for f in g["files"]}


def _miscase_first_tag(case, path):
    """Lowercase the first tag word in a doc, asserting the mutation landed.

    Without the assertion these tests pass vacuously against a document whose
    evidence bucket happened to be empty — the injected fault would simply not
    exist, and 'the gate did not fail' would prove nothing.
    """
    text = open(path, encoding="utf-8").read()
    mutated = text.replace("[Evidenced —", "[evidenced —", 1)
    case.assertNotEqual(text, mutated, f"{os.path.basename(path)} carried no tag to miscase")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(mutated)


def _has_segment(rel, name):
    """Segment-wise membership. A substring check would call
    'outbound/Client.java' an 'out' directory."""
    return name in rel.split("/")


def _kitchen_sink_real_repo() -> str | None:
    from doc_engine.real_fixture import real_repo_path

    path = real_repo_path()
    return str(path) if path is not None else None
