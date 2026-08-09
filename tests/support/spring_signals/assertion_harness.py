"""Cohesive suite from tests/spring_signals/test_check_assertions.py: write_csv, row, write_spec, base_spec, run."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ENGINE_PATH = REPO_ROOT / "spring-signals" / "harness" / "check-assertions.py"
HARNESS_DIR = ENGINE_PATH.parent
spec = importlib.util.spec_from_file_location("check_assertions", ENGINE_PATH)
ca = importlib.util.module_from_spec(spec)
sys.modules["check_assertions"] = ca  # dataclasses/typing resolve __module__ via sys.modules
assert spec.loader is not None
spec.loader.exec_module(ca)

HEADER = (
    "file,start_line,end_line,source_set,schema_version,"
    "rule_id,framework,generation,symbol,signal,detail\n"
)


def write_csv(out_dir: Path, query: str, rows: list[str]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{query}.csv"
    path.write_text(HEADER + "".join(rows), encoding="utf-8")
    return path


def row(rule_id: str, signal: str, symbol: str = "com.example/Foo#bar.") -> str:
    return f"src/Foo.java,1,1,main,v1,{rule_id},spring,,{symbol},{signal},x\n"


def write_spec(path: Path, spec_obj: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec_obj, indent=2) + "\n", encoding="utf-8")
    return path


def base_spec(**sections) -> dict:
    return {"repo": "test", "asserted": {}, "minimums": {}, "snapshot": {}, **sections}


def run(spec_path: Path, out_dir: Path, *extra: str) -> int:
    return ca.main(["--out", str(out_dir), "--expectations", str(spec_path), *extra])
