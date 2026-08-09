"""Frozen kitchen-sink artifacts port (E-KH1 / K4 / K10)."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from tests.support.kitchen_sink.chain import _git, run_chain
from tests.support.kitchen_sink.repo_builder import build_enterprise_repo


@dataclass(frozen=True)
class KitchenArtifacts:
    """Read-only view of one amortized kitchen plant + chain run."""

    tmp: str
    repo: str
    out: str
    docs: str
    steps: Mapping[str, Any]
    snapshots: Sequence[tuple[str, dict]]
    signals: dict
    covering_proof: dict
    facts: Sequence[dict]
    groups: dict
    edges: dict
    manifest: dict
    preflight: dict


def _load_kitchen_json(out_dir: str, name: str) -> dict:
    with open(os.path.join(out_dir, name), encoding="utf-8") as handle:
        return json.load(handle)


def _load_kitchen_facts(out_dir: str) -> list[dict]:
    path = os.path.join(out_dir, "facts.jsonl")
    if not os.path.isfile(path):
        return []
    rows: list[dict] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _git_init_kitchen_repo(repo: str) -> None:
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


def build_kitchen_artifacts() -> KitchenArtifacts:
    """Create enterprise repo + full chain once; caller owns tmp cleanup."""
    tmp = tempfile.mkdtemp(prefix="kitchensink_")
    repo = os.path.join(tmp, "repo")
    out_dir = os.path.join(tmp, "run")
    os.makedirs(out_dir)
    build_enterprise_repo(repo)
    _git_init_kitchen_repo(repo)
    steps, snapshots = run_chain(repo, out_dir)
    return KitchenArtifacts(
        tmp=tmp,
        repo=repo,
        out=out_dir,
        docs=os.path.join(repo, "docs"),
        steps=steps,
        snapshots=snapshots,
        signals=_load_kitchen_json(out_dir, "spring_signals.json"),
        covering_proof=_load_kitchen_json(out_dir, "covering_proof.json"),
        facts=_load_kitchen_facts(out_dir),
        groups=_load_kitchen_json(out_dir, "groups.json"),
        edges=_load_kitchen_json(out_dir, "cross_group_edges.json"),
        manifest=_load_kitchen_json(out_dir, "run_manifest.json"),
        preflight=_load_kitchen_json(out_dir, "capacity_preflight_report.json"),
    )
