---
title: E-STK0 — Watch/stalker agents (findings → research → refactor) without context bloat
status: E-STK0 APPROVED (2026-08-09) — merge Approve of STK1–STK10
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Meta-repo process SoR + optional Cursor/CI watch agent — not doc-engine kernel SoT
related:
  - docs/design/suite-stalking-sensors-design-2026-08-09.md
  - docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - docs/research/process/18-docs-research-taxonomy-claude-consolidation-2026.md
do_not:
  - replace deterministic oracle / suite sensors with an always-on LLM chat
  - accumulate raw tool logs as research SoT (chat-dump refuse DOC12)
  - treat commercial “mend” SaaS or GitHub repos under **1000★** as implement SoR
  - schedule CompactionRL / weight training as a product dependency
  - adopt `riponcm/projectmem` (≈579★) or `Acquarts/ai-repo-health-agent` (0★) as merge SoR
  - adopt agentmemory / context-mode / prime-agent as product dependencies or default hosts
  - treat ≥1k★ + recent push as automatic Adopt (discernment §5.1 required)
spec_gate: APPROVED E-STK0 (2026-08-09) — STK1–STK10
---

# Principal memo: stalker-shaped watch agents (mid-2026)

> **APPROVED — SPEC GATE E-STK0 (2026-08-09)**
>
> Merge Approve of **STK1–STK10**. **Embody** sensors + in-repo ledger + react-doctor
> *pattern*; **Adopt** rotate focus / Spec chain / watch≠fixer / cycle reset;
> **Spike** headroom / loopx-as-projection / optional gh-aw proposer. **Defer/Refuse**
> memory daemons, ELv2 routers, alternate hosts (§5.1). E-STK1 Implement stays Deferred
> until chosen as Active tip.

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is there a 2026 pattern for agents that *watch* systems, surface bugs / inefficiencies / wrong frameworks / gaps, then drive research + refactor adoption? | **Yes.** Strongest native shape is **sensor findings → compact external memory → research memo / backlog → Spec → implement**, not a forever-growing chat. `[Evidenced]` |
| What maps to this repo’s “stalker”? | **Suite-stalking sensors (E-RUN)** already Embody the *watch* half for CI plateaus — deterministic junit / cascade clarity; LLM flake triage refused. Broader “framework/gap stalking” is a **separate meta-agent** that must not dilute oracle SoT. `[Confirmed]` |
| How do mid-2026 systems avoid context bloat? | ≥1k★ + 14-day push qualifies **research SoR only**. Product stance (§5.1): thin **in-repo ledger** default; **Spike** headroom / loopx; **Defer** claude-mem; **Refuse** agentmemory dep + context-mode (ELv2) + alternate hosts — not Adopt those as merge deps. `[Evidenced]` |
| Adopt for *this* product now? | **Spec Approved.** **Embody** sensors + in-repo ledger + react-doctor *pattern*. **Adopt** process (rotate focus, Spec chain, cycle reset). **Spike** headroom (compress dumps) + loopx (handoffs) + optional gh-aw *proposer*. **Defer/Refuse** full memory daemons / alternate agent hosts / ELv2 routers (see §5.1). |

---

## 1. Problem frame (this product)

Desired behavior (user):

1. **Watch** — bugs, inefficiencies, wrong frameworks, operational gaps.
2. **Present** — findings + areas to research / adopt / refactor.
3. **Stay lean** — do not bloat agent context over time.

Category errors to refuse up front:

| Error | Why |
| --- | --- |
| LLM stalker as Cover% / fail_under proof | Constitution + synthesis refuse LLM-judge as 98.7 SoT |
| One chat that re-reads the whole repo each cycle | Quadratic cost + context poisoning (`Focus` paper) |
| “Rust stalker” product bundles (runner swap + RTS + flake LLM) as drop-in | E-RUN0 already refused most of that for oracle cell |
| Auto-merge refactor PRs from watch agents | Violates Spec → Implement → Verify; one tip writer |

---

## 2. Repo Confirmed baseline (suite “stalker”)

| Artifact | Role |
| --- | --- |
| [`suite-stalking-sensors-design-2026-08-09.md`](../../design/suite-stalking-sensors-design-2026-08-09.md) | E-RUN0 Approve **R1–R8**; implement D1/D2/D17 sensors only |
| Research 08 | Industry “Rust stalker” framing; prefer 2026 primaries; refuse in-tree Rust / suite-wide xdist |
| `quality-backlog` P7 | E-RUN1 Active for durations; D8 LLM flake triage **Defer** |
| E-DOC1 look-first | Domain map + backlog as forced entry — already a **findings door**, not a chat dump |

**Confirmed product rule:** *watch* for CI/oracle health = **sensors + step summary**. *Watch* for framework/gap debt = **research memos + backlog**, not a second oracle.

---

## 3. External primaries (prefer Jun–Aug 2026)

**GitHub implement SoR bar (this memo):**

1. Stars **≥1000** at research fetch.
2. **`pushed_at` within the last 14 days** of the research date (here: **2026-07-26 → 2026-08-09**). Stale tips are orientation-only even if famous.
3. Prefer **created/rewritten 2025–2026** with **tagged Releases and/or CHANGELOG**.
4. Below 1k★ **or** no push in that window → **Refuse as SoR** (arXiv may still Evidenced the algorithm).

### 3.0 Preferred GH SoR — ≥1k★ **and** pushed in last 14 days (fetched 2026-08-09)

Window: **`pushed_at` ≥ 2026-07-26**. Rows verified via GitHub API. Prefer **created 2025–2026** + Releases/CHANGELOG.

#### Lean context / memory (highest leverage for “don’t bloat”)

| Repo | Created | ★ | Last push | Releases / changelog | Fit |
| --- | --- | --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 2025-08 | ≈90.2k | **2026-08-09** | `CHANGELOG.md`; **v13.14.0** (2026-08-08) | Capture → AI compress → reinject relevant context across sessions (multi-harness) |
| [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 2026-01 | ≈65.6k | **2026-08-09** | `CHANGELOG.md`; **v0.34.0** (2026-08-05) | Compress tool outputs/logs/RAG **before** the LLM; library + proxy + MCP |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | 2026-02 | ≈26.8k | **2026-08-09** | `CHANGELOG.md`; tags → v0.9.28 | Coding-agent MCP memory; decay/forget; self-hosted SQLite |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | 2026-02 | ≈19.7k | **2026-08-09** | tags → v1.0.169 | Sandbox tool output (~98% reduction) + session memory via MCP/hooks |
| [huangruiteng/loopx](https://github.com/huangruiteng/loopx) | 2026-05 | ≈3.7k | **2026-08-09** | **v0.4.4** (2026-08-09) | Durable goals, evidence logs, verifiable handoffs across agent loops — stalker *team* kernel |
| [cortexkit/magic-context](https://github.com/cortexkit/magic-context) | 2026-03 | ≈1.7k | **2026-08-09** | `CHANGELOG.md`; **v0.35.0** (same day) | Self-managing memory for coding agents (Spike; just above 1k floor) |

#### Watch / continuous improve / act harnesses

| Repo | Created | ★ | Last push | Releases / changelog | Fit |
| --- | --- | --- | --- | --- | --- |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | 2026-05 | ≈10.7k | **2026-08-09** | v0.7.0 / v0.7.1; [arXiv:2605.09998](https://arxiv.org/abs/2605.09998) | Auto compaction + Continual Harness + quality gates |
| [millionco/react-doctor](https://github.com/millionco/react-doctor) | 2026-02 | ≈14.3k | **2026-08-09** | npm 0.9.10–0.9.11 | Deterministic scan → agent skill (React pattern only) |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 2025-07 | ≈27.6k | **2026-08-09** | deepagents 0.7.4–0.7.5 | Harness composition |
| [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | 2025-05 | ≈10.5k | **2026-08-09** | Active tip | Async coding agent → draft PRs |
| [github/gh-aw](https://github.com/github/gh-aw) | 2025-08 | ≈4.9k | **2026-08-09** | Official continuous-improvement workflows | Rotating Quality Improver + cache memory |
| [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | 2024-03 | ≈83.5k | **2026-08-09** | v1.9–v1.12 (Aug week) | Event log + condensers |
| [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | 2025-06 | ≈6.3k | **2026-08-03** | Active | Minimal fix-loop scaffold |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 2023-06 | ≈62.9k | **2026-08-07** | Apr 2026 algo refresh | Valid Spike; older tree than claude-mem/agentmemory |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 2023-10 | ≈24.2k | **2026-08-01** | Active | Spike; lock-in risk |

### 3.1 Watch → findings → adopt (papers + official)

| Source | Date | Claim | Tier | Note |
| --- | --- | --- | --- | --- |
| [gh-aw Continuous Improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/) | 2026-01 | Rotating focus + Discussions → Plan → PRs | Evidenced | Pairs with `github/gh-aw` |
| [icat-agent — arXiv:2606.25514](https://arxiv.org/abs/2606.25514) | 2026-06 | Event-passed Explorer/Validator/Patch; no shared megacontext | Evidenced | Paper SoR |
| [RefactorAssist — arXiv:2608.00924](https://arxiv.org/abs/2608.00924) | 2026-08 | Static-first then agentic refactor repair | Evidenced | Paper SoR |
| [ReProAgent — arXiv:2607.09123](https://arxiv.org/abs/2607.09123) | 2026-07 | Multi-stage reproduction tests from issues | Evidenced | Paper SoR |
| [ConFL — arXiv:2608.02974](https://arxiv.org/abs/2608.02974) | 2026-08 | Hierarchy-guided concurrent FL | Evidenced | Niche |

### 3.2 Context non-bloat (algorithms + mature memory stacks)

| Source | Date | Claim | Tier | Note |
| --- | --- | --- | --- | --- |
| **agentmemory** (§3.0) | 2026 | Projected MCP memory + decay/forget | Evidenced | Prefer for *coding* agents |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | ongoing; algo refresh Apr 2026 | Universal memory API; MCP/hooks; PreCompact | Evidenced | **≈62k★** — valid; heavier/productized |
| [letta-ai/letta](https://github.com/letta-ai/letta) | MemGPT lineage | Tiered agent-managed memory | Evidenced | **≈24k★** — Spike; lock-in risk |
| [Focus — arXiv:2601.07190](https://arxiv.org/abs/2601.07190) | 2026-01 | Agent-controlled compress/prune | Evidenced | Paper |
| [CompactionRL — arXiv:2607.05378](https://arxiv.org/abs/2607.05378) | 2026-07 | Trainable compaction | Evidenced | **Refuse** weight training in-tree |
| [CAT — arXiv:2512.22087](https://arxiv.org/abs/2512.22087) | 2025-12 | Context as callable tool | Evidenced | Algorithm |
| OpenHands condenser / SDK | 2025–2026 | `LLMSummarizingCondenser`; condensation events | Evidenced | Implement reference |

### 3.3 Orientation / refuse as implement SoR

| Source | Note | Tier |
| --- | --- | --- |
| [riponcm/projectmem](https://github.com/riponcm/projectmem) + [arXiv:2606.12329](https://arxiv.org/abs/2606.12329) | Algorithm OK; GH **≈579★** — superseded as SoR by **agentmemory** | Evidenced (paper) / **Refuse (GH)** |
| [Acquarts/ai-repo-health-agent](https://github.com/Acquarts/ai-repo-health-agent) | **0★** | **Refuse** |
| Truemend | Vendor | Unknown |
| DeepWiki | Cartography only | Confirmed process |

## 4. Pattern synthesis (what “good stalker” means in 2026)

```text
┌─────────────┐     compact projection      ┌──────────────────┐
│ Deterministic│ ───────────────────────────▶│ Findings ledger  │
│ sensors /    │   (MCP / JSON / SARIF /     │ (events, not     │
│ static scans │    step summary)            │  chat transcript) │
└─────────────┘                              └────────┬─────────┘
                                                      │
                         round-robin focus + cache     │
                                                      ▼
                                             ┌──────────────────┐
                                             │ Research / Spec  │
                                             │ (domain memo +   │
                                             │  backlog ticket) │
                                             └────────┬─────────┘
                                                      │
                         separate short-horizon agent  │
                                                      ▼
                                             ┌──────────────────┐
                                             │ Implement +      │
                                             │ Verify (gates)   │
                                             └──────────────────┘
```

| Layer | Mid-2026 recipe | Anti-pattern |
| --- | --- | --- |
| **Sense** | Deterministic auditors + CI sensors (E-RUN, CodeQL, claims, size) | LLM re-grades Cover% |
| **Remember** | **Thin in-repo ledger** (default); **headroom** Spike for dump compression; **loopx** Spike for handoffs | Memory daemons as SoT; ELv2 routers; 50+ MCP tool zoos |
| **Judge** | Rubric pivot (`icat` arXiv); pre-action warnings from **our** ledger | Soft “remember to check backlog” only |
| **Propose** | Findings → discussion/memo → Plan (gh-aw ResearchPlanAssignOps) | Silent auto-refactor on main |
| **Act** | Short-horizon fixer with event messages + compaction (`icat`, Focus, RefactorAssist static-first) | Shared megacontext explorer+fixer forever |
| **Close loop** | Backlog Archive + session-log only when steering claims move | Raw trajectories committed as research |

---

## 5. Embody / Adopt / Refuse (this Python CLI / meta-repo)

### 5.1 Deep adoption discernment (candidate → stance)

Star count and 14-day push qualify a tree as *research SoR*, not as *merge dependency*. Discernment below is against: Python 3.10+ CLI, deterministic gates, `quality-backlog` tip SoT, Cursor look-first, refuse LLM-as-fail_under, LOC≤225 / complexipy≤5, one tip writer, local-first.

| Candidate | Solves | Coupling / deps | Stance | Why (one line) |
| --- | --- | --- | --- | --- |
| **In-repo sensors** (E-RUN, claims, size, CodeQL, poke) | Detect CI/oracle/process defects | Already Python/CI | **Embody** | Only boolean watch SoT that matches constitution |
| **In-repo findings ledger → backlog** | Present research areas without chat dumps | Markdown/JSON under `docs/` | **Embody** | Closes the user loop without new runtime |
| **react-doctor *pattern*** | Deterministic scan → structured finding → skill/CI delta | Pattern only (not the React npm) | **Embody** | Best “stalker shape”; domain product refused |
| **OpenHands condenser *interface*** | Pipeline reduce history without deleting SoT | Pattern; stock LLM summarizer optional | **Embody** interface / **Refuse** LLM-summarize-as-SoT | Condensation events OK; lossy summary ≠ verified state |
| **gh-aw rotate focus + ResearchPlanAssignOps** | Continuous improve without scanning everything | Ideas from Actions markdown workflows | **Adopt** (process) | 60/30/10 + findings→Spec→tickets; not auto-merge factory |
| **icat / Focus / CAT / RefactorAssist** (arXiv) | Event-pass, cycle compress, static-first repair | Papers | **Adopt** (process) | Algorithms only — no weight training / host swap |
| **headroom** | Compress tool/logs/RAG *before* LLM | Python 3.10+ lib/proxy/MCP; can wrap agents | **Spike** | Highest-fit lean tool; never a quality gate; watch tip thrash from `wrap` |
| **loopx** | Durable goals, evidence, handoffs across loops | Python 3.11+; stdlib-ish; `.loopx/` state | **Spike** | Useful handoff kernel **only if** it *projects from* backlog — not a second tip |
| **gh-aw scheduled watcher** (optional) | Cron propose issues/discussions | GitHub Actions + cloud minutes | **Spike** | Proposer-only; merge gates stay local/deterministic |
| **claude-mem** | Cross-session capture→compress→reinject | Node/Bun + SQLite/Chroma; Claude-first hooks | **Defer** | Memory daemon beside SoT; risk of non-auditable second tip + optional cloud |
| **magic-context** | Self-managing long context | TS/Bun; OpenCode/Pi hosts | **Defer** | Wrong host surface for this Cursor/Claude-disciplined meta-repo |
| **agentmemory** | Broad MCP memory (many tools) | Node + iii-engine daemon; 50+ MCP tools | **Refuse** (dep) | Daemon/tool sprawl fights look-first, LOC bar, single tip writer |
| **context-mode** | Sandbox tool output + forced routing | Node; **ELv2** license; deep hooks | **Refuse** | ELv2 + routing hooks collide with agent policy / OSS posture |
| **prime-agent** / **open-swe** / **deepagents** as default runtime | Replace/compose coding agent host | TS/Python agent platforms | **Refuse** (v1 product) | Category error: do not swap our Cursor/CI constitution for another harness |
| **mem0** / **letta** | Generic agent memory platforms | Heavier productized stacks | **Defer** | Valid ≥1k★/push; prefer thinner Spike (headroom) or in-repo ledger first |
| **CompactionRL** / vendor mend SaaS | Trainable compact / commercial mend | Weights / vendor | **Refuse** | No model zoo; Unknown vendor SoR |

**Ranking for “watch findings → research backlog without context bloat” (this product):**

1. **Embody** react-doctor *pattern* + existing sensors → ledger → backlog  
2. **Embody/Adopt** condenser *pipeline* + cycle reset (STK4) — LLM summarize optional only  
3. **Spike** headroom for bulky CI/sensor dumps — never fail_under  

### 5.2 Stance summary (what Approve locks)

| Choice | Stance |
| --- | --- |
| Sensor-first watch; findings ledger outside chat | **Embody** |
| Rotating focus; ResearchPlanAssignOps; watch≠fixer; static-first refactor; cycle reset | **Adopt** (process) |
| Thin in-repo ledger as memory default | **Adopt default** |
| headroom / loopx-as-projection / gh-aw proposer | **Spike** (post-Approve) |
| claude-mem / magic-context / mem0 / letta | **Defer** |
| agentmemory dep; context-mode; prime-agent/open-swe as host; LLM-judge/oracle; CompactionRL; auto-PR factory | **Refuse** |

## 6. Spec decisions (STK1–STK10) — Approved E-STK0

| ID | Decision |
| --- | --- |
| **STK1** | A **watch agent** may propose findings + research areas; it must **not** write oracle SoT (`coverage.xml`, fail_under, size/complexipy caps) |
| **STK2** | Findings SoR = **structured ledger** (JSON/SARIF/markdown table under `docs/research/` or CI artifact) + pointer into `quality-backlog.md` — never raw chat |
| **STK3** | Each watch cycle picks **one focus domain** (or one backlog ID) via rotating/cache policy; default budget ≤20–30 min wall or fixed tool-call cap |
| **STK4** | Between cycles, context must **reset** to: system + domain map Read receipt + compact ledger projection + current focus — no cumulative trajectory |
| **STK5** | Prefer **deterministic sensors** for detect; LLM only for *ranking / explaining / drafting research questions* when sensors already fired |
| **STK6** | Adoption path = **Evidenced research memo → Spec gate → Implement** (principal-SE); watch agent stops at memo/backlog draft unless explicitly Spec’d to open draft PRs |
| **STK7** | Fixer agents (if any) use **event-passed** handoffs + static-first repair; no shared megacontext with the watcher |
| **STK8** | Memory default = **thin in-repo ledger**. Optional Spike order: **headroom** (compress) → **loopx** (handoffs projecting from backlog) → **gh-aw proposer**. **Defer** claude-mem/mem0/letta; **Refuse** agentmemory dep + context-mode (ELv2) |
| **STK9** | Suite-stalking remains **E-RUN sensors**; E-STK does not reopen D3/D8/D9 refuses without a new Spec |
| **STK10** | Refuse: chat dumps as SoT; LLM as 98.7 proof; GH trees **&lt;1000★** or **no push in 14 days** as implement SoR; forever-grandfather of watch noise; parallel tip thrash from auto-PRs |

---

## 7. Adversarial checklist

- [x] Can the watch agent inflate context by re-attaching full prior run logs? — **Mitigated by STK4** (cycle reset) + **headroom/context-mode**-shaped compression of tool output; refuse transcript SoT.
- [x] Does a finding mutate fail_under / baseline JSON without Spec? — **Forbidden by STK1**; sensors may *report*, never rewrite floors.
- [x] Is “wrong framework” advice grounded in arXiv+GitHub tiers or vibes? — **STK5–STK6** + GH SoR bar (≥1k★ + 14-day push); vibes → research question only.
- [x] Does rotating focus actually revisit (10% bucket) or starve domains? — **STK3** adopts gh-aw 60/30/10-style cache; spike must measure revisit rate.
- [x] Are reproduction tests (ReProAgent-shaped) required before risky refactors? — **Adopt for high-risk**; not every finding — Spec in E-STK1 when fixer lands.
- [x] Cloud/Cursor: does watch rely on `sessionStart`? — **No** (DOC9); use scheduled/CI + `beforeSubmitPrompt` / inject map.

---

## 8. Epic sketch (fresh-chat ready) — E-STK0 Spec → E-STK1 Implement

| Field | Content |
| --- | --- |
| **Epic goal** | Spec a stalker-shaped watch loop that surfaces actionable research/refactor opportunities from sensors + focused LLM judgment **without** context accumulation or oracle dilution |
| **STK0-1** | Approve **STK1–STK10** in this memo | Acceptance: `spec_gate: APPROVED E-STK0` |
| **STK0-2** | Map sensors → finding schema (Embody path; not a product Spike) | Exit: ≤1-page JSON/markdown schema |
| **STK0-3** | Spike **headroom** only: compress bulky CI/sensor dumps into ledger fields | Exit: go/no-go; never gate; LOC/complexipy impact |
| **STK0-4** | Spike **loopx**-shaped handoff **projected from** `quality-backlog` (no dual tip) | Exit: one-page schema; dual-SoT refuse |
| **STK0-5** | Optional Spike: gh-aw **proposer** workflow (discussions/issues only) | Exit: no write to SoT paths; local gates remain |
| **STK1-1** (after Approve) | Implement ledger writer + rotating focus (in-repo) | Acceptance: STK4 reset; claims green; LOC ≤225 |
| **STK1-2** | Presenter: findings → backlog stub / research question template | Acceptance: draft only; no auto-merge |
| **Invariants** | fail_under 98.7; complexipy ≤5; LOC ≤225; no utils/; E-RUN refuses intact; GH SoR ≥1k★ **and** 14-day push |

**Ordering:** Do **not** start E-STK1 while E-DOC1 or E-CQL1 owns the tip unless this becomes the single Active stream.

---

## 9. Better choices earlier

| Debt | Better earlier |
| --- | --- |
| Soft “check tool-quirks / backlog” without a findings projection | Thin in-repo ledger + cycle reset (Focus/CAT); optional ≥1k★ memory |
| Suite stalker research bundled with LLM flake triage | Sensor-only first (E-RUN0 got this right) |
| Continuous improvement = unbounded agent chat | gh-aw rotating focus + causal chain to Spec |
| Citing immature GH (&lt;1k★) as “the” memory/health product | arXiv for algorithms; ≥1k★ or in-repo for implement |
| Citing high★ but **stale tips** (&gt;14 days without push) | Re-fetch `pushed_at`; drop from implement SoR |

---

## 10. Sources (quick index)

- arXiv: [2606.25514](https://arxiv.org/abs/2606.25514), [2607.05378](https://arxiv.org/abs/2607.05378), [2607.09123](https://arxiv.org/abs/2607.09123), [2608.00924](https://arxiv.org/abs/2608.00924), [2608.02974](https://arxiv.org/abs/2608.02974), [2601.07190](https://arxiv.org/abs/2601.07190), [2512.22087](https://arxiv.org/abs/2512.22087), [2605.09998](https://arxiv.org/abs/2605.09998) (Continual Harness), [2606.12329](https://arxiv.org/abs/2606.12329) (algorithm only)
- GitHub SoR (≥1k★ + 14-day push): lean — [claude-mem](https://github.com/thedotmack/claude-mem), [headroom](https://github.com/headroomlabs-ai/headroom), [agentmemory](https://github.com/rohitg00/agentmemory), [context-mode](https://github.com/mksglu/context-mode), [loopx](https://github.com/huangruiteng/loopx), [magic-context](https://github.com/cortexkit/magic-context); watch/act — [prime-agent](https://github.com/PrimeIntellect-ai/prime-agent), [deepagents](https://github.com/langchain-ai/deepagents), [open-swe](https://github.com/langchain-ai/open-swe), [react-doctor](https://github.com/millionco/react-doctor), [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent), [OpenHands](https://github.com/All-Hands-AI/OpenHands), [gh-aw](https://github.com/github/gh-aw); also mem0 / letta
- GitHub **refused** as SoR (&lt;1k★): [riponcm/projectmem](https://github.com/riponcm/projectmem), [Acquarts/ai-repo-health-agent](https://github.com/Acquarts/ai-repo-health-agent)
- In-repo: suite-stalking design; research 08; quality-backlog P7/P15; E-DOC1 domain map
