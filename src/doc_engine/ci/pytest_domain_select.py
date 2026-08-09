"""Deterministic path → domain pytest argv for local pre_pr (E-SEL1).

Closed prefix map (NameRTS-shaped). Unknown code paths fail-closed to full
``tests/``. Never skips the merge oracle cell.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from doc_engine.ci.test_path_shards import paths_for_marker

# Longest-prefix-first product / test trees → parallel domain markers.
_PREFIX_MARKERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("src/doc_engine/ci/", ("domain_ci_meta",)),
    ("scripts/ci/", ("domain_ci_meta",)),
    ("scripts/ratchets/", ("domain_ci_meta",)),
    ("scripts/coverage/", ("domain_ci_meta",)),
    ("tests/ci/", ("domain_ci_meta",)),
    ("tests/ratchets/", ("domain_ci_meta",)),
    ("tests/coverage/", ("domain_ci_meta",)),
    ("src/doc_engine/scanning/", ("domain_stage0",)),
    ("src/doc_engine/pipeline/", ("domain_pipeline",)),
    ("src/stf/", ("domain_stf",)),
    ("tests/stf/", ("domain_stf",)),
    ("tests/adapters/", ("domain_adapters",)),
    ("src/doc_engine/adapters/", ("domain_adapters",)),
    ("tests/spring_signals/", ("domain_stage0",)),
)


@dataclass(frozen=True)
class PytestSelectPlan:
    """Local pytest selection plan (sensor / pre_pr only)."""

    mode: str  # "full" | "domains"
    markers: tuple[str, ...]
    paths: tuple[str, ...]

    def argv(self, *, junitxml: str | None = None) -> list[str]:
        args: list[str] = ["-q", "--tb=line"]
        if junitxml:
            args.append(f"--junitxml={junitxml}")
        if self.mode == "full":
            args.append("tests/")
            return args
        args.extend(self.paths)
        expr = " or ".join(self.markers)
        args.extend(["-m", expr])
        return args


def normalize_repo_path(raw: str) -> str:
    norm = raw.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm


def markers_for_paths(paths: list[str]) -> frozenset[str] | None:
    """Return selected markers, or None to run the full suite (fail-closed)."""
    if not paths:
        return None
    selected: set[str] = set()
    for raw in paths:
        outcome = _accumulate_path(normalize_repo_path(raw), selected)
        if outcome == "full":
            return None
    return frozenset(selected) if selected else None


def _accumulate_path(norm: str, selected: set[str]) -> str:
    """Return 'ok' or 'full' when this path forces the whole suite."""
    matched = _markers_for_one(norm)
    if matched is not None:
        selected.update(matched)
        return "ok"
    if _looks_like_code(norm):
        return "full"
    return "ok"


def _markers_for_one(norm: str) -> tuple[str, ...] | None:
    for prefix, markers in sorted(_PREFIX_MARKERS, key=lambda item: -len(item[0])):
        if norm == prefix.rstrip("/") or norm.startswith(prefix):
            return markers
    return None


def _looks_like_code(norm: str) -> bool:
    return norm.endswith(".py") or norm.startswith(("src/", "scripts/", "tests/"))


def build_select_plan(
    repo: Path,
    changed_paths: list[str],
    *,
    force_full: bool,
) -> PytestSelectPlan:
    """Build a selection plan; force_full or unknown → full suite."""
    if force_full:
        return PytestSelectPlan(mode="full", markers=(), paths=("tests/",))
    markers = markers_for_paths(changed_paths)
    if markers is None:
        return PytestSelectPlan(mode="full", markers=(), paths=("tests/",))
    ordered = tuple(sorted(markers))
    paths: list[str] = []
    for marker in ordered:
        paths.extend(paths_for_marker(repo, marker))
    unique = _dedupe_paths(paths)
    if not unique:
        return PytestSelectPlan(mode="full", markers=(), paths=("tests/",))
    return PytestSelectPlan(mode="domains", markers=ordered, paths=tuple(unique))


def _dedupe_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out
