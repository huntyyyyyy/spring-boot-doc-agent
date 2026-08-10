---
title: E-CTX0 — algorithm-first quality frameworks (build/orchestrate from theory)
status: DRAFT amend — CTX19–CTX26 pending Approve with 26+27
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
parent:
  - docs/research/process/26-agent-context-markdown-bloat-2026.md
  - docs/research/process/27-agent-context-repo-discernment-2026.md
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/19-watch-stalker-agents-context-lean-2026.md
do_not:
  - vendor opaque viral MCP memory as “quality”
  - train CompactionRL / in-tree weight zoos as product SoT
  - token-prune agent action grammar (LLMLingua-class on trajectories)
  - replace claims/coverage oracles with compressed prose
spec_gate: DRAFT E-CTX0 algorithm-first (2026-08-10)
---

# Algorithm-first: theory → our orchestration (not ★-products)

**User stance (Adopt as product doctrine).** Prefer research algorithms, applied math,
and named quality frameworks we can **discern and implement/orchestrate ourselves**
over black-box high-★ agent-memory products. If a repo is only a thin wrapper on an
opaque service, it is not SoR — the **paper + measurable predicate** is.

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Stance | Decision |
| --- | --- |
| **Embody** | SoR = **named algorithm + Accept predicate**; code is a port under our gates (LOC, complexipy, claims, 16-A) |
| **Adopt** | Step-/observation-level **masking** (Complexity Trap); MemGPT **tier algebra** as design; CAT **compress-as-tool**; Liu **edge placement**; DOC map doors |
| **Spike** | Thin in-repo porter for mask/budget; optional AGORA-class step scorer only after measure; StarScout offline |
| **Refuse** | Viral memory MCP as merge dep; token-level extractive compression on agent actions; LLM-summary of SoR docs; trainable compaction weights in-tree |

---

## 1. Quality bar for “take and build”

An external idea is **build-eligible** only if all hold:

| # | Gate | Why |
| --- | --- | --- |
| B1 | **Named method** (paper § or formal rule) | Not a README metric (“99% tokens”) |
| B2 | **Clear inputs/outputs** | e.g. trajectory → masked trajectory; memo → section slice |
| B3 | **Falsifiable Accept** | solve-rate±ε, token±%, claims green — not vibes |
| B4 | **Fits constitution** | no second oracle; no utils bag; ≤225 / complexipy≤5 on *our* port |
| B5 | **Orchestrable** | strategies/ports (OCP); we own the loop |
| B6 | **Discernment** | ★ filter + memo 27 heuristics; paper/lab beats hypergrowth MCP |

Fail any → orientation only.

---

## 2. Algorithm menu (what to port vs refuse)

| Algorithm / theory | Math / mechanism (sketch) | Build here? |
| --- | --- | --- |
| **Observation masking** [arXiv:2508.21433](https://arxiv.org/abs/2508.21433) | Keep actions/decisions; drop or truncate aged tool observations under budget | **Yes — first port** (pure policy; no weights) |
| **Step-level retention / AGORA floor** [arXiv:2605.26596](https://arxiv.org/abs/2605.26596) | Never token-prune inside `(action, observation)`; always-keep system+task+last-K; optional relevance scorer | **Embody floor**; Spike scorer later |
| **Token extractive (Selective Context / LLMLingua-2)** [arXiv:2310.06201](https://arxiv.org/abs/2310.06201), [2403.12968](https://arxiv.org/abs/2403.12968) | Drop low self-info tokens | **Refuse on agent trajectories** — destroys action grammar `[Evidenced]` AGORA audit |
| **MemGPT paging** [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) | Core / recall FIFO / archival; page via tools | **Orchestrate ourselves** via Read/section + findings ledger — not Letta runtime |
| **CAT compress-as-tool** [arXiv:2512.22087](https://arxiv.org/abs/2512.22087) | Milestone compression into structured workspace | **Design pattern** for tip resets / handoffs |
| **Working set / locality** (Denning) | Resident set ≤ attention budget | **Process law** for tips |
| **U-placement** [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | Critical facts at context edges | **Prompt/orchestrator law** |
| **CompactionRL** class | Learned compaction policy | **Refuse** weight training as product SoT (E-STK0) |
| **Claims / coverage / tach** (this repo) | Deterministic predicates | **Already Embody** — context hygiene must not dilute |

---

## 3. Reference architectures we *study*, ports we *own*

| External | Use as | Do not |
| --- | --- | --- |
| Complexity Trap + SWE-agent harness | Reproduce mask policy; cite numbers | Vendor their scaffold |
| OpenHands condensers | Read event/condensation shapes | Depend on OpenHands |
| MemGPT/Letta | Tier vocabulary | Install as kernel |
| agentmemory / claude-mem / headroom / rtk | Discern ideas under memo 27 | ★-driven merge |
| StarScout [arXiv:2412.13459](https://arxiv.org/abs/2412.13459) | Audit ★ shortlists | Gate CI on it without Spec |

**Confirmed home for our port:** meta process / optional `scripts/` or Cursor hooks —
**not** `doc_engine` wheel guts — unless a later product Spec says otherwise.

---

## 4. Implementation shape (when Approve → Implement)

```text
tip_brief (edge) → Active + Accept + invariants
     │
     ├─ page: Read(path, section)          # archival disk
     ├─ mask: drop aged tool observations  # Complexity Trap
     ├─ never: token-prune action lines    # AGORA refuse
     └─ never: summarize CONSTRAINTS       # 16-A / claims SoR
```

Ports (OCP): `ObservationMaskPolicy`, `TipBriefBuilder`, `SectionPager` — no if/elif god.

Verify: CTX-S1 tokens; claims; complexipy≤5; no coverage.xml climb dual-write.

---

## 5. Spec delta — CTX19–CTX26

| ID | Decision | Stance |
| --- | --- | --- |
| **CTX19** | Prefer algorithm+Accept over product★ for context hygiene | Embody |
| **CTX20** | First implementable algorithm = observation/step masking (+ always-keep floor) | Adopt |
| **CTX21** | Refuse token-level extractive compression on agent action grammar | Refuse |
| **CTX22** | MemGPT/CAT/Liu are **orchestration laws** we encode; runtimes optional never | Embody |
| **CTX23** | Any port lives behind strategies/ports; constitution gates apply | Embody |
| **CTX24** | Viral memory MCP may inform Spike only after B1–B6 | Adopt discernment |
| **CTX25** | Trainable compaction / CompactionRL not product SoT | Refuse |
| **CTX26** | Docs SoR stay file-backed; compression never invents a second SoR | Embody |

---

## 6. Adversarial

- [ ] Is “build ourselves” becoming NIH of OpenHands condensers? → port *policy*, not framework
- [ ] Does a relevance scorer sneak weights into CI critical path? → Spike only, off oracle
- [ ] Are we still tempted by 90k★ memory because orchestration feels slower? → measure CTX-S1 first

---

## 7. Exit

Approve **CTX1–CTX26** as one E-CTX0 packet (memos 26+27+28). Implement tip:
tip-brief + mask policy port + AGENTS blurb — **high-quality small code**, not a memory product.
