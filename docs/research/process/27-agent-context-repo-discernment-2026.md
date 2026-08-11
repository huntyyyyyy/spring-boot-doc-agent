---
title: E-CTX0 deepdive — models in depth + GH repo discernment (star inflation)
status: DRAFT amend to E-CTX0 — CTX11–CTX18 pending Approve with CTX1–CTX10
date: '2026-08-10'
research_window: 2023-01-01 → 2026-08-10
claim_tiers: Evidenced / Confirmed / Unknown
parent: docs/research/process/26-agent-context-markdown-bloat-2026.md
related:
- docs/research/process/19-watch-stalker-agents-context-lean-2026.md
- docs/research/process/26-agent-context-markdown-bloat-2026.md
do_not:
- treat ★≥1k as automatic Adopt (fake-star campaigns target AI/LLM repos)
- run StarScout as CI gate without Spec (heavy GHArchive)
- Adopt viral memory MCP stacks as merge SoT from ★ alone
- equate “low ★” with “low quality” when arXiv+institution backs the artifact
spec_gate: DRAFT E-CTX0 deepdive (2026-08-10)
gh_discernment: ★ floor is filter not proof; fork/watch/velocity/institution/paper
  required
last_reviewed: '2026-08-10'
---

# Deepdive: models + repositories under star-inflation pressure

**Why this amend.** Memo 26 stated the short verdict. User ask: go **deeper** on the
mental models, dig into repos, and question whether high-★ “winners” are inflated
while lower-★ paper repos are actually better SoR.

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. Verdict delta (vs memo 26)

| Was | Now |
| --- | --- |
| GH SoR ≈ ★≥1k + recent push | **Necessary filter, not sufficient** — AI/LLM tools are an explicit fake-star *target class* `[Evidenced]` |
| Prefer famous memory stacks (MemGPT/agentmemory/…) for patterns | Prefer **algorithm + measurable SE result**; JetBrains Complexity Trap (17★) outranks viral MCP READMEs for *mask vs summarize* |
| magic-context / rtk above floor ⇒ Spike-worthy | Add **fork/star + ★/day + institutional** gates; flag LOW_FORK / hypergrowth as **Unknown integrity** |

---

## 1. Models — deeper (architecture meaning)

### 1.1 Working set / thrashing (Denning)

Agents that re-`Read` whole research packets each turn **thrash**: the working set
exceeds the attention budget, so every decision pays cold-cache cost. Tip hygiene =
keep Spec Accept + touched paths resident; page lore from disk.

### 1.2 U-shaped attention (Liu et al., [arXiv:2307.03172](https://arxiv.org/abs/2307.03172))

Not only “don’t dump docs” — **order** matters. Put Active tip + invariants at the
**edges** of the injected prompt; links to memos in the middle are fine because the
model should *tool-read* them, not memorize them mid-context.

### 1.3 Observation masking vs LLM summary ([arXiv:2508.21433](https://arxiv.org/abs/2508.21433))

**Mechanism:** drop or truncate old *tool observations*; keep decisions/actions.
On SWE-bench Verified inside SWE-agent, masking ≈ LLM-summary solve rate at ~½ cost.
**Implication for markdown SoR:** summarizing CONSTRAINTS into chat memory is the
*wrong* analogue — SoR text must stay file-backed. Masking applies to **trajectories
and tool dumps**, not to replacing claims-gated docs.

Repo: [JetBrains-Research/the-complexity-trap](https://github.com/JetBrains-Research/the-complexity-trap) —
**17★**, fork/star **0.29**, JetBrains Research, paper-primary. **Algorithm SoR: high.
★ SoR: refuse.** This is the poster child for “low stars, better signal.”

### 1.4 MemGPT hierarchy ([arXiv:2310.08560](https://arxiv.org/abs/2310.08560)) → Letta

| Tier | MemGPT | This repo mapping |
| --- | --- | --- |
| Main / core | Always-resident instructions | `AGENTS.md` / tip brief / Active row |
| Recall FIFO | Recent messages | Current tip transcript (maskable) |
| Archival | External searchable store | `docs/research/**`, session-log, findings ledger |

**Adopt** the tier map. **Refuse** Letta/MemGPT as product runtime (lock-in; E-STK0).
Note: `cpacker/MemGPT` and `letta-ai/letta` resolve to the **same** metrics today
(rename/platform) — don’t double-count ★.

### 1.5 Context as a Tool / CAT ([arXiv:2512.22087](https://arxiv.org/abs/2512.22087))

Workspace = **stable task semantics** + **condensed LTM** + **high-fidelity STM**.
Map: Spec Accept = stable; backlog/DOMAIN_MAP = LTM on disk; tip = STM.
Compression is an **agent action at milestones**, not append-only history.

### 1.6 Context engineering survey ([arXiv:2507.13334](https://arxiv.org/abs/2507.13334))

Taxonomy: retrieve → process → manage. Our DOC1 map is **retrieve**; section reads are
**process**; masking + tip reset are **manage**. Catalog GH
[Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering)
(~3.2k★, organicish f/s) = **cartography**, not implement SoR.

### 1.7 Cognitive load / information hiding / living docs

Extraneous markdown raises **extraneous** load (Sweller). Domain folders **hide**
internals (Parnas). Claims-gated current-state beats lore dumps (Martraire). Already
aligned with E-DOC1 / E-STK0.

---

## 2. Fake stars — why ★ floors mislead

| Claim | Tier | Source |
| --- | --- | --- |
| ~6M suspected fake stars (2019–2024); surge in 2024; AI/LLM repos among non-malware promotion classes | Evidenced | He et al., [arXiv:2412.13459](https://arxiv.org/abs/2412.13459) (ICSE ’26); code [hehao98/StarScout](https://github.com/hehao98/StarScout) (~188★) |
| Detectors: low-activity accounts + lockstep starring bursts | Evidenced | Same |
| Short-term growth-hack effect &lt;~2 months; long-term liability | Evidenced | Same |
| This tip did **not** run StarScout on candidates | Confirmed | API metrics only |

**Policy shift:** ★≥1k + 14-day push remains a **research filter**. Implement/Adopt
requires **discernment** (already E-STK0 §5.1) plus the heuristics below.

### 2.1 Discernment heuristics (API-cheap; not StarScout)

Fetched **2026-08-10** via GitHub API:

| Signal | Prefer | Suspect |
| --- | --- | --- |
| fork/star | ≳0.08–0.15 for apps | ≪0.05 at multi-k★ |
| ★/day since create | modest / event-tied | hundreds/day sustained |
| Institution / paper | JetBrains, CMU, peer-reviewed | README-only “99% savings” |
| Watchers vs ★ | some committed audience | tiny watch at huge ★ |
| Issues/PRs | real bug traffic | empty or botty |

**Hypergrowth examples (Unknown integrity — not proven fake):**

| Repo | ★ | f/s | ★/day | Note |
| --- | --- | --- | --- | --- |
| `rtk-ai/rtk` | ~75k | 0.063 | ~379 | Token-compress CLI; viral velocity |
| `headroomlabs-ai/headroom` | ~66k | 0.076 | ~307 | Listed E-STK0 Spike; re-score under inflation lens |
| `thedotmack/claude-mem` | ~90k | 0.087 | ~263 | E-STK0 Defer; ★ alone overweighted historically |
| `cortexkit/magic-context` | ~1.7k | **0.048** | — | Above 1k floor but **LOW_FORK** flag |
| `millionco/react-doctor` | ~14k | **0.032** | ~81 | Pattern useful; ★ integrity Unknown |

**High-signal low-★ (or paper-first):**

| Repo | ★ | Why it can beat a 50k★ MCP |
| --- | --- | --- |
| `JetBrains-Research/the-complexity-trap` | 17 | Controlled SE-agent experiment; NeurIPS workshop paper |
| `lixiaochuan2020/agentic-context-management` | 25 | ACM paper companion — algorithm Spike only |
| `hehao98/StarScout` | 188 | Meta-tool to audit the ★ signal itself |

**Mature scaffolds (still not auto-Adopt for *our* kernel):** OpenHands, SWE-agent,
Aider, LangGraph — organicish f/s, real issue load; use as **reference patterns**
(condensers / loops), not deps.

**Tiny marketing-heavy (Refuse merge SoR):** `context-mem` (~15★), `context-compress`
(~1★), `agent-mem` (~5★) — may hold ideas; claims like “99.1% token savings” stay
**Unknown** until reproduced here.

---

## 3. Re-scoring E-STK0 / E-CTX memory candidates

| Candidate | Prior stance | Deepdive stance |
| --- | --- | --- |
| Complexity Trap finding | Adopt finding | **Strengthen** — best SE evidence for mask≳summary |
| MemGPT/Letta *model* | Adopt model / Refuse runtime | Unchanged |
| agentmemory / claude-mem / headroom / context-mode | Spike/Defer/Refuse mix | **Downgrade confidence in ★**; require fork/velocity + local reproduce before Spike budget |
| magic-context | Spike (barely ≥1k) | **Spike only** with LOW_FORK caveat; prefer paper algorithms |
| OpenHands condensers | Reference | Keep as **Evidenced implement reference** (not dep) |
| StarScout | — | **Spike** optional offline audit; never silent ★ trust |

---

## 4. Spec delta — CTX11–CTX18

| ID | Decision | Stance |
| --- | --- | --- |
| **CTX11** | ★≥1k is filter not proof; AI/LLM repos need discernment | Embody |
| **CTX12** | Record fork/star, ★/day, watchers, institution/paper beside ★ in research tables | Adopt |
| **CTX13** | Prefer arXiv+controlled SE eval over viral MCP README metrics for algorithm Adopt | Embody |
| **CTX14** | Flag f/s≪0.05 or sustained ★/day≳100 as Unknown integrity until audited | Adopt |
| **CTX15** | Low-★ paper repos eligible as **algorithm SoR**; still Refuse as unreviewed merge dep | Adopt |
| **CTX16** | Do not double-count MemGPT/Letta ★ | Adopt |
| **CTX17** | Optional Spike: run StarScout / manual lockstep checks on Spike shortlist | Spike |
| **CTX18** | Tip docs: section reads + edge placement of Accept (Liu) | Embody |

---

## 5. Adversarial

- [ ] Are we refusing a 17★ JetBrains result because of the old ★ bar? (must not)
- [ ] Are we Adopting a 90k★ memory daemon because E-STK0 listed it? (re-check)
- [ ] Would StarScout false positives block a real lab repo? (hence Spike, not gate)
- [ ] Does “discernment” become vibes? → keep **numeric** heuristics in the table

---

## 6. Exit

Merge into E-CTX0 Approve packet (26+27). Implement tip still: AGENTS working-set
blurb + section-read habit — **not** shipping memory runtimes.
