"""Shared helpers for semantic (anti-tautological) adversarial-review hooks."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("XDG_RUNTIME_DIR") or "/tmp") / "cursor-semantic-review"

SKILL = ".cursor/skills/semantic-adversarial-review/SKILL.md"
PREDICATE = (
    "ports/verified-architecture/.cursor/skills/predicate-prose/SKILL.md"
)

# User is asking for a design/adversarial review — not every PR “code review”.
REVIEW_PROMPT_RE = re.compile(
    r"(?is)"
    r"("
    r"\badversarial\s+review\b"
    r"|\bprincipal\b.{0,40}\breview\b"
    r"|\breview\b.{0,80}\b(implement-ready|freeze|dor|adr|architecture|ddl|icd)\b"
    r"|\b(support|refute|nuance)\b.{0,40}\b(claim|hypothesis|approach)\b"
    r"|\bif\s+it\s+is\s+raining\b"
    r"|\btautolog"
    r")"
)

VERDICT_STAMP_RE = re.compile(
    r"(?m)^\s*(\*\*)?(Support|Refuse|Refute|Nuance|Partial support|Embody|Adopt)"
    r"(\*\*)?\s*([.—:\-]|$)"
)
SCOREBOARD_ROW_RE = re.compile(
    r"(?im)^\s*\|[^|\n]{0,80}\|\s*"
    r"(Support|Refuse|Refute|Nuance|Partial\s+support|Embody|Adopt|Keep)\b"
)
IF_THEN_RE = re.compile(r"(?is)\bif\b.{8,240}?\bthen\b")

INJECT_CONTEXT = (
    "Semantic review mandate (hooks): lead with if→then entailments, not "
    "Support/Refuse/Nuance scoreboard stamps that restate the claim. "
    f"Read `{SKILL}` before drafting the review. Spec prose skill (adjacent): "
    f"`{PREDICATE}`. Fail-mode: “it is raining; it is wet” — verdict columns "
    "without a predicate the destination did not already contain."
)

FOLLOWUP = (
    "Semantic-review hook: the last review looked tautological (verdict stamps "
    "/ Support–Refuse tables without enough if→then entailments). Rewrite once: "
    "keep only claims that survive deleting the subject noun from the predicate; "
    f"prefer if P then Q. Skill: `{SKILL}`."
)


def state_path() -> Path:
    key = hashlib.sha256(str(REPO_ROOT.resolve()).encode()).hexdigest()[:16]
    return STATE_DIR / f"review-{key}.json"


def load_state() -> Dict[str, Any]:
    path = state_path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def save_state(data: Dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path().write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def clear_state() -> None:
    path = state_path()
    if path.is_file():
        path.unlink()


def prompt_is_review(prompt: str) -> bool:
    return bool(REVIEW_PROMPT_RE.search(prompt or ""))


def scan_review_text(text: str) -> Tuple[bool, List[str]]:
    """Return (is_tautological, reasons). Fail-open on empty."""
    if not text or len(text.strip()) < 200:
        return False, []
    stamps = VERDICT_STAMP_RE.findall(text)
    rows = SCOREBOARD_ROW_RE.findall(text)
    conditionals = IF_THEN_RE.findall(text)
    stamp_n = len(stamps) + len(rows)
    if_n = len(conditionals)
    reasons: List[str] = []
    # Scoreboard without entailment density.
    if stamp_n >= 4 and if_n * 2 < stamp_n:
        reasons.append(
            f"verdict_stamps={stamp_n} if_then={if_n} (need if→then ≥ stamps/2)"
        )
    # Classic parallel stamp paragraphs.
    if len(stamps) >= 3 and if_n == 0:
        reasons.append("≥3 Support/Refuse stamps and zero if→then sentences")
    return bool(reasons), reasons


def mark_review_active(prompt_excerpt: str) -> None:
    save_state(
        {
            "active": True,
            "prompt_excerpt": (prompt_excerpt or "")[:240],
            "finding": None,
        }
    )


def record_finding(reasons: List[str]) -> None:
    state = load_state()
    if not state.get("active"):
        return
    state["finding"] = {"reasons": reasons}
    save_state(state)


def clear_finding() -> None:
    state = load_state()
    if not state:
        return
    state["finding"] = None
    save_state(state)
