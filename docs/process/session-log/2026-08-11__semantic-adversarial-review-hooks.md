# Session log — 2026-08-11

## 2026-08-11 — Semantic adversarial-review hooks (if→then, not scoreboards)
Commit: 9f1bec1a
Tests: `pytest tests/ci/test_semantic_review_hooks.py` 6/6; `check_repo_claims.py` OK
Assumptions affected:
- Agent review discipline — "Skill/constitution text alone stops tautological Support/Refuse reviews" — [New info — Cursor hooks now inject + audit + stop follow-up; Skill `semantic-adversarial-review` is the written mandate]
- `predicate-prose` scope — Spec Markdown only — [Still accurate — chat reviews use the new root Skill; cross-link added]
Files touched: `.cursor/hooks.json`, `.cursor/hooks/semantic_review_common.py`, `.cursor/hooks/inject_semantic_review.py`, `.cursor/hooks/audit_semantic_review_response.py`, `.cursor/hooks/stop_semantic_review_rewrite.py`, `.cursor/skills/semantic-adversarial-review/SKILL.md`, `.cursor/rules/semantic-adversarial-review.mdc`, `tests/ci/test_semantic_review_hooks.py`, `ports/verified-architecture/.cursor/skills/predicate-prose/SKILL.md`
