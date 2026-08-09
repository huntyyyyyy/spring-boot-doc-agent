---
title: E-DOC0 — Research domain taxonomy + claude→docs consolidation + look-first hook
status: RESEARCH COMPLETE — awaiting Approve E-DOC0 (2026-08-09)
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Meta-repo process SoR (docs) + Cursor/Claude agent adapters — not doc-engine kernel
related:
  - docs/product-architecture.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - .cursor/skills/principal-se-research-epic/SKILL.md
  - docs/design/ci-workflow-modularity-design-2026-08-09.md
do_not:
  - dump chat transcripts / raw session lore as research SoT
  - deep-nest research like docs/design/ddia-north-star (64 files / 29 dirs)
  - delete adapters/claude without a Cursor-equivalent adapter Spec
  - treat .claude/settings deny lists as deletable without check F replacement
  - mass-move claude/ without rewriting check_repo_claims OWN_PATH_PREFIXES + predicates
spec_gate: PENDING APPROVE E-DOC0 — decisions DOC1–DOC12
---

# Principal memo: research domains, claude→docs, look-first hook

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Consolidate research into domains? | **Yes.** Flat `01`–`17` ordinals are taxonomy debt; domains ≤2 deep + epic IDs in frontmatter. `[Confirmed]` |
| Too many files/folders = reshape? | **Yes as a signal, not a LOC rule.** `docs/design/ddia-north-star/` (64 files / 29 dirs) is the anti-pattern for research; research stays **thin memos + index**, not a second DDIA tree. |
| Force agents to look at research first? | **Yes, via Cursor-native hooks** (not Claude-only). Soft rules alone are insufficient. Cloud caveat: `sessionStart` **does not run** on cloud agents — use `beforeSubmitPrompt` + `preToolUse` fail-closed. `[Evidenced]` [Cursor hooks](https://cursor.com/docs/hooks.md) |
| Kill `claude/` and `.claude-plugins`? | **Migrate valuable content into `docs/`**; **do not delete** Claude *adapter* packaging (`adapters/claude/`, `.claude/settings.json` deny+hooks, `.claude-plugin/marketplace.json`) without an explicit adapter-retire Spec. There is **no** `.claude-plugins/` tree today — only `.claude-plugin/`. |
| Chat / Claude-only lore? | **Flag + archive or distill** — refuse as domain SoT. |

**Product rule (proposed):** `docs/research/` is the only research SoR. Agents must open the domain index (and the matching domain memo when design-shaped) before weighing frameworks or writing Spec/impl. Claude Code remains an **optional adapter**, not the docs home.

---

## 1. Confirmed inventory

### 1.1 `docs/` today

| Area | Scale | Notes |
| --- | --- | --- |
| `docs/research/` | ~17–18 flat memos | Ordinal series + synthesis + backlog; numbering **gap 13–16** (and tip-only `17` on E-CQL branch) |
| `docs/design/` | 7 loose + **ddia-north-star 64/29** | Design Specs OK; DDIA tree is deep SoR — **do not clone that shape under research** |
| `docs/guides/`, `reviews/`, `examples/` | small | Keep |

### 1.2 `claude/` today (~93 files)

| Entry | Classification | Disposition |
| --- | --- | --- |
| `steering-prompts/` (15) | Repo-valuable (claims `verify:` corpus) | → `docs/process/steering-prompts/` (or keep path alias one release) |
| `session-log.md` | Repo-valuable | → `docs/process/session-log.md` |
| `tool-quirks.md` | Repo-valuable | → `docs/process/tool-quirks.md` |
| `research/` (32 md) | Durable ADRs mixed with spikes | Distill into domain folders; stubs for moved paths |
| Root research/plans (architecture, JPA, wave1 adjudications, …) | Ambiguous | Distill or `docs/research/archive/` |
| `llms/` (29) | Repo process, Claude-named | → `docs/process/pr-verification/` (rename); keep `check_llms_coverage` contract |
| Claude product UX only | — | **Flag**, do not promote to SoT |

### 1.3 Claude runtime packaging (keep unless adapter-retire Spec)

| Path | Role | If removed |
| --- | --- | --- |
| `adapters/claude/` | Marketplace plugin (agents, hooks, skills, SEARCH.md) | Breaks Claude Code install; product-architecture A+C |
| `.claude/settings.json` | Allow/deny + PreToolUse wiring | Breaks dual control with check F (Grep/network denies) |
| `.claude/hooks/check_pipe_exit_code.py` | Pipe-exit false-green | False greens return in Claude sessions |
| `.claude/skills/verify-state-claims` | Claims hygiene | Soft only; CI claims remain |
| `.claude/skills/stf-*` | STF planner UX | Claude-only workflow |
| `.claude-plugin/marketplace.json` | Points `source` → `adapters/claude` | Marketplace discoverability |
| `.claude-plugins/` | **Absent** | N/A — user name likely meant `.claude-plugin/` |

**Orphan:** `.cursor/hooks/__pycache__/bridge_claude_policy.*.pyc` with **no** tracked `.cursor/hooks.json` / source — refuse rebuilding without Spec.

### 1.4 “Look at research first” today

| Mechanism | Force? | Notes |
| --- | --- | --- |
| `.cursor/rules/se-quality-constitution.mdc` | Soft | alwaysApply |
| `.cursor/skills/principal-se-research-epic` | Soft | Spec before code |
| Claude `adapters/claude/hooks` | Hard for search/network/commit | **Not** research-index |
| Cursor native research gate | **Missing** | Must Spec |

---

## 2. External primaries (hooks)

| Source | Claim | Tier |
| --- | --- | --- |
| [Cursor hooks](https://cursor.com/docs/hooks.md) | `beforeSubmitPrompt`, `preToolUse`, `sessionStart`; project `.cursor/hooks.json`; cloud loads project hooks | Evidenced |
| Same docs — cloud table | **`sessionStart` / `sessionEnd` not available** on cloud agents | Evidenced |
| [Third-party hooks](https://cursor.com/docs/reference/third-party-hooks.md) | Claude Code hooks can map into Cursor; prefer native Cursor format for full features | Evidenced |

---

## 3. Proposed taxonomy (≤2 levels under `docs/research/`)

```text
docs/research/
  README.md                 # domain map + “how to pick a domain before new research”
  quality-backlog.md        # stays root of research (active stream SoT)
  se-quality-synthesis-….md # stays root (cross-domain merge)
  process/                  # SDD, foundational SE, frameworks, dynamics
  coverage-quality/         # oracle/climb, metrics, adequacy, suite-stalking
  ci/                       # workflow modularity, CI UX, CodeQL signals skip
  kitchen/                  # kitchen harness
  modularity/               # Stage-0 ports, test-suite BCs
  stage0/                   # covering/absence/recall, claim-symbol, fact-store ADRs (from claude/research)
  archive/                  # superseded WIP, duration receipts, distilled adjudications
docs/process/               # session-log, tool-quirks, steering-prompts, pr-verification (from claude/)
```

**File-count heuristic (Adopt, not hard SoT):** if a **domain folder** grows past ~12 active memos or gains a third nesting level, stop and **reshape concepts** (merge memos, promote a synthesis, or split a new top-level domain) — do not add `sub/sub/sub/`.

**Stable IDs:** epic keys (`E-CM0`, `E-CQL0`, `E-DOC0`) in frontmatter are the primary cross-ref; drop ordinal dependence for new memos.

---

## 4. Deep fit — Embody / Adopt / Refuse

| Choice | Stance | Why here |
| --- | --- | --- |
| Domain folders ≤2 deep + epic IDs | **Embody** | Fixes ordinal/gap debt; matches principal skill “write under docs/research” |
| Thin `docs/research/README.md` map (claims-derived counts OK) | **Embody** | Hook + humans share one entry door |
| Cursor `.cursor/hooks.json` look-first | **Embody** | Soft rules failed to force scope; cloud needs non-`sessionStart` events |
| Migrate `session-log` / `tool-quirks` / steering / durable ADRs into `docs/` | **Adopt** | Same tip as taxonomy **or** phased; claims rewrite mandatory |
| Keep `adapters/claude` + `.claude*` as adapter runtime | **Embody keep** | Product A+C; not “Claude folder lore” |
| Mirror Claude deny hooks into Cursor where useful | **Adopt** | Pipe-exit / text-search already have Cursor gaps |
| Huge nested research trees | **Refuse** | DDIA under design is enough nesting |
| Chat transcripts / raw Cowork dumps as SoT | **Refuse** | Distill or archive |
| Delete marketplace / adapter to “simplify docs” | **Refuse** without adapter-retire Spec |
| Dual-home root `skills/` + `adapters/claude/skills/` forever | **Refuse** | Pick install SoR (separate ticket) |

---

## 5. Look-first hook design (native Cursor)

### 5.1 Goals

1. At prompt submit: inject **research domain map** path + instruction to select domain before new framework weighing.
2. Before design-shaped writes (`docs/design/**`, new `docs/research/**`, SoT-touching `src/**` per matcher): require evidence the agent **read** `docs/research/README.md` (and optionally the domain README) in-session — fail closed with a short deny reason pointing at the map.
3. Work on **cloud agents** (no `sessionStart`).

### 5.2 Proposed events

| Event | Behavior |
| --- | --- |
| `beforeSubmitPrompt` | Always inject additionalContext: research map + backlog + “pick domain before Spec” |
| `preToolUse` matcher Write/StrReplace/EditNotebook | If path matches design-shaped glob and session has no `research_scope` receipt → **deny** with reason |
| Receipt | Sidecar under `.git/` or agent-temp: written when Read tool opens `docs/research/README.md` (observe via `postToolUse` on Read) — exact mechanism Spike DOC-S1 |
| `sessionStart` | Optional IDE-only inject; **do not rely on it for cloud** |

### 5.3 Fail-closed rules

- Missing hooks.json / hook crash with `failClosed: true` on design writes → block (or degrade to ask — Spec choice **DOC8**).
- Docs-only typo fixes under `archive/` may be allowlisted.
- Never block reading research.

### 5.4 Limitation

Receipt forgery (agent writes receipt without reading) is possible if receipt is a plain file — mitigate by tying receipt to **postToolUse Read** of the map (hash path+mtime) in the hook process, not agent-authored markdown.

---

## 6. Claude consolidation — flag list (cannot be “just docs”)

| Item | Why Claude-tied | Action |
| --- | --- | --- |
| `adapters/claude/**` | Marketplace plugin runtime | **Keep**; document under `docs/` as adapter |
| `.claude/settings.json` denies + PreToolUse | Claude Code tool policy; pairs with check F | **Keep** until Cursor-native equivalents cover the same hazards |
| `.claude/hooks/check_pipe_exit_code.py` | Claude PreToolUse | Keep; **port** to Cursor `beforeShellExecution` in E-DOC1 |
| `.claude/skills/stf-*` | Claude skill UX (`disable-model-invocation`) | Keep or move under `adapters/claude` only; not `docs/research` |
| `.claude-plugin/marketplace.json` | Install pointer | Keep |
| CONSTRAINTS / CLAUDE.md prose citing deleted `hooks/` at repo root | Stale paths | Fix in migration (claims) |
| `.claude-plugin/plugin.json` cited in CONSTRAINTS | **Missing file** today | Correct claim or restore — do not invent |

**User intent “don’t need claude folder”:** satisfied by **emptying `claude/` into `docs/process` + `docs/research/{domain}`**, leaving Claude **adapter** trees. That is not the same as deleting Claude support.

---

## 7. Better choices earlier

| Debt | Better earlier |
| --- | --- |
| Flat `01`–`N` research | Domain folders + epic IDs from first principal memos |
| Writing new SoT under `docs/research` while leaving `claude/research` live | Single SoR + stubs on first migration (ddia stub pattern) |
| Soft Cursor rules without hooks.json | Native look-first when constitution landed |
| CLAUDE.md still describing root `hooks/` | Update paths when adapters landed |
| Ordinal gap 13–16 | Don’t imply continuity; use epic IDs |

---

## 8. Spec decisions (DOC1–DOC12)

| ID | Decision |
| --- | --- |
| **DOC1** | `docs/research/` is the only research SoR; domains ≤2 deep; epic ID primary key |
| **DOC2** | Land `docs/research/README.md` domain map as the forced entry door |
| **DOC3** | Migrate durable `claude/research/*` into domains; wave1 adjudications / raw plans → `archive/` or distill |
| **DOC4** | Move `session-log`, `tool-quirks`, `steering-prompts`, `llms/` → `docs/process/` (names as in §3) |
| **DOC5** | After migrate + claims rewrite, `claude/` becomes tombstone stub or deleted; **claims must pass** |
| **DOC6** | Keep `adapters/claude/`, `.claude/`, `.claude-plugin/` unless separate **E-ADP-retire** Spec |
| **DOC7** | Cursor `.cursor/hooks.json` look-first: `beforeSubmitPrompt` inject + `preToolUse` deny design writes without research-map Read receipt |
| **DOC8** | Hook failure policy: **fail closed** on design-shaped writes (`failClosed: true`); never fail closed on Read of research |
| **DOC9** | Do not rely on `sessionStart` for cloud; document cloud vs IDE matrix in CONTRIBUTING |
| **DOC10** | Domain file-count heuristic ~12 active memos → reshape Spec, not deeper nesting |
| **DOC11** | Rewrite `check_repo_claims` prefixes/globs/predicates in the **same** migration commits |
| **DOC12** | Refuse: chat dumps as SoT; DDIA-shaped research trees; deleting adapter without retire Spec; dual skill homes |

---

## 9. Adversarial checklist

- [ ] Can cloud agents skip the gate because only `sessionStart` was wired?
- [ ] Does moving `steering-prompts` break MIRRORED_PROMPT_GLOB / verify predicates?
- [ ] Is `OWN_PATH_PREFIXES` updated so claims still scan process docs?
- [ ] Did we accidentally put session-log under research SoT?
- [ ] Can an agent forge a research receipt without a Read event?
- [ ] Does look-first block legitimate tiny typo fixes (allowlist)?
- [ ] Is Claude marketplace install still documented after `claude/` emptying?
- [ ] File/folder explosion: any domain already needing reshape before migrate?

---

## 10. Epic E-DOC0 → E-DOC1

### E-DOC0 — Spec (this memo)

| ID | Acceptance |
| --- | --- |
| DOC0-1 | Human Approve **DOC1–DOC12** |
| DOC0-2 | Backlog P14 stamped; Implement blocked until Approve |

### E-DOC1 — Implement (phased)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| DOC1-1 | Domain folders + README map + move existing `docs/research` memos (no content rewrite) | Map links resolve; backlog paths updated |
| DOC1-2 | `.cursor/hooks.json` + `scripts/ci` or `.cursor/hooks/*` look-first scripts + characterization tests | Deny without Read receipt; cloud-safe events |
| DOC1-3 | Migrate `claude/{session-log,tool-quirks,steering-prompts,llms,research}` → docs; stubs; claims rewrite | `check_repo_claims` green; CONTRIBUTING/CLAUDE/AGENTS paths honest |
| DOC1-4 | Port pipe-exit (and optionally text-search) to Cursor hooks | Cursor parity note in tool-quirks |
| DOC1-5 | Tombstone/remove empty `claude/`; leave adapters | No broken marketplace pointer |

### Spike

| ID | Question | Exit |
| --- | --- | --- |
| DOC-S1 | Exact Cursor hook JSON schema for additionalContext + deny on this Cursor build | Working fixture in CI or documented Unknown + manual verify |
| DOC-S2 | Whether `llms/` stays enforcing-adjacent or becomes pure docs | Decision recorded; `check_llms_coverage` paths updated |

### Exit / invariants

Approve → phased Implement → Verify claims/hooks → Archive. Do not weaken fail_under / complexipy / LOC. One tip writer. Do not merge mass moves without claims green.

---

## 11. Explicit refuse

- Research tree nested like `ddia-north-star`
- Chat transcript SoT
- Deleting `.claude` / `adapters/claude` / marketplace as part of “docs cleanup”
- Relying only on soft alwaysApply rules for look-first
- Implementing mass moves before Approve of DOC1–DOC12
