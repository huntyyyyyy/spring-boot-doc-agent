---
name: principal-se-research-epic
description: >-
  Runs principal-SE research (arXiv/GitHub/DeepWiki, claim tiers), synthesis,
  adversarial review packet, and Jira-style epics before implementing design-shaped
  work. Use when the user asks for rigorous research, dual-mode/SoT design,
  epic/handoff planning, Spec-driven delivery, or “same bar as the quality
  synthesis / E-CM” — and while implementing those features afterward.
---

# Principal SE research → epic → implement

Follow this skill whenever work is **design-shaped** (new SoT, gates, measure modes, architecture) or the user asks for principal rigor. The always-on rule **se-quality-constitution** still applies during implementation.

## SoTs (read first)

- `docs/research/README.md` — **forced entry** domain map (look-first hooks)
- `docs/research/se-quality-synthesis-2026-08-08.md` — decisions 1–31, Embody/Adopt/Refuse
- `docs/research/quality-backlog.md` — ordered backlog
- `docs/design/coverage-measure-modes-design-2026-08-08.md` — dual-mode design
- Epic pattern mirror: `docs/reviews/9bc7851_PR_94.md` §6 (Epic / Spike / Ticket + Acceptance)

## Phase A — Research (before code)

1. Frame the question; list alternatives; refuse category errors (e.g. PIT ≠ gate mutators).
2. Gather evidence with tiers: **Evidenced** (primary) / **Confirmed** (this repo) / **Unknown**.
3. Prefer **arXiv + GitHub primary docs + DeepWiki** (cartography only). Mark missing IDs Unknown.
4. Map findings to **Embody / Adopt / Refuse** for *this* Python CLI product.
5. Write under `docs/research/<domain>/` (see `docs/research/README.md`); not `claude/`. Keep modules/docs cohesive.

## Phase B — Synthesis + review packet

1. Merge segments into one principal memo + short quality backlog.
2. Produce a **one-page verdict** + adversarial findings checklist.
3. Lock open product choices (example: coverage climb artifact **16-A** → distinct `coverage.climb.xml`).
4. Do **not** implement until Spec gate is recorded in-repo.

## Phase C — Jira-style epic (fresh-chat ready)

Use IDs like `E-CM0` / `CM0-1`:

| Field | Required |
| --- | --- |
| Epic goal | One sentence |
| Tickets | ID, title, est, **Acceptance** |
| Spikes | Question + exit criterion |
| Exit | When epic is done |
| Invariants | Link constitution gates |

Order: **Spec gate epic → impl epic → process/docs → optional spikes**. One tip writer.

## Phase D — Implement (same bar)

1. Spec approved in design memo / CONTRIBUTING.
2. Size preflight; if LOC ratchet fails, cohesive ≤225 splits **first**.
3. OCP strategies/ports; no if/elif gods; no utils bag; descriptive names.
4. Verify: deterministic gates (ruff, size, complexipy, claims, cov oracle on 3.11).
5. Archive: CONTRIBUTING / session-log only if steering claims moved.

## Explicit refuse (do not schedule)

Scoped Cover% or LLM-judge as 98.7 proof · fuzzy/PID green · cross-worktree combine · cov on every Python · mesh/ECS/Backstage/WASM-by-default · Spec Kit WorkflowEngine as mandatory runtime · parallel SoT tip thrash / force-push recovery theater

## Bootstrap blurb (paste if needed)

```text
Follow skill principal-se-research-epic + rule se-quality-constitution.
SoT: docs/research/se-quality-synthesis-2026-08-08.md
Start at Spec gate; policy 16-A; fail_under 98.7; complexipy ≤5; LOC ≤225;
no utils; SDD one-stream. Do not skip research when changing SoT/gates.
```
