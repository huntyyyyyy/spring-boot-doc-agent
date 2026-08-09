"""Pytest fixtures for the kitchen-sink test BC (E-KH1; KH-S1 = session)."""

from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import Iterator

import pytest

from tests.support.kitchen_sink.artifacts import KitchenArtifacts, build_kitchen_artifacts


@pytest.fixture(scope="session")
def kitchen() -> Iterator[KitchenArtifacts]:
    """One plant+chain per process; treat as read-only (K4)."""
    if not shutil.which("ast-grep"):
        pytest.skip("ast-grep not on PATH")
    if not shutil.which("git"):
        pytest.skip("git not on PATH")
    artifacts = build_kitchen_artifacts()
    try:
        yield artifacts
    finally:
        shutil.rmtree(artifacts.tmp, ignore_errors=True)


@pytest.fixture
def kitchen_docs_scratch(kitchen: KitchenArtifacts) -> Iterator[tuple[str, str]]:
    """Function-scoped docs copy for fault injection."""
    scratch = tempfile.mkdtemp(prefix="ks_docs_")
    docs = os.path.join(scratch, "docs")
    shutil.copytree(kitchen.docs, docs)
    try:
        yield scratch, docs
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


@pytest.fixture
def kitchen_repo_copy(kitchen: KitchenArtifacts) -> Iterator[str]:
    """Function-scoped full repo copy for drift / stray-write faults."""
    scratch = tempfile.mkdtemp(prefix="ks_repo_")
    repo = os.path.join(scratch, "repo")
    shutil.copytree(kitchen.repo, repo)
    try:
        yield repo
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
