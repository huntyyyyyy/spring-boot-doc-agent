---
name: principal-se-research-epic
description: >-
  Principal-SE research → synthesis → epic → implement. Requires paper digests
  (type keys, sections, references walk), GitHub anti-bogus adopters (≥5 exact or
  honest Pilot), arXiv+GitHub+DeepWiki+llms.txt, claim tiers, Bloom through Create
  before Implement. Use for design-shaped work, Spec-driven delivery, framework
  adoption, Must-spine claims, or “same bar as the quality synthesis.”
---

# Principal SE research → epic → implement

Follow whenever work is **design-shaped** (new System of Record, gates, measure
modes, architecture, framework/tool adoption, Must-spine science) or the user
asks for principal rigor. Always-on **se-quality-constitution** still applies
during implementation. Agent-requested **principal-research-gate** mandates this
skill; for cross-domain analogy also follow **cross-domain-isomorphism** (I1–I5).

## Sources of Truth (read first)

- `docs/research/README.md` — forced-entry domain map
- `docs/research/method/paper-digest-framework.md` — **paper type + sections + refs**
- `docs/research/se-quality-synthesis-2026-08-08.md` — Embody/Adopt/Refuse decisions
- `docs/research/quality-backlog.md` — Active tip + Draft Specs
- Epic pattern: `docs/reviews/9bc7851_PR_94.md` §6
- Skills: **paper-digest** (mandatory in Phase A), **cross-domain-isomorphism** when analogy is in play

## Hard gate — Bloom through Create before Implement

Future-dev plans (Spec Draft, epic tickets, “Spike → wire into pre_pr”, framework
adoption) **must** record Bloom **1→6** with deterministic primary evidence.
Chat-only “I read the docs/papers” is **not** evidence.

| Level | Name | Deterministic evidence (required) |
| --- | --- | --- |
| **1** | Remember | Tool/API/rule/paper IDs; Atom metadata; `llms.txt` / primary docs / DeepWiki topic |
| **2** | Understand | **Paper digests** with type key + **section map** (not abstract-only); restate in *this* product’s types |
| **3** | Apply | How it runs here (CLI, config, venv, suite) **or** Spike charter if no public code |
| **4** | Analyze | Alternatives; Embody/Adopt/Refuse; **exact vs adjacent** GitHub; I3 non-preserved structure |
| **5** | Evaluate | Adversarial checklist; false-green / false-red; research-depth FAIL if digests/adopters missing |
| **6** | Create | Spec/epic tickets with Acceptance; seams ≤225 LOC; **then** Implement |

```yaml
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
  - paper_digest
```

## Phase A — Research (before Spec Create)

### A0 — Frame entities

1. Name the **entities** (algorithm classes / ports / predicates), not slogans.
2. List alternatives; refuse category errors.
3. Claim tiers: **Evidenced** / **Confirmed** / **Unknown**.

### A1 — Paper digests (mandatory)

For each load-bearing paper, run skill **paper-digest**:

1. arXiv Atom for metadata (**categories ≠ paper type**).
2. HTML/PDF **section map**: abstract, methods/model, results, analysis, conclusions, references.
3. Assign closed **primary_type** (`theoretical`, `formal-systems`, `empirical`,
   `benchmark`, `systems-artifact`, `methodological`, `analytic`,
   `literature-survey`, `systematic-review`, `position`) — `[Inferred]` unless
   self-labeled.
4. Answer the type-specific checklist in `docs/research/method/paper-digest-framework.md`.
5. Write `docs/research/papers/digests/<id>-<slug>.md` (or port mirror).

**Refuse** promoting Must / Adopt from abstract-only or title→todo mapping.

### A2 — Related-paper walk

From each digest’s References / Related Work: up to five **algorithmic kin**;
digest at least one follow-on or record “no kin.” Prefer cited works over
similar-title search. External citation graphs optional (note rate-limits).

### A3 — GitHub algorithm adopters (anti-bogus)

Per entity, target **≥5 genuine repositories that implement the algorithm**:

| Pass | Fail |
| --- | --- |
| Canonical org / dependents; recent maintenance; tests/Actions; **algorithm fit** | Scrapers, 0-star stubs, homonyms, anonymous 0-CI dumps, unreleased org profiles |

Separate **exact** vs **adjacent**. Adjacent ≥5 does **not** unlock “Must Adopt”
for an exact algorithm with zero public implementations — write **Pilot / invent**
with Spike exit criteria instead.

For public frameworks: primary docs + `llms.txt` + DeepWiki page + DeepWiki MCP
`ask_question` (`https://mcp.deepwiki.com/mcp`). DeepWiki alone ≠ boolean SoT.

### A4 — Embody / Adopt / Refuse

Map to *this* product. Exact adopter tables required for Adopt. Constraints from
undecidability proofs may be **Embody** without shipping the full checker.

### A5 — Write location

Parent repo: `docs/research/<domain>/`. Not `claude/`. Port/greenfield trees use
their `research/` mirror but the **same method**.

## DeepWiki + llms.txt (frameworks)

| Is | Is not |
| --- | --- |
| Sensor for Bloom 1–5 on public repos | Merge System of Record / Cover% proof |
| Grounded Ask on indexed repos | Substitute for paper digests or Spec Approve |

Wire: Streamable HTTP `https://mcp.deepwiki.com/mcp` → `ask_question` with
`repoName`, `question`. Keep Ask search URLs in memo `sources:`.

## Phase B — Synthesis + review packet

1. One principal memo + quality-backlog Draft Spec row.
2. One-page verdict + adversarial checklist (Bloom Evaluate).
3. Explicit research-depth status: PASS only if A1–A3 met or waived with eyes open.
4. No Implement until Spec gate + Bloom Create tickets exist.

## Phase C — Jira-style epic = Bloom Create

| Field | Required |
| --- | --- |
| Epic goal | One sentence |
| Tickets | ID, title, **Acceptance** |
| Spikes | Question + exit (mandatory when exact adopters = 0) |
| Exit | When epic is done |
| Invariants | Constitution gates |
| Bloom | Ladder evidence + digest paths + Ask URLs |

Order: Spec gate epic → impl epic → process/docs → optional spikes. One tip writer.

## Phase D — Implement

Only after Spec Approve **and** Bloom 1–6:

1. Size preflight; cohesive ≤225 LOC splits first if needed.
2. Open/closed strategies; no grab-bag utils; descriptive names.
3. Verify deterministic gates (ruff, size, complexipy, claims, coverage oracle on 3.11).
4. Session-log only if steering/research assumptions moved.

## Explicit refuse

- Abstract-only or title-skim as “research complete”
- Treating arXiv subject categories as paper-type keys
- Adjacent GitHub repos as proof of exact-algorithm Adopt
- Zenodo study zips / “code coming soon” org profiles as shipped dependencies
- Scoped Cover% or LLM-judge as 98.7 proof · fuzzy green · Implement from chat
  memory without Bloom/MCP/digest evidence · DeepWiki Ask without citation

## Bootstrap blurb

```text
Follow skill principal-se-research-epic + paper-digest + se-quality-constitution.
Phase A: entities → paper digests (type+sections+refs) → related walk →
GitHub anti-bogus (≥5 exact or Pilot Spike) → Embody/Adopt/Refuse.
Bloom 1–6 via digests + llms.txt + DeepWiki ask_question before Implement.
SoT: docs/research/method/paper-digest-framework.md + quality-backlog Active tip.
```
