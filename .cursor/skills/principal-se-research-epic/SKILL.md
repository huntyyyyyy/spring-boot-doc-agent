---
name: principal-se-research-epic
description: >-
  Runs principal-SE research (arXiv/GitHub/DeepWiki MCP + llms.txt, claim tiers),
  Bloom's taxonomy through Create before Implement, synthesis, adversarial review,
  and Jira-style epics. Use for design-shaped work, Spec-driven delivery, framework
  adoption, or “same bar as the quality synthesis / E-CM” — and while implementing
  those features afterward.
---

# Principal SE research → epic → implement

Follow this skill whenever work is **design-shaped** (new SoT, gates, measure modes,
architecture, framework/tool adoption) or the user asks for principal rigor. The
always-on rule **se-quality-constitution** still applies during implementation. For
cross-domain analogy, also follow **cross-domain-isomorphism** (I1–I5).

## SoTs (read first)

- `docs/research/README.md` — **forced entry** domain map (look-first hooks)
- `docs/research/se-quality-synthesis-2026-08-08.md` — decisions 1–31, Embody/Adopt/Refuse
- `docs/research/quality-backlog.md` — ordered backlog (Active tip + Draft Specs)
- `docs/design/coverage-measure-modes-design-2026-08-08.md` — dual-mode design
- Epic pattern mirror: `docs/reviews/9bc7851_PR_94.md` §6 (Epic / Spike / Ticket + Acceptance)
- Lint/import gap example (DeepWiki Ask): `docs/research/process/46-lint-import-resolution-ruff-vs-ty-2026-08-10.md`

## Hard gate — Bloom through Create before Implement

Any markdown that is a **future-dev plan** (Spec Draft, epic ticket list, design stub
with Implement tickets, “Spike → wire into pre_pr”, framework adoption) **must**
record a **Bloom ladder** fulfilled with **deterministic MCP/primary evidence** before
Phase D code generation. Goal: contextual, elegant implementation in *this* repo —
not vibes or skimmed READMEs.

| Level | Name | Deterministic evidence (required) |
| --- | --- | --- |
| **1** | Remember | Name tool/API/rule IDs; cite primary `llms.txt` / rule page / DeepWiki topic |
| **2** | Understand | Restate problem classes in *this* product’s types (SoT vs sensor, L1–Ln, ports) |
| **3** | Apply | Show how the tool would run here (CLI, config path, venv, `pre_pr` suite shape) |
| **4** | Analyze | Contrast alternatives; map Embody/Adopt/Refuse; note non-preserved structure (I3) |
| **5** | Evaluate | Adversarial checklist; FP budget; what would false-green / false-red tip |
| **6** | Create | Spec/epic tickets with Acceptance; proposed module seams ≤225 LOC; **then** Implement |

**Refuse to Implement** (no PR code for the planned feature) if levels **1–6** are not
in the research/design memo (or linked companion) with claim tags. Chat-only “I read
the docs” is **not** evidence.

Frontmatter hint for future-dev memos:

```yaml
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
```

## DeepWiki + llms.txt + MCP (do not lose across chats)

DeepWiki is **not browse-only**. Prefer this stack for public GitHub frameworks:

### 1. LLM doc index (`llms.txt`)

- Astral example: `https://docs.astral.sh/ruff/llms.txt`, `https://docs.astral.sh/ty/llms.txt`
- Fetch linked `index.md` paths for clean markdown (sites document this in `llms.txt`)
- Tier: **Evidenced** when quoting primary docs

### 2. DeepWiki pages (cartography)

- URL: `https://deepwiki.com/<owner>/<repo>` (swap `github.com` → `deepwiki.com`)
- Use for architecture maps, crate/module layout, “where does X live”
- Tier: **Evidenced — DeepWiki** (cartography); still verify merge-critical claims on primary docs

### 3. DeepWiki Ask (Q&A) — official MCP

Remote MCP (public repos, **no auth**):

| Item | Value |
| --- | --- |
| Base | `https://mcp.deepwiki.com/` |
| Preferred wire | Streamable HTTP `https://mcp.deepwiki.com/mcp` |
| Legacy | SSE `https://mcp.deepwiki.com/sse` (deprecated) |
| Tools | `read_wiki_structure`, `read_wiki_contents`, **`ask_question`** |

**`ask_question` args:** `repoName` (string or list ≤10 of `owner/repo`), `question` (string).

Minimal call shape (JSON-RPC over Streamable HTTP; `Accept: application/json, text/event-stream`):

1. `initialize` → optional `notifications/initialized`
2. `tools/call` with `name: ask_question`, `arguments: { repoName, question }`
3. Read SSE `data:` JSON; answer is in `result.content[].text`
4. Keep the DeepWiki search URL from the answer body in the memo `sources:`

Cursor client config (if wiring MCP into the IDE):

```json
{
  "mcpServers": {
    "deepwiki": {
      "url": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

If DeepWiki MCP is **not** in the session’s MCP catalog, agents **must** still call it
via HTTP as above (or equivalent) before Implement — do not skip Ask because the tool
isn’t pre-registered.

Docs: <https://docs.devin.ai/work-with-devin/deepwiki-mcp> · Devin `llms.txt` index:
<https://docs.devin.ai/llms.txt>

### 4. What DeepWiki is / is not

| Is | Is not |
| --- | --- |
| Sensor for framework understanding + Bloom 1–5 | Merge SoT / Cover% proof |
| Grounded Q&A on indexed public repos | Substitute for in-repo Spec Approve |
| Complement to arXiv + GitHub primary | Excuse to skip Confirmed checkout probes |

## Phase A — Research (before code)

1. Frame the question; list alternatives; refuse category errors (e.g. PIT ≠ gate mutators).
2. Gather evidence with tiers: **Evidenced** (primary) / **Confirmed** (this repo) / **Unknown**.
3. Prefer **arXiv + GitHub primary docs + `llms.txt` + DeepWiki (page + `ask_question`)** .
   Mark missing IDs Unknown. DeepWiki alone is insufficient for boolean SoT changes.
4. Climb Bloom **1→5** in the memo (tables + Ask links). Leave **6 Create** for Spec/epic.
5. Map findings to **Embody / Adopt / Refuse** for *this* Python CLI product.
6. Write under `docs/research/<domain>/` (see `docs/research/README.md`); not `claude/`.
   Keep modules/docs cohesive (LOC/cohesion culture applies to new code later).

## Phase B — Synthesis + review packet

1. Merge segments into one principal memo + short quality backlog row (Draft Spec).
2. Produce a **one-page verdict** + adversarial findings checklist (Bloom **Evaluate**).
3. Lock open product choices (example: coverage climb artifact **16-A**).
4. Do **not** implement until Spec gate is recorded in-repo **and** Bloom **Create**
   tickets/Acceptance exist.

## Phase C — Jira-style epic (fresh-chat ready) = Bloom Create

Use IDs like `E-CM0` / `CM0-1`:

| Field | Required |
| --- | --- |
| Epic goal | One sentence |
| Tickets | ID, title, **Acceptance** |
| Spikes | Question + exit criterion |
| Exit | When epic is done |
| Invariants | Link constitution gates |
| Bloom | Pointer to ladder evidence + MCP Ask URLs |

Order: **Spec gate epic → impl epic → process/docs → optional spikes**. One tip writer.

## Phase D — Implement (same bar)

Only after Spec Approve **and** Bloom **1–6** recorded:

1. Spec approved in design memo / CONTRIBUTING / research frontmatter.
2. Size preflight; if LOC ratchet fails, cohesive ≤225 splits **first**.
3. OCP strategies/ports; no if/elif gods; no utils bag; descriptive names.
4. Verify: deterministic gates (ruff, size, complexipy, claims, cov oracle on 3.11).
5. Archive: session-log only if steering/research assumptions moved.

## Explicit refuse (do not schedule)

Scoped Cover% or LLM-judge as 98.7 proof · fuzzy/PID green · cross-worktree combine ·
cov on every Python · mesh/ECS/Backstage/WASM-by-default · Spec Kit WorkflowEngine as
mandatory runtime · parallel SoT tip thrash / force-push recovery theater · Implement
from chat memory without Bloom/MCP evidence · replace DeepWiki Ask with uncited summary

## Bootstrap blurb (paste if needed)

```text
Follow skill principal-se-research-epic + rule se-quality-constitution.
SoT: docs/research/se-quality-synthesis-2026-08-08.md + quality-backlog Active tip.
Bloom 1–6 via llms.txt + DeepWiki MCP ask_question before Implement.
Policy 16-A; fail_under 98.7; complexipy ≤5; LOC ≤225; no utils; SDD one-stream.
```
