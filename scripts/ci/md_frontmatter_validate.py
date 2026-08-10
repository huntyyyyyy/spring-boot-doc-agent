#!/usr/bin/env python3
"""Validate / normalize one markdown frontmatter document (E-MD0)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml
from md_frontmatter_kinds import (
    DEPRECATED_KEYS,
    SOURCE_NEST_KEYS,
    allowed_keys,
    classify,
    required_keys,
    unknown_keys_hard,
)

_FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


@dataclass
class Finding:
    path: str
    level: str  # hard | soft
    message: str


@dataclass
class DocResult:
    kind: str
    skipped: bool
    data: Dict[str, Any] = field(default_factory=dict)
    findings: List[Finding] = field(default_factory=list)
    fixed_text: Optional[str] = None


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    match = _FM_RE.match(text)
    if not match:
        return None, text
    return match.group(1), text[match.end() :]


def load_frontmatter(text: str) -> Tuple[Dict[str, Any], Optional[str]]:
    """Return (data, parse_error). parse_error set when YAML is invalid."""
    raw, _ = split_frontmatter(text)
    if raw is None:
        return {}, None
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        return {}, str(exc).splitlines()[0]
    if not isinstance(loaded, dict):
        return {}, "frontmatter root must be a mapping"
    return loaded, None


def apply_deprecated_aliases(data: Mapping[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in data.items():
        canon = DEPRECATED_KEYS.get(str(key), str(key))
        if canon in out and str(key) in DEPRECATED_KEYS:
            continue
        out[canon] = value
    return out


def rewrite_deprecated_in_text(text: str) -> str:
    raw, body = split_frontmatter(text)
    if raw is None:
        return text
    lines = []
    for line in raw.splitlines():
        replaced = line
        for old, new in DEPRECATED_KEYS.items():
            if replaced.startswith(f"{old}:"):
                replaced = f"{new}:" + replaced[len(old) + 1 :]
                break
        lines.append(replaced)
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def _related_ok(repo: Path, item: Any) -> bool:
    if isinstance(item, dict):
        item = item.get("path") or item.get("href") or ""
    if not isinstance(item, str) or not item.strip():
        return False
    value = item.strip()
    if value.startswith(("http://", "https://", "external:")):
        return True
    return (repo / value).exists()


def validate_doc(repo: Path, path: Path, *, fix: bool = False) -> DocResult:
    rel = path.resolve().relative_to(repo.resolve()).as_posix()
    kind, skip = classify(repo, path)
    if skip:
        return DocResult(kind=kind, skipped=True)
    text = path.read_text(encoding="utf-8")
    raw_fm, _ = split_frontmatter(text)
    if raw_fm is None:
        if kind in {"research_memo", "design_epic", "ddia_page"}:
            return DocResult(
                kind=kind,
                skipped=False,
                findings=[Finding(rel, "hard", "missing YAML frontmatter")],
            )
        return DocResult(kind=kind, skipped=False)

    loaded, parse_err = load_frontmatter(text)
    findings: List[Finding] = []
    if parse_err:
        level = "soft" if kind in {"steering", "skill_agent"} else "hard"
        return DocResult(
            kind=kind,
            skipped=False,
            findings=[Finding(rel, level, f"YAML parse error: {parse_err}")],
        )
    data = apply_deprecated_aliases(loaded)
    fixed = rewrite_deprecated_in_text(text) if fix else None

    for old in DEPRECATED_KEYS:
        if re.search(rf"^{re.escape(old)}\s*:", text, re.M):
            findings.append(
                Finding(rel, "hard", f"deprecated key {old!r} — use {DEPRECATED_KEYS[old]!r}")
            )

    req = required_keys(kind)
    for key in sorted(req):
        value = data.get(key)
        if key == "related":
            if not isinstance(value, list):
                findings.append(Finding(rel, "hard", f"missing required key {key!r}"))
            continue
        if value in (None, "", []):
            findings.append(Finding(rel, "hard", f"missing required key {key!r}"))

    allow = allowed_keys(kind)
    if unknown_keys_hard(kind) and allow:
        for key in sorted(data):
            if key not in allow:
                findings.append(Finding(rel, "hard", f"unknown key {key!r}"))

    if "related" in data and kind in {"research_memo", "design_epic"}:
        related = data["related"]
        if not isinstance(related, list):
            findings.append(Finding(rel, "hard", "related must be a list"))
        else:
            for item in related:
                if not _related_ok(repo, item):
                    findings.append(Finding(rel, "hard", f"related path missing: {item!r}"))

    if kind in {"steering", "skill_agent"}:
        # Soft-only kinds: claims/DDIA own hard SoT elsewhere.
        findings = [
            Finding(f.path, "soft", f.message) if f.level == "hard" else f for f in findings
        ]
        return DocResult(kind=kind, skipped=False, data=data, findings=findings, fixed_text=fixed)

    if data.get("bloom_gate") == "required-through-create":
        mcp = data.get("bloom_mcp")
        if not isinstance(mcp, list) or not mcp:
            findings.append(Finding(rel, "hard", "bloom_gate requires bloom_mcp list"))
        sources = data.get("sources")
        if not isinstance(sources, dict) or not (SOURCE_NEST_KEYS & set(sources)):
            findings.append(
                Finding(rel, "hard", "bloom_gate requires sources with known nest keys")
            )

    freshness = data.get("freshness")
    if freshness == "tip-bound":
        findings.append(
            Finding(rel, "soft", "tip-bound freshness — confirm last_reviewed still current")
        )

    return DocResult(kind=kind, skipped=False, data=data, findings=findings, fixed_text=fixed)
