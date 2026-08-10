---
title: E-MDC0 — Cursor MDC rules DevEx (activation algebra, not MD rename)
status: RESEARCH COMPLETE — Spec Approve (Implement on tip #119 docs/.cursor only)
date: 2026-08-10
epic: E-MDC0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/research/process/26-agent-context-markdown-bloat-2026.md
  - docs/research/process/28-agent-context-algorithm-first-2026.md
  - .cursor/skills/principal-se-research-epic/SKILL.md
  - .cursor/skills/cross-domain-isomorphism/SKILL.md
  - AGENTS.md
  - DOMAIN_MAP.md
sources:
  llms_txt:
    - https://cursor.com/llms.txt
  primary_docs:
    - https://cursor.com/docs/context/rules
    - https://cursor.com/docs/skills.md
    - https://cursor.com/docs/hooks.md
  deepwiki_ask:
    - https://deepwiki.com/search/how-do-cursor-project-rules-ac_b0a5e245-2e70-4548-81cc-92b94349dba3
  mcp: https://mcp.deepwiki.com/mcp (ask_question)
---

# Principal memo: optimize MDC DevEx (conditional activation)

**Product:** agent-context stack for `doc-engine` (Cursor Project Rules + Cloud
`AGENTS.md` ingest + skills + hooks).  
**Question.** How do we stop treating “files exist under `.cursor/rules`” as done,
and actually use MDC activation modes so agents are both **correct** and
**token-efficient**?

**Method.** Cursor primary docs (`llms.txt` → rules/skills) + DeepWiki MCP
`ask_question` (cartography; verify on primary) → Embody/Adopt/Refuse → inventory
kill list → Spec Create → Implement rule pack on tip #119 (docs + `.cursor` only).

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is mass `.md` → `.mdc` the fix? | **No** — category error. Research/human SoT stays Markdown. |
| Root failure today | **3/3** project rules `alwaysApply: true`; **zero** globs / intelligent / manual `[Confirmed]` |
| Activation SoT for path scope | **MDC `globs` only** — nested `AGENTS.md` path-scoping **Refuse** beside globs |
| Always-on budget | **≤2**: slim constitution + Task model pin |
| Depth procedures | Stay in **Skills** (progressive disclosure); rules = mandate + `@` skill |
| Hard deny vs soft rule | Keep **hooks** for deny; do not replace with prose rules |
| Spec status | **Approve** via user Implement instruction (2026-08-10) — rebuild rules now |

**Bottom line:** MDC wins when **mode redistribution** is the product. Paste-policy
everywhere is the anti-pattern this epic reverses.

---

## 0b. Bloom ladder (required before MDC Implement)

| Level | Evidence in this memo |
| --- | --- |
| **1 Remember** | Modes: Always / Intelligently / Specific Files / Manual; fields `alwaysApply`, `description`, `globs`; Skills progressive load; `@` file refs |
| **2 Understand** | Problem classes C1–C6 mapped to this repo’s ingest surfaces |
| **3 Apply** | Concrete `.cursor/rules/*.mdc` pack + glob paths that exist here |
| **4 Analyze** | Peer structure Adopt table; legacy decisions reversed |
| **5 Evaluate** | Adversarial §7; false-green (alwaysApply bloat) vs false-red (missing invariants) |
| **6 Create** | Tickets MDC0–MDC4 + inventory matrix — **Implement proceeds on tip** |

DeepWiki Ask on `getcursor/docs` returned **no Project Rules coverage** (stale wiki
vs `cursor.com/docs`) — treated as **cartography miss**; primary docs remain
**Evidenced**. Search URL in frontmatter.

---

## 1. Problem classes (do not collapse)

| Class | Failure | Owner *here* | Action |
| --- | --- | --- | --- |
| **C1 Always-on thrash** | Every chat pays full policy essay | Project Rules `alwaysApply` | Cap ≤2; invariants only |
| **C2 Mode underuse** | `.mdc` without globs/description | Frontmatter algebra | Add ≥4 glob + ≥2 intelligent + ≤1 manual |
| **C3 Dual path-SoT** | Nested AGENTS **and** MDC globs | Path scoping | **Refuse** nested AGENTS; one root thin pointer |
| **C4 Skill paste** | Always-on restates full skill | Rules vs Skills | Demote iso; `@` skill |
| **C5 Ingest clones** | AGENTS/DOMAIN_MAP restate gates | Cloud ingest | Slim to pointers |
| **C6 Soft deny** | Prose instead of hooks | Hooks | Keep hard deny scripts |

---

## 2. Primary evidence (Cursor)

**Evidenced —** [Rules](https://cursor.com/docs/context/rules) via
[llms.txt](https://cursor.com/llms.txt):

| `alwaysApply` | `description` | `globs` | Behavior |
| --- | --- | --- | --- |
| `true` | — | — | Always included |
| `false` | — | provided | Auto-attach when matching file in context |
| `false` | provided | omitted | Agent pulls when relevant |
| `false` | omitted | omitted | Manual `@`-mention only |

Best practices: focused rules, **&lt;500 lines**, **reference files** instead of
copying, add rules when Agent **repeats mistakes**, don’t paste style guides.

**Evidenced —** [Skills](https://cursor.com/docs/skills.md): progressive disclosure;
on-demand depth; `/migrate-to-skills` converts *intelligent* rules (no globs) to
skills — **not** alwaysApply/glob rules. Structure Adopt: keep depth in skills;
keep activation control in MDC.

**Nested AGENTS.md:** Cursor supports subdirectory precedence. **Structure idea
Adopt**; **substrate Refuse** as second path-SoT beside MDC globs in *this* repo
(Cloud already injects root `AGENTS.md`).

---

## 3. Peer structure Adopt / substrate Refuse

| Peer | Structure to steal | Substrate Refuse |
| --- | --- | --- |
| Cursor Project Rules | Activation algebra | — |
| AGENTS.md nested | Directory precedence idea | Dual path-SoT beside MDC globs |
| Cursor Skills | Progressive disclosure | Skills → alwaysApply paste |
| Hooks (existing) | Hard deny vs soft rule | Replacing hooks with prose |
| Nx / Packwerk / tach | Boundary → glob lens mapping | Installing Nx as product |
| Spec Kit / OpenSpec | Spec before Implement | WorkflowEngine runtime |
| llms.txt / DeepWiki Ask | Deterministic framework learning | Chat summary as Spec proof |

---

## 4. Legacy decisions reversed

1. “All project rules alwaysApply” → **false**; redistribute.
2. “Isomorphism must alwaysApply” → **agent-requested** + skill depth.
3. “AGENTS.md can grow as second rule system” → **thin pointer**; path = MDC globs.
4. “Paste policy into every surface” → **one SoT + @**.
5. “MDC = rename markdown” → **category error**.

---

## 5. Inventory matrix (MDC1) — content → mode

| Source chunk | Today | Decision | Destination |
| --- | --- | --- | --- |
| fail_under 98.7 / complexipy / LOC / no utils | constitution always | **Keep** | always constitution |
| SoT vs sensor / 16-A | constitution always | **Keep** | always constitution |
| Spec→Impl tip writer | constitution always | **Keep** | always constitution |
| Bloom / DeepWiki procedure | constitution + AGENTS | **Move** | agent-requested `principal-research-gate` + skill |
| Iso I1–I5 full paste | iso always + skill | **Demote** | agent-requested 5-line + `@` skill |
| Task model pin | always | **Keep** | always `task-subagent-model-grok` |
| pre_pr / hooks / outage | AGENTS essay | **Move** | glob `ci-local-gates` + manual tip-recovery |
| doc_engine nest / façade / cohesion | scattered | **Move** | glob `doc-engine-cohesion` |
| ast-grep / fixtures / rule coverage | CLAUDE (Claude SoT) | **Lens** | glob `stage0-citation` (Cursor path attach) |
| Spec Draft discipline | constitution / README | **Move** | glob `research-spec-drafts` |
| Session-log append / pack | CLAUDE + nest README | **Lens** | glob `session-log-nest` (shards stay `.md`) |
| Cloud env / venv / cert gotchas | AGENTS | **Keep slim** | root AGENTS ≤~40 lines |
| BC map / truth classes | DOMAIN_MAP | **Keep human** | DOMAIN_MAP; drop tip-clone policy; point backlog |
| CLAUDE.md steering / claims | Claude SoT | **Unchanged** | not Cursor MDC |
| Skills full procedures | skills | **Keep** | on-demand skills |

**Spec Approve:** architecture + this matrix — **Approved** for Implement by user
instruction to execute E-MDC0 plan (chat, 2026-08-10). Active tip remains land
#119 → E-COH1; this epic is docs + `.cursor/rules` only.

---

## 6. Create — epic tickets

| ID | Acceptance |
| --- | --- |
| **MDC0** | Memo 47 + Bloom 1–6 + backlog Draft row |
| **MDC1** | Inventory matrix complete (this §5) |
| **MDC2** | ≤2 alwaysApply; ≥4 glob; ≥2 agent-requested; ≤1 manual; no rule &gt;150 lines |
| **MDC3** | AGENTS thin pointer (no fail_under essay); DOMAIN_MAP no agent-policy clones; path SoT = MDC globs |
| **MDC4** | Frontmatter smoke checklist; `check_repo_claims` if scripts/skills touched; tip #119 |

### Concrete rule pack (Implement)

| File | Mode |
| --- | --- |
| `se-quality-constitution.mdc` | always — invariants + `@` SoTs |
| `task-subagent-model-grok.mdc` | always |
| `ci-local-gates.mdc` | globs: `scripts/ci/**,.github/workflows/**,.githooks/**` |
| `doc-engine-cohesion.mdc` | globs: `src/doc_engine/**,tests/doc_engine/**` |
| `stage0-citation.mdc` | globs: `**/spring-signals/**,scripts/fixtures/**,scripts/coverage/**` |
| `research-spec-drafts.mdc` | globs: `docs/research/**/*.md,docs/design/**/*.md` |
| `session-log-nest.mdc` | globs: nest + packer paths — ≤225 / `START__slug` |
| `principal-research-gate.mdc` | agent-requested |
| `cross-domain-isomorphism.mdc` | agent-requested (demoted) |
| `tip-recovery-manual.mdc` | manual |

---

## 7. Adversarial evaluation

| Risk | Mitigation |
| --- | --- |
| Demoting iso → agents forget Structure-Adopt | Agent-requested description + skill still discoverable; research glob points Bloom |
| Slim constitution → soften 98.7 | Invariants stay always-on; success metric requires refuse soften |
| Nested AGENTS temptation | Explicit Refuse in memo + constitution pointer |
| DeepWiki stale wiki as Spec proof | Primary docs Evidenced; Ask miss recorded |
| Mass rename docs | Explicit Refuse |

---

## 8. Explicit refuse

- Mass `.md` → `.mdc` under `docs/`
- `SKILL.md` → `.mdc`
- Nested AGENTS.md path-scoping **in addition to** MDC globs
- Mega-linter / cursor-doctor as merge SoT
- Growing alwaysApply to “be safe”
- Softening constitution gates
