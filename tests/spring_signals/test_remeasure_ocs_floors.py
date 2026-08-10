"""Offline OCS floor remeasure via campaign ast-grep rules (E-OCS0 OCS6)."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.domain_stage0

REPO = Path(__file__).resolve().parents[2]

def _load_remeasure():
    path = REPO / "scripts" / "ci" / "remeasure_ocs_floors.py"
    spec = importlib.util.spec_from_file_location("remeasure_ocs_floors", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _plant_tree(root: Path) -> Path:
    java = root / "src" / "main" / "java" / "com" / "ex"
    java.mkdir(parents=True)
    (java / "Api.java").write_text(
        "\n".join(
            [
                "package com.ex;",
                "@RestController",
                '@RequestMapping("/api")',
                "class Api {",
                '  @GetMapping("/x") String x() { return ""; }',
                '  @PostMapping("/y") String y() { return ""; }',
                # Method-level RequestMapping must NOT inflate path_prefix.
                '  @RequestMapping("/z") String z() { return ""; }',
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (java / "Repo.java").write_text(
        "\n".join(
            [
                "package com.ex;",
                "interface BookBasedRepository {}",
                "interface TopicRepository extends BookBasedRepository {}",
                "interface Other extends JpaRepository<String, Long> {}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return root

def test_remeasure_dry_run_proposal(tmp_path: Path) -> None:
    mod = _load_remeasure()
    checkout = _plant_tree(tmp_path / "tree")
    expectations = tmp_path / "expectations.json"
    expectations.write_text(
        json.dumps(
            {
                "repo": "ocs-api-service",
                "minimums": {
                    "ApiSurface": {
                        "api_surface__controller": 1,
                        "api_surface__endpoint": 1,
                        "api_surface__path_prefix": 1,
                    },
                    "Persistence": {"persistence__repository_marker": 1},
                },
            }
        ),
        encoding="utf-8",
    )
    rc = mod.main(
        [
            "--checkout",
            str(checkout),
            "--expectations",
            str(expectations),
            "--rules",
            str(REPO / "spring-signals/harness/astgrep_ocs_floors.yml"),
        ]
    )
    assert rc == 0
    data = json.loads(expectations.read_text(encoding="utf-8"))
    # dry-run must not mutate
    assert data["minimums"]["ApiSurface"]["api_surface__endpoint"] == 1

def test_remeasure_write_updates_floors(tmp_path: Path, capsys) -> None:
    mod = _load_remeasure()
    checkout = _plant_tree(tmp_path / "tree")
    expectations = tmp_path / "expectations.json"
    expectations.write_text(
        json.dumps(
            {
                "repo": "ocs-api-service",
                "minimums": {
                    "ApiSurface": {
                        "api_surface__controller": 0,
                        "api_surface__endpoint": 0,
                        "api_surface__path_prefix": 0,
                        "_note": "keep",
                    },
                    "Persistence": {
                        "persistence__repository_marker": 0,
                        "_note": "keep",
                    },
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    rc = mod.main(
        [
            "--checkout",
            str(checkout),
            "--expectations",
            str(expectations),
            "--rules",
            str(REPO / "spring-signals/harness/astgrep_ocs_floors.yml"),
            "--write",
        ]
    )
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["write_applied"] is True
    data = json.loads(expectations.read_text(encoding="utf-8"))
    assert data["minimums"]["ApiSurface"]["api_surface__controller"] == 1
    assert data["minimums"]["ApiSurface"]["api_surface__endpoint"] == 2
    assert data["minimums"]["ApiSurface"]["api_surface__path_prefix"] == 1
    assert data["minimums"]["Persistence"]["persistence__repository_marker"] == 1
    assert data["minimums"]["ApiSurface"]["_note"] == "keep"
    # Post-write proposal must show aligned minima (no stale pre-write delta).
    assert out["floors"][2]["rule_id"] == "api_surface__path_prefix"
    assert out["floors"][2]["minimum"] == 1
    assert out["floors"][2]["delta"] == 0

def test_remeasure_missing_checkout_exits_2() -> None:
    mod = _load_remeasure()
    rc = mod.main(["--checkout", "/no/such/ocs/checkout"])
    assert rc == 2

def test_resolve_astgrep_finds_binary() -> None:
    mod = _load_remeasure()
    path = Path(mod._resolve_astgrep())
    assert path.is_file()
    assert "ast-grep" in path.name.lower()
