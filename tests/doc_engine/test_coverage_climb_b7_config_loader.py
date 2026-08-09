"""Coverage climb B7: config loader symlink / yaml-missing / non-dict.

Q2 adequacy witness: mutmut_slice on doc_engine.config.loader — asserts bite
outside-root continue, PyYAML ImportError, and non-dict config return None.
"""

from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

from doc_engine.config import loader as loader_mod

pytestmark = pytest.mark.domain_climb_sensor


def test_find_repo_config_skips_outside_root(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    cfg = tmp_path / ".doc-engine.json"
    cfg.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(loader_mod, "is_path_inside_root", lambda *_a, **_k: False)
    assert loader_mod.find_repo_config(str(tmp_path)) is None


def test_load_yaml_import_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / ".doc-engine.yml"
    path.write_text("scanners: []\n", encoding="utf-8")
    real_import = builtins.__import__

    def fake_import(name: str, *a: object, **k: object):
        if name == "yaml":
            raise ImportError("no yaml")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(RuntimeError, match="PyYAML"):
        loader_mod._load_yaml(path)


def test_load_repo_config_non_dict_json(tmp_path: Path) -> None:
    cfg = tmp_path / ".doc-engine.json"
    cfg.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
    assert loader_mod.load_repo_config(str(tmp_path)) is None
