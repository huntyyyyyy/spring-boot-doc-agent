---
title: E-STK0 — Watch/stalker agents (findings → research → refactor) without context bloat
status: DRAFT Spec — pending Approve of STK1–STK10
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
spec_gate: DRAFT E-STK0 (2026-08-09) — STK1–STK10 pending Approve
---

# Principal memo: stalker-shaped watch agents (mid-2026)

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is there a 2026 pattern for agents that *watch* systems, surface bugs / inefficiencies / wrong frameworks / gaps, then drive research + refactor adoption? | **Yes.** Strongest native shape is **sensor findings → compact external memory → research memo / backlog → Spec → implement**, not a forever-growing chat. `[Evidenced]` |
| What maps to this repo’s “stalker”? | **Suite-stalking sensors (E-RUN)** already Embody the *watch* half for CI plateaus — deterministic junit / cascade clarity; LLM flake triage refused. Broader “framework/gap stalking” is a **separate meta-agent** that must not dilute oracle SoT. `[Confirmed]` |
| How do mid-2026 systems avoid context bloat? | Prefer **newer ≥1k★ harnesses with release cadence**: **agentmemory** (MCP + decay), **OpenHands** condensers, **Prime Agent** Continual Harness + compaction, **deepagents** / **open-swe** composition — plus arXiv compaction papers. `[Evidenced]` |
| Adopt for *this* product now? | **Spec-only (E-STK0).** Prefer **deterministic sensors + in-repo backlog**. GH SoR = **≥1000★** *and* prefer **created/accelerated 2025–2026 with tagged releases/CHANGELOG** over stagnant giants. |

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
2. Prefer **newer or recently accelerated** trees (created/rewritten **2025–2026**) with **tagged Releases and/or CHANGELOG** — not only legacy star count.
3. Below 1k★ → **Refuse as SoR** (arXiv may still Evidenced the algorithm).

### 3.0 Preferred GH SoR — newer, widely adopted, release cadence (fetched 2026-08-09)

| Repo | Created | ★ | Recent releases / changelog | Why it fits stalker + lean context |
| --- | --- | --- | --- | --- |
| [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) | 2026-02 | **≈26.8k** | `CHANGELOG.md`; tags through **v0.9.28** (2026-07); tip pushed 2026-08-09 | Coding-agent **persistent memory** via MCP; 4-tier consolidation + decay + auto-forget; self-hosted SQLite — preferred memory SoR vs sub-1k toys |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | 2026-05 | **≈10.7k** | **v0.7.0 / v0.7.1** (2026-08); Continual Harness ([arXiv:2605.09998](https://arxiv.org/abs/2605.09998)) | **Automatic compaction**, durable memories/skills, heartbeats/schedules, bounded autonomous mode + quality gates |
| [millionco/react-doctor](https://github.com/millionco/react-doctor) | 2026-02 | **≈14.3k** | npm tags **0.9.10–0.9.11** (2026-08-09); CI skill install | **Deterministic** scan → agent skill for self-correction; PR-diff gated findings — stalker *shape* (React-specific; pattern only here) |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 2025-07 | **≈27.6k** | **deepagents 0.7.4–0.7.5** + `deepagents-code` (2026-08) | Batteries-included harness; composition base for coding agents |
| [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) | 2025-05 | **≈10.5k** | Active tip 2026-08 | Async coding agent on Deep Agents; Linear/Slack/GitHub → draft PRs (*act* after findings) |
| [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | 2025-06 | **≈6.3k** | Active; supersedes heavy SWE-agent monorepo | Minimal fix-loop scaffold; leaner research baseline |
| [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | 2024-03 | **≈83.5k** | **v1.9–v1.12** in one week (2026-08-03→08-07) | Production scaffold; **event log + LLMSummarizingCondenser** — reference lean-context *implementation* |
| [github/gh-aw](https://github.com/github/gh-aw) | 2025-08 | **≈4.9k** | Official continuous-improvement workflows | Rotating Quality Improver + cache memory; ResearchPlanAssignOps |

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
| **Remember** | **agentmemory** / OpenHands condenser / Prime Continual Harness **or** thin in-repo ledger; rotating cache (gh-aw) | Append-only chat as SoT; sub-1k GH memory toys as deps |
| **Judge** | Rubric pivot (`icat` arXiv); pre-action warnings from **our** ledger | Soft “remember to check backlog” only |
| **Propose** | Findings → discussion/memo → Plan (gh-aw ResearchPlanAssignOps) | Silent auto-refactor on main |
| **Act** | Short-horizon fixer with event messages + compaction (`icat`, Focus, RefactorAssist static-first) | Shared megacontext explorer+fixer forever |
| **Close loop** | Backlog Archive + session-log only when steering claims move | Raw trajectories committed as research |

---

## 5. Embody / Adopt / Refuse (this Python CLI / meta-repo)

| Choice | Stance | Why here |
| --- | --- | --- |
| Sensor-first watch (junit durations, claims, size, CodeQL, façade poke) | **Embody** | Already SoT; matches E-RUN / constitution |
| Findings ledger outside chat (compact projection → backlog/memo) | **Embody** | DOC refuse chat dumps; arXiv Memory-as-Governance idea without weak GH |
| Rotating focus areas + revisit budget (gh-aw Quality Improver 60/30/10) | **Adopt** | Stops “always scan everything”; **≥1k★** official stack |
| ResearchPlanAssignOps (findings → Spec → tickets → PR) | **Adopt** | Matches principal-SE skill Phase A–C |
| Separate watch vs fix agents; event messages not shared dump | **Adopt** | `icat-agent` Jun 2026 (paper) |
| Active compaction between watch cycles (Focus / CAT-shaped) | **Adopt** (process) | Do **not** train CompactionRL in-tree |
| Static-first then agentic repair for refactors | **Adopt** | RefactorAssist Aug 2026 |
| **agentmemory** (or Mem0) as optional memory Spike | **Adopt spike** | ≥1k★ + CHANGELOG/releases; prefer self-hosted; no mandatory cloud telemetry |
| OpenHands condenser / Prime compaction patterns | **Adopt** (process) | Copy *ideas* into cycle reset — do not vend whole monorepo |
| Thin in-repo event ledger (no third-party memory product) | **Adopt default** | Fits claims/session-log contracts; LOC ≤225 modules |
| react-doctor-style deterministic scan → skill | **Adopt pattern** | Sensors first; React-specific product refused for this Python CLI |
| gh-aw continuous auto-PR factory as default | **Refuse** (v1) | Tip thrash / Spec bypass; remix later |
| `projectmem` GH (<1k★) / `ai-repo-health-agent` (0★) as SoR | **Refuse** | Star floor; paper ideas may inform design without the trees |
| Vendor mend SaaS | **Refuse** | Unknown maturity |
| LLM flake triage / LLM-judge as oracle | **Refuse** | E-RUN D8 Defer; synthesis refuse |
| CompactionRL / weight training as product dep | **Refuse** | Research only; no model zoo |

---

## 6. Spec decisions (STK1–STK10) — pending Approve

| ID | Decision |
| --- | --- |
| **STK1** | A **watch agent** may propose findings + research areas; it must **not** write oracle SoT (`coverage.xml`, fail_under, size/complexipy caps) |
| **STK2** | Findings SoR = **structured ledger** (JSON/SARIF/markdown table under `docs/research/` or CI artifact) + pointer into `quality-backlog.md` — never raw chat |
| **STK3** | Each watch cycle picks **one focus domain** (or one backlog ID) via rotating/cache policy; default budget ≤20–30 min wall or fixed tool-call cap |
| **STK4** | Between cycles, context must **reset** to: system + domain map Read receipt + compact ledger projection + current focus — no cumulative trajectory |
| **STK5** | Prefer **deterministic sensors** for detect; LLM only for *ranking / explaining / drafting research questions* when sensors already fired |
| **STK6** | Adoption path = **Evidenced research memo → Spec gate → Implement** (principal-SE); watch agent stops at memo/backlog draft unless explicitly Spec’d to open draft PRs |
| **STK7** | Fixer agents (if any) use **event-passed** handoffs + static-first repair; no shared megacontext with the watcher |
| **STK8** | Memory default = **thin in-repo ledger**; optional Spike prefers **agentmemory** (or Mem0) — ≥1k★ + active Releases/CHANGELOG, local-first — **never** sub-1k GH memory repos |
| **STK9** | Suite-stalking remains **E-RUN sensors**; E-STK does not reopen D3/D8/D9 refuses without a new Spec |
| **STK10** | Refuse: chat dumps as SoT; LLM as 98.7 proof; GH trees **&lt;1000★** as implement SoR; forever-grandfather of watch noise; parallel tip thrash from auto-PRs |

---

## 7. Adversarial checklist

- [ ] Can the watch agent inflate context by re-attaching full prior run logs?
- [ ] Does a finding mutate fail_under / baseline JSON without Spec?
- [ ] Is “wrong framework” advice grounded in arXiv+GitHub tiers or vibes?
- [ ] Does rotating focus actually revisit (10% bucket) or starve domains?
- [ ] Are reproduction tests (ReProAgent-shaped) required before risky refactors?
- [ ] Cloud/Cursor: does watch rely on `sessionStart`? (DOC9 — must not)

---

## 8. Epic sketch (fresh-chat ready) — E-STK0 Spec → E-STK1 Implement

| Field | Content |
| --- | --- |
| **Epic goal** | Spec a stalker-shaped watch loop that surfaces actionable research/refactor opportunities from sensors + focused LLM judgment **without** context accumulation or oracle dilution |
| **STK0-1** | Approve **STK1–STK10** in this memo | Acceptance: `spec_gate: APPROVED E-STK0` |
| **STK0-2** | Spike: map existing sensors (suite_timing, claims, size, CodeQL, poke) → finding schema | Exit: one JSON schema draft ≤1 page |
| **STK0-3** | Spike: thin in-repo ledger vs **agentmemory** / Mem0 (≥1k★, changelog) optional MCP — **exclude** projectmem GH | Exit: Adopt default + optional Spike with LOC/complexipy impact |
| **STK1-1** (after Approve) | Implement ledger writer + rotating focus CLI/hook | Acceptance: cycle resets context; claims green; LOC ≤225 |
| **STK1-2** | Presenter: findings → backlog stub / research question template | Acceptance: no auto-merge; draft only |
| **Invariants** | fail_under 98.7; complexipy ≤5; LOC ≤225; no utils/; E-RUN refuses intact; GH SoR ≥1k★ |

**Ordering:** Do **not** start E-STK1 while E-DOC1 or E-CQL1 owns the tip unless this becomes the single Active stream.

---

## 9. Better choices earlier

| Debt | Better earlier |
| --- | --- |
| Soft “check tool-quirks / backlog” without a findings projection | Thin in-repo ledger + cycle reset (Focus/CAT); optional ≥1k★ memory |
| Suite stalker research bundled with LLM flake triage | Sensor-only first (E-RUN0 got this right) |
| Continuous improvement = unbounded agent chat | gh-aw rotating focus + causal chain to Spec |
| Citing immature GH (&lt;1k★) as “the” memory/health product | arXiv for algorithms; ≥1k★ or in-repo for implement |

---

## 10. Sources (quick index)

- arXiv: [2606.25514](https://arxiv.org/abs/2606.25514), [2607.05378](https://arxiv.org/abs/2607.05378), [2607.09123](https://arxiv.org/abs/2607.09123), [2608.00924](https://arxiv.org/abs/2608.00924), [2608.02974](https://arxiv.org/abs/2608.02974), [2601.07190](https://arxiv.org/abs/2601.07190), [2512.22087](https://arxiv.org/abs/2512.22087), [2605.09998](https://arxiv.org/abs/2605.09998) (Continual Harness), [2606.12329](https://arxiv.org/abs/2606.12329) (algorithm only)
- GitHub SoR (newer / active releases, ≥1k★): [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) (≈26.8k), [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) (≈10.7k), [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) (≈27.6k), [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) (≈10.5k), [millionco/react-doctor](https://github.com/millionco/react-doctor) (≈14.3k), [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) (≈6.3k), [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) (≈83.5k), [github/gh-aw](https://github.com/github/gh-aw) (≈4.9k); also [mem0ai/mem0](https://github.com/mem0ai/mem0), [letta-ai/letta](https://github.com/letta-ai/letta)
- GitHub **refused** as SoR (&lt;1k★): [riponcm/projectmem](https://github.com/riponcm/projectmem), [Acquarts/ai-repo-health-agent](https://github.com/Acquarts/ai-repo-health-agent)
- In-repo: suite-stalking design; research 08; quality-backlog P7/P15; E-DOC1 domain map
