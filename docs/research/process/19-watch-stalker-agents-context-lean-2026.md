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
  - treat commercial “mend” SaaS or low-star one-shots as merge SoR
  - schedule CompactionRL / weight training as a product dependency
spec_gate: DRAFT E-STK0 (2026-08-09) — STK1–STK10 pending Approve
---

# Principal memo: stalker-shaped watch agents (mid-2026)

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is there a 2026 pattern for agents that *watch* systems, surface bugs / inefficiencies / wrong frameworks / gaps, then drive research + refactor adoption? | **Yes.** Strongest native shape is **sensor findings → compact external memory → research memo / backlog → Spec → implement**, not a forever-growing chat. `[Evidenced]` |
| What maps to this repo’s “stalker”? | **Suite-stalking sensors (E-RUN)** already Embody the *watch* half for CI plateaus — deterministic junit / cascade clarity; LLM flake triage refused. Broader “framework/gap stalking” is a **separate meta-agent** that must not dilute oracle SoT. `[Confirmed]` |
| How do mid-2026 systems avoid context bloat? | **(1)** Event-sourced / projected memory outside the window (`projectmem`). **(2)** Event-passed multi-agent scaffolds (`icat-agent`) instead of shared megacontext. **(3)** Active compaction / “context as tool” (`Focus`, CompactionRL, CAT). **(4)** Rotating focus + cache memory (GitHub Agentic Workflows Quality Improver). `[Evidenced]` |
| Adopt for *this* product now? | **Spec-only (E-STK0).** Implement only after E-DOC1 Archive and without blocking E-CQL1 if that stream is next. Prefer **deterministic sensors + backlog projection** over autonomous PR factories. |

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

### 3.1 Watch → findings → adopt (stalker-shaped)

| Source | Date | Claim | Tier | Stars / note |
| --- | --- | --- | --- | --- |
| [GitHub Agentic Workflows — Continuous Improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/) | 2026-01-13 | Daily/rotating **Quality Improver** + dependency/type agents; **cache memory** (60% custom / 30% standard / 10% revisit); output = Discussions → Plan → issues → PRs (**ResearchPlanAssignOps**), not infinite chat | Evidenced | Official gh-aw / GitHub Next blog (slightly before Jun window; still the clearest *native* continuous-watch recipe) |
| [projectmem — arXiv:2606.12329](https://arxiv.org/abs/2606.12329) · [github.com/riponcm/projectmem](https://github.com/riponcm/projectmem) | 2026-06 | Append-only **event log** (issues/attempts/fixes/decisions) → deterministic **projected summaries** via MCP; **pre-action gate** (“you tried this — it failed”) = Memory-as-Governance | Evidenced | **579★** (fetched 2026-08-09); MIT; local-first |
| [icat-agent — arXiv:2606.25514](https://arxiv.org/abs/2606.25514) | 2026-06 | Decentralized Explorer / Validator / Patch Editor; **event-based message passing** replaces shared context; rubric pivots workflow; cost ↓ vs multi-agent Claude Code baseline on SWE-bench | Evidenced | Strong anti-bloat scaffold for *fix* half |
| [ai-repo-health-agent](https://github.com/Acquarts/ai-repo-health-agent) | 2026 (active) | On-demand repo health: EOL deps, deprecated APIs, modernization; **one issue per repo**; deterministic auditors + LLM report; verify versions against PyPI/npm/endoflife | Evidenced | **0★** — pattern useful; do **not** treat as mature SoR |
| [RefactorAssist — arXiv:2608.00924](https://arxiv.org/abs/2608.00924) | 2026-08 | LLM refactor fails often (hallucination / rename / incompleteness…); **static repair first**, then test-guided agentic repair → high cumulative pass | Evidenced | Guides *how* to adopt refactorations safely |
| [ReProAgent — arXiv:2607.09123](https://arxiv.org/abs/2607.09123) | 2026-07 | Multi-stage localization → root cause → test plan → generation for **reproduction tests** from issues | Evidenced | Useful when findings need executable proof |
| [ConFL — arXiv:2608.02974](https://arxiv.org/abs/2608.02974) | 2026-08 | Hierarchy-guided concurrent fault localization; structured KB + DSL — focused reasoning without deep call-chain dumps | Evidenced | ISSTA 2026; niche (concurrency) |

### 3.2 Context non-bloat (algorithms / scaffolds)

| Source | Date | Claim | Tier |
| --- | --- | --- | --- |
| [Focus / Active Context Compression — arXiv:2601.07190](https://arxiv.org/abs/2601.07190) | 2026-01 | Agent-controlled `start_focus` / `complete_focus`; prune raw history into persistent Knowledge block; **sawtooth** context; ~22.7% tokens @ equal accuracy (N=5); aggressive prompting required | Evidenced |
| [CompactionRL — arXiv:2607.05378](https://arxiv.org/abs/2607.05378) | 2026-07 | Trainable compaction inside RL rollouts; summary + short tail resume; SWE-bench / Terminal-Bench gains on open GLM models | Evidenced |
| [CAT — Context as a Tool — arXiv:2512.22087](https://arxiv.org/abs/2512.22087) | 2025-12 | Context workspace \(Q, M(t), I^{(k)}(t)\); compression as **callable tool**; SWE-Compressor 57.6% SWE-Bench-Verified (reported) | Evidenced (just outside Jun window; algorithm still current) |
| ContextPilot (Gao et al., PDF) | 2026 | Explorer/generator split + memory summaries for repo-scale context | Evidenced (secondary PDF; prefer arXiv ID when indexed — mark **Unknown** if ID missing) |

### 3.3 Orientation / caution

| Source | Note | Tier |
| --- | --- | --- |
| Truemend (truemend.ai) | Marketing “lives in repo / mends debt”; AST claims — useful as **category existence**, not SoR | Unknown (vendor) |
| Agent Audit — arXiv:2603.22853 | Security scan for *agent apps* (SAST/SARIF) — adjacent, not general stalker | Evidenced |
| DeepWiki | Cartography only for unfamiliar GH trees | Confirmed process (steering 00) |

---

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
| **Remember** | Append-only events + *projected* summaries (`projectmem`); rotating cache (gh-aw) | Append-only chat as SoT |
| **Judge** | Pre-action gate / rubric pivot (`projectmem`, `icat`) | Soft “remember to check backlog” only |
| **Propose** | Findings → discussion/memo → Plan (ResearchPlanAssignOps) | Silent auto-refactor on main |
| **Act** | Short-horizon fixer with event messages + compaction (`icat`, Focus, RefactorAssist static-first) | Shared megacontext explorer+fixer forever |
| **Close loop** | Backlog Archive + session-log only when steering claims move | Raw trajectories committed as research |

---

## 5. Embody / Adopt / Refuse (this Python CLI / meta-repo)

| Choice | Stance | Why here |
| --- | --- | --- |
| Sensor-first watch (junit durations, claims, size, CodeQL, façade poke) | **Embody** | Already SoT; matches E-RUN / constitution |
| Findings ledger outside chat (event log → compact projection → backlog/memo) | **Embody** | `projectmem` Memory-as-Governance + DOC refuse chat dumps |
| Rotating focus areas + revisit budget (Quality Improver 60/30/10) | **Adopt** | Stops “always scan everything” context/cost blowups |
| ResearchPlanAssignOps (findings → Spec → tickets → PR) | **Adopt** | Matches principal-SE skill Phase A–C |
| Separate watch vs fix agents; event messages not shared dump | **Adopt** | `icat-agent` Jun 2026 |
| Active compaction between watch cycles (Focus / CAT-shaped tools) | **Adopt** (process) | Do **not** train CompactionRL in-tree |
| Static-first then agentic repair for refactors | **Adopt** | RefactorAssist Aug 2026 |
| gh-aw continuous auto-PR factory as default | **Refuse** (v1) | Tip thrash / Spec bypass risk; remix later as optional |
| Vendor mend SaaS / 0★ health agents as SoR | **Refuse** | Pattern ok; maturity Unknown |
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
| **STK8** | Optional MCP memory (`projectmem`-shaped) is **Adopt spike** — local-first, no telemetry; must not replace claims/session-log contracts |
| **STK9** | Suite-stalking remains **E-RUN sensors**; E-STK does not reopen D3/D8/D9 refuses without a new Spec |
| **STK10** | Refuse: chat dumps as SoT; LLM as 98.7 proof; forever-grandfather of watch noise without Archive; parallel tip thrash from auto-PRs |

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
| **STK0-3** | Spike: `projectmem` MCP vs thin in-repo event log | Exit: Adopt/Defer with LOC/complexipy impact |
| **STK1-1** (after Approve) | Implement ledger writer + rotating focus CLI/hook | Acceptance: cycle resets context; claims green; LOC ≤225 |
| **STK1-2** | Presenter: findings → backlog stub / research question template | Acceptance: no auto-merge; draft only |
| **Invariants** | fail_under 98.7; complexipy ≤5; LOC ≤225; no utils/; E-RUN refuses intact |

**Ordering:** Do **not** start E-STK1 while E-DOC1 or E-CQL1 owns the tip unless this becomes the single Active stream.

---

## 9. Better choices earlier

| Debt | Better earlier |
| --- | --- |
| Soft “check tool-quirks / backlog” without a findings projection | Event ledger + pre-action gate (`projectmem`) |
| Suite stalker research bundled with LLM flake triage | Sensor-only first (E-RUN0 got this right) |
| Continuous improvement = unbounded agent chat | gh-aw rotating focus + causal chain to Spec |

---

## 10. Sources (quick index)

- arXiv: [2606.12329](https://arxiv.org/abs/2606.12329), [2606.25514](https://arxiv.org/abs/2606.25514), [2607.05378](https://arxiv.org/abs/2607.05378), [2607.09123](https://arxiv.org/abs/2607.09123), [2608.00924](https://arxiv.org/abs/2608.00924), [2608.02974](https://arxiv.org/abs/2608.02974), [2601.07190](https://arxiv.org/abs/2601.07190), [2512.22087](https://arxiv.org/abs/2512.22087)
- GitHub: [riponcm/projectmem](https://github.com/riponcm/projectmem) (579★), [gh-aw continuous improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/), [Acquarts/ai-repo-health-agent](https://github.com/Acquarts/ai-repo-health-agent) (0★)
- In-repo: suite-stalking design; research 08; quality-backlog P7; E-DOC1 domain map
