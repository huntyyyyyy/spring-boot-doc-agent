---
title: E-CTX0 — Agent context bloat from huge markdown (arXiv + SE mental models)
status: DRAFT Spec — CTX1–CTX10 pending Approve
date: '2026-08-10'
research_window: 2023-01-01 → 2026-08-10
claim_tiers: Evidenced / Confirmed / Unknown
product: Meta-repo agent hygiene (Cursor/Claude tips) — not the product kernel Source of Truth
related:




- docs/research/se-quality-synthesis-2026-08-08.md
do_not:
- paste full research memos into every agent turn
- treat million-token windows as “just dump the docs”
- treat ★≥1k as automatic Adopt (see memo 27 / fake-star literature)
- adopt MemGPT/Letta / complexity-trap *code* as product deps without discernment
- replace deterministic System of Record (claims, coverage.xml) with large language model summary memory
spec_gate: DRAFT E-CTX0 (2026-08-10) — CTX1–CTX10 + deepdive CTX11–CTX18 pending Approve
gh_sor_bar: ≥1000★ + recent push is a filter only; require fork/velocity/institution/paper
  discernment (memo 27)
last_reviewed: '2026-08-10'
---

# Principal memo: huge markdown vs agent working set

**Question.** Do giant in-repo markdown SoTs (research packets, session-logs, STATUS)
bloat large language model agent context — and what do arXiv / SE architecture models prescribe?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**This memo is intentionally short** — embodying the hygiene it recommends.

---

## 0. One-page verdict

| Stance | Decision |
| --- | --- |
| **Embody** | Context = **working set**, not warehouse; U-shaped attention; System of Record on disk, slice into tips; **algorithm+Accept ≻ product★** (memo 28) |
| **Adopt** | Section-first reads; map/index doors (DOC1); observation masking / drop over large language model-summary-of-docs; MemGPT *mental model* (RAM vs disk) without runtime dep; **self-orchestrated ports** of named methods |
| **Spike** | Soft LOC/token budget on research memos; inject-map only (already look-first); “open §N” agent instruction; thin mask-policy porter |
| **Refuse** | Dumping whole `quality-backlog` / packet 21–25 into every tip; MemGPT/Letta as merge Source of Truth; chat-dump research (DOC12 / STK); **★-only Adopt of viral AI tools**; **token-prune of agent action grammar** |

**Answer to the session question:** yes — long markdown in the middle of the tip is exactly the failure mode Liu et al. measure. Bigger windows do not fix it.

**Deepdive:** repo discernment + star inflation → [`27`](27-agent-context-repo-discernment-2026.md).  
**Algorithm-first build doctrine:** [`28`](28-agent-context-algorithm-first-2026.md).

---

## 1. Evidence inventory (arXiv + GH)

| Claim | Tier | Source |
| --- | --- | --- |
| Relevant facts at **start/end** of long context recall better; **middle** degrades; longer context worsens use | Evidenced | Liu et al., *Lost in the Middle*, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) |
| SE agents: append-only trajectories explode cost; **simple Observation Masking** ≈ large language model-summary solve rate, ~½ cost | Evidenced | JetBrains-Research, *The Complexity Trap*, [arXiv:2508.21433](https://arxiv.org/abs/2508.21433) · code [JetBrains-Research/the-complexity-trap](https://github.com/JetBrains-Research/the-complexity-trap) (17★ — **below** GH System of Record bar; paper still Evidenced) |
| Context engineering = retrieval + processing + **management** (memory hierarchy, compression) | Evidenced | Mei et al. survey, [arXiv:2507.13334](https://arxiv.org/abs/2507.13334) · catalog [Meirtz/Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) (**3273★**, pushed 2026-05) |
| Context maintenance as **callable tool**; workspace = stable task + LTM summary + STM fidelity | Evidenced | *Context as a Tool (CAT)*, [arXiv:2512.22087](https://arxiv.org/abs/2512.22087) |
| Hierarchical memory: context window ≈ RAM, external store ≈ disk; model pages via tools | Evidenced | Packer et al., *MemGPT*, [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) · [cpacker/MemGPT](https://github.com/cpacker/MemGPT) (**24k★**) |
| This repo already refuses chat-dump Source of Truth; stalker Spec is context-lean | Confirmed | E-STK0 memo 19; DOC12; look-first injects **map**, not whole corpus |
| Exact token waste of pasting `DOMAIN_MAP`+packet mid-tip | Unknown | Needs measure (Spike CTX-S1) |

DeepWiki: orientation only — not sole cite.

---

## 2. Mental models (principal SE / architecture)

| Model | Origin | Design implication here |
| --- | --- | --- |
| **Working set / locality** | Denning (OS) | Tip holds *current* Spec + touched code; rest stays on disk until `Read` |
| **RAM vs disk (MemGPT)** | arXiv:2310.08560 | `docs/research/**` = disk; agent context = RAM; page via path+section, not preload |
| **U-shaped attention** | arXiv:2307.03172 | Put task + invariants at tip **edges**; do not bury Accept criteria under lore |
| **Cognitive load (extraneous)** | Sweller CLT | Extraneous markdown = load that does not change the design decision |
| **Information hiding** | Parnas | Research domains hide internals; map exposes interfaces (DOC1 ≤2 levels) |
| **Living documentation** | Martraire | Prefer claims-gated current-state (`DOMAIN_MAP`, CONSTRAINTS) over append-only lore in-context |
| **Context as a tool (CAT)** | arXiv:2512.22087 | Compress/offload is an *action*, not a passive transcript |
| **System of Record vs derived vs sensor** | This repo / 16-A | Never promote large language model summary of docs to System of Record |

Classic SE texts above are **framework labels** (not arXiv); arXiv rows carry Evidenced weight for agent behavior.

---

## 3. Solution families → Embody / Adopt / Refuse

| Family | Examples | This repo |
| --- | --- | --- |
| **Position & budget** | Critical facts at edges; shorter payloads | **Embody** — tip briefs ≤1 screen; link paths |
| **Index / map doors** | Research README look-first | **Embody** — already shipped (E-DOC1) |
| **Mask / drop old observations** | Complexity Trap | **Adopt** for tool traces; **Spike** for “don’t re-read whole memo” |
| **large language model summarize history** | OpenHands / SWE-agent summaries | **Defer** as default — paper says masking ≈ equal; risk semantic drift on System of Record text |
| **External memory / MemGPT runtime** | Letta/MemGPT | **Refuse** as product dep; **Adopt** the RAM/disk *model* |
| **Agentic compress tools** | CAT / ACM-class | **Spike** only if tips routinely exceed budget; not kernel |
| **Bigger context models** | 1M windows | **Refuse** as structural fix — Liu: length still hurts middle use |

---

## 4. Spec gate — CTX1–CTX10 (Approve to Implement)

| ID | Decision | Stance |
| --- | --- | --- |
| **CTX1** | Treat agent context as working set; System of Record remains files on disk | Embody |
| **CTX2** | Agents Prefer section/`offset` reads; refuse whole-file habit for memos >~200 LOC | Adopt |
| **CTX3** | Soft research-memo budget: target ≤225 LOC (align size bar) or split synthesis | Spike |
| **CTX4** | Tip launcher paste: Active row + one Spec path + invariants — not backlog dump | Adopt |
| **CTX5** | Keep look-first map inject; do not expand inject to full memos | Embody |
| **CTX6** | Observation masking for long tool logs; no large language model-summary of CONSTRAINTS/claims | Adopt / Refuse summary-as-System of Record |
| **CTX7** | MemGPT/Letta runtime not a merge dependency | Refuse |
| **CTX8** | Complexity-trap *finding* (mask≈summary) Adopt as tip hygiene; code scaffold not System of Record (<1k★) | Adopt finding / Refuse scaffold |
| **CTX9** | Measure Spike CTX-S1: tokens from forced full-memo Reads vs section Reads on one tip | Spike |
| **CTX10** | Chat dumps / session lore stay non-Source of Truth (DOC12 / STK) | Embody |

---

## 5. Adversarial checklist

- [ ] Does a tip still work if the agent never saw memo 21–24 bodies — only DOMAIN_MAP § needed?
- [ ] Would large language model-summarizing CONSTRAINTS create a second System of Record? (must be no)
- [ ] Is “just use a bigger model” being used to avoid map/section discipline?
- [ ] Does CTX3 soft budget become a mechanical chop that destroys claim tiers? (pair with E-COH cohesion)

---

## 6. Exit / Archive

**Done when:** CTX1–CTX10 Approved; CTX-S1 measured or Deferred with reason; CONTRIBUTING / AGENTS gains a 5-line “context working set” note (Implement tip, not this draft).

**Not done:** shipping MemGPT; auto-summarizing research into chat memory.
