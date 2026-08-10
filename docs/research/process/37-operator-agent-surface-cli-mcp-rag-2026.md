---
title: E-OAS0 — Operator/agent surface (CLI grade + MCP + structured retrieval)
status: DRAFT Spec — pending Approve of OAS1–OAS14
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine + thin MCP adapter + future RAG-shaped retrieval
related:
  - docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md
  - docs/research/process/25-tip-grounding-mcp-2026.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/process/28-local-stalker-telemetry-etl-2026.md
  - docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
  - docs/research/process/39-cli-operator-problem-classes-2026-08-10.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/process/local-grading-pack.md
  - src/doc_engine/query/mcp_tools.py
  - adapters/mcp/server.py
  - scripts/ci/run_local_grading_pack.sh
do_not:
  - implement before Spec Approve
  - make rich / OTel / embeddings CI or citation SoT
  - rewrite every scripts/ci façade to Typer in one tip
  - add MCP write/codegen tools
  - treat vector RAG as Stage-0 citation replacement
  - treat MCP/agents as unattended merge authority (human review remains floor)
spec_gate: DRAFT E-OAS0 (2026-08-10) — OAS1–OAS15 pending Approve
depends_on: E-UX0 (landed); E-GND0 still DRAFT/demoted — this memo does not unblock GND1
gh_sor_bar: "≥10000★ for new external SoR; Confirmed pins Embody-continue"
---

# Principal memo: operator/agent surface (CLI ↔ MCP ↔ retrieval)

**Question.** The local grading runner is thin bash with opaque logs; operators
hit venv/PATH/Artifactory failures that look like “no output.” Meanwhile
doc-engine is already a **read-only MCP + Stage-0 query** product and will grow
toward richer agent/RAG-shaped surfaces. What high-bar architecture gives
**modern CLI + MCP + retrieval observability** without violating existing
Refuse lines (rich-as-CI-SoT, OTel-as-tip-SoT, embedding-as-citation-SoT) — and
without drifting into **unattended AI adoption**?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**Human-review floor (non-negotiable).** Agents/MCP/RAG surfaces assist;
they do **not** replace Spec Approve, operator-reviewed `--write`, certification
gates, or merge SoR. Continuous human review is the bare minimum — not a
stretch goal. Full autonomous “AI runs the plant and merges” is **Refuse**.

---

## 0. Live operator grade (2026-08-10) — Confirmed

| Signal | Finding | Grade |
| --- | --- | --- |
| `doctor` | `prefix=C:\Python311`, npm `ast-grep`, **no** `.venv` | **Fail** toolchain hygiene |
| `artifactory_*` | unset | Expected for P1 exit 3 |
| `p1-plant-profile.log` | JSON `exit_code=3`, `remeasure_ok=true`, checkout OK | **Pass** preflight semantics |
| `p3-run-plant-ocs.log` | `Python was not found` (WindowsApps `python3` stub); EXIT 49 | **Fail** — plant invoked without venv/`python3` SoR |
| Operator invocations | `python …cmd`, `python …sh` | **Fail** UX affordance (NoFAQ class) |

Immediate remediation (no Spec needed): `source .venv/Scripts/activate`, set
Artifactory for P3, never `python` the `.cmd`/`.sh`. The rest of this memo is
the **product-bar** fix so the next surface (MCP/RAG) does not repeat opaque logs.

---

## 1. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | Shared **RunContext** ports + dual sinks (headline + JSONL/JSON receipt); Stage-0 / `context_packet` as structured retrieval SoR; MCP library `dispatch_tool` SoR; stderr-only on stdio MCP `[Evidenced]`; **human Spec/operator review as merge floor** `[Confirmed]` |
| **Adopt** | clig.dev human+machine dual output `[Evidenced]`; actionable errors / next-step remediation `[Evidenced]` arXiv CLI UX + NoFAQ; Typer **only** for a thin local `doc-engine grade` façade (≥10k★) `[Evidenced]`; optional TTY polish behind `NO_COLOR` — never CI SoT; **campaign** OS×shell matrix for grade smoke `[Evidenced]` |
| **Refuse** | `rich` as CI/merge SoT (E-UX0 U7) `[Confirmed]`; OTel as tip SoT (E-TEL) `[Confirmed]`; embedding/vector as citation SoT `[Confirmed]`; MCP write/codegen tools `[Confirmed]`; boiling all `scripts/ci` into one megacli; Fire / untyped CLI generators; **unattended AI merge / “full AI adoption”** `[Confirmed]`; **one product that emulates all OS+terminals+phones as CLI SoT** `[Evidenced]` — that category does not exist as honest merge proof |

**Architecture sketch (OCP):** high-level wrapper → context modules → step
strategies → sinks. Same context object feeds CLI grade, MCP tool calls, and
(later) retrieval eval harnesses.

---

## 2. Product map — what already ships vs modern bar

### 2.1 Shipped today `[Confirmed]`

- Stage-0 query library + envelopes + `context_packet` (`src/doc_engine/query/`)
- Thin MCP stdio adapter (`adapters/mcp/server.py`) — **no** FastMCP/SDK pin
- `doc-engine query` / `certification verify` (argparse)
- Local receipts: `pre_pr-receipt.json`, stalker telemetry, vacuity ledger
- Bash grading pack + hermetic tests (`scripts/ci/run_local_grading_pack.*`)

### 2.2 Modern MCP / RAG bar (external) `[Evidenced]`

| Capability | External SoR | This repo stance |
| --- | --- | --- |
| Stdio ≠ stdout logs | FastMCP / MCP walkthroughs — log to **stderr** | **Embody** — already required; harden grade+MCP shared logger |
| Client-visible structured logs | FastMCP `ctx.info(..., extra={})` | **Adopt pattern** via receipt events; SDK pin still Deferred (GND9) |
| Tools callable without transport | FastMCP testing doctrine | **Embody** — keep `dispatch_tool` library SoR |
| Lean tool returns / budgets | FastMCP guidance; our `rank.py` | **Embody** continue |
| RAG observability (OTel / LangSmith) | LlamaIndex / LangChain OTel stacks | **Refuse as tip SoT**; optional future **port** only after Spec |
| Vector RAG platforms | LlamaIndex/LangChain ecosystems | **Refuse as citation SoT**; Embody **partial RAG** = Stage-0 + packets |
| Human/machine dual CLI | [clig.dev](https://clig.dev/) (≥ community SoR) | **Adopt** |
| Actionable CLI errors | arXiv CLI UX / HotOS shell future / NoFAQ | **Adopt** remediation next-actions |

### 2.3 Gaps vs that bar `[Confirmed]` / `[Unknown]`

| Gap | Tier |
| --- | --- |
| Grade runner lacks structured receipt + remediation | Confirmed |
| Doctor does not fail-closed on wrong interpreter/venv | Confirmed |
| No shared RunContext across CLI grade and MCP | Confirmed |
| MCP lacks resources/prompts/sampling; thin tools-only | Confirmed |
| Official MCP SDK / FastMCP | Explicit Defer (GND9) |
| Hybrid BM25 / materialized index | Unknown product (E-Q3 spikes) |
| Hosted HTTP MCP + auth | Unknown — out of v1 |

---

## 3. Research evidence (tiers)

| Claim | Tier | Source |
| --- | --- | --- |
| CLI should be human-first with machine-readable opt-in (JSON) | Evidenced | [clig.dev](https://clig.dev/) |
| Cryptic CLI errors are a top UX failure; remediation matters | Evidenced | arXiv CLI UX playbook strand (Google Cloud UXR 2605.31104); NoFAQ [1608.08219] |
| Shell lacks affordances; better state/error surfacing needed | Evidenced | HotOS “Future of the Shell” [2109.11016] |
| Log message readability = structure + information + wording | Evidenced | arXiv 2308.08836 |
| Agent observability wants structured multi-surface events | Evidenced | AgentTrace [2602.10133] (pattern only — not a dep) |
| Typer ≥10k★; Rich ≥10k★; Click ≥10k★; structlog high but <10k★ | Evidenced | GitHub (Typer ~19.9k, Rich ~57k, Click ~17.6k, structlog ~4.9k) |
| MCP stdio: never print to stdout | Evidenced | FastMCP / MCP server guides |
| This repo refuses rich as CI SoT; OTel as tip SoT; embedding citation SoT | Confirmed | E-UX0; E-TEL / synthesis; process/04 + synthesis |
| Query MCP + packets already embody partial RAG | Confirmed | `query/`, `adapters/mcp`, SEARCH.md |
| E-GND0 tip-grounding still DRAFT/demoted | Confirmed | quality-backlog P22 |

---

## 4. Proposed architecture (wrapper + context modules)

```text
                    +------------------+
  human / IDE       |  grade CLI       |  (Typer or argparse thin façade)
  MCP host          |  mcp adapter     |  (stdio; stderr logs only)
  future RAG eval   |  eval harness    |
                    +--------+---------+
                             | builds
                    +--------v---------+
                    |  RunContext      |  immutable ports:
                    |  - toolchain     |  interpreter, venv, pins
                    |  - plant         |  checkout, artifactory, expectations
                    |  - artifacts     |  run_dir / DOC_ENGINE_ROOT
                    |  - policy        |  plant=fixture|ocs, profile
                    +--------+---------+
                             |
              +--------------+--------------+
              v              v              v
         StepStrategy   ReceiptSink    HeadlineSink
         (p1,p2,p3,…)   JSONL/JSON     PASS/FAIL + next
```

**Scalability:** new campaign steps = new strategy modules (≤225 LOC each), not
new bash megascripts. MCP tools and CLI steps share the same context builders
so “doctor” findings appear identically in grade receipts and MCP error envelopes.

**Logging quality bar (OAS):**

1. Every step emits: `step_id`, `status`, `exit_code`, `duration_ms`, `next_actions[]`
2. Headline on stderr/TTY; full event to `local-runs/logs/<run_id>.jsonl`
3. Subprocess stdout/stderr captured as artifacts, not silent overwrite
4. Doctor is a **hard gate** before campaign steps that need the toolchain

---

## 5. Decisions pending Approve (OAS1–OAS16)

| ID | Decision |
| --- | --- |
| **OAS1** | Introduce shared `RunContext` ports (toolchain / plant / artifacts / policy) used by grade CLI and MCP paths |
| **OAS2** | Dual sink: headline + JSONL receipt; schema_versioned like `pre_pr-receipt` |
| **OAS3** | MCP stdio: all diagnostics on stderr; zero stdout outside JSON-RPC |
| **OAS4** | Doctor fail-closed: refuse grade/plant steps when interpreter is not venv or `ast-grep` pin path is wrong |
| **OAS5** | Actionable remediation strings for known failures (no-venv, python-on-cmd, Artifactory missing, WindowsApps python3 stub) |
| **OAS6** | Step strategies are OCP modules; bash remains a thin launcher or is replaced by `doc-engine grade` after Approve |
| **OAS7** | Typer **Adopt** only for local `doc-engine grade` (optional `[grade]` extra); do **not** rewrite all CI façades |
| **OAS8** | Rich **Refuse** as CI/merge dependency; optional local TTY only, honor `NO_COLOR` / non-TTY |
| **OAS9** | structlog **Defer** as hard pin (stars &lt;10k bar); prefer stdlib logging + JSONL events unless Spike proves need |
| **OAS10** | OTel **Refuse** as tip SoT; allow a future `TraceExporter` port behind Explicit Spec |
| **OAS11** | Retrieval SoR remains Stage-0 + `context_packet` (**Embody partial RAG**); Refuse embedding as citation SoT |
| **OAS12** | MCP write/codegen tools remain Refuse; GND tip tools stay on E-GND0 track (not this epic’s Implement) |
| **OAS13** | One tip stream: land grade surface first; do not parallel thrash GND Spec |
| **OAS14** | process/ domain already &gt;12 memos — this is a **synthesis** memo; reshape taxonomy later, do not add a third nesting level |
| **OAS15** | **Human review is the floor:** Spec Approve, operator-reviewed expectation `--write`, certification gates, and merge SoR stay human; MCP/agents are assistive only — Refuse unattended AI adoption as product policy |
| **OAS16** | **Shell/OS matrix:** Adopt a **campaign** GitHub Actions (or local) scenario matrix for grade smoke (`ubuntu`+bash; `windows`+bash/Git Bash; `windows`+`pwsh`; optional `cmd`); Refuse phone/device-farm and “universal OS emulator” as CLI merge SoT; macOS optional/campaign cost |

---

## 5b. Multi-OS / multi-terminal testing — what actually exists

**Short answer:** there is **no** single product that honestly emulates *all* OS × *all* terminals × phones for CLI merge proof. Browser/device farms (BrowserStack, AWS Device Farm) target **apps/browsers**, not Git Bash vs Admin PowerShell quoting.

| Approach | What it covers | Stance for doc-engine |
| --- | --- | --- |
| **GitHub Actions OS×shell jobs** (`ubuntu`/`windows`/`macos` × `bash`/`pwsh`/`powershell`/`cmd`) `[Evidenced]` | Real runners, real shells; Windows Git Bash = Git for Windows bash on `windows-latest` | **Adopt campaign** smoke for `doc-engine grade` / grading pack self-test |
| **Scenario matrix harness** (shell × launch × PATH × env) `[Evidenced]` e.g. github/gh-aw windows-cli-integration | Catches PATH/PATHEXT/`NO_COLOR`/quoting chaos | **Adopt pattern** for grade doctor + launcher |
| **VMs / Multipass / Vagrant / Windows Sandbox / Hyper-V** | Deeper Windows Admin vs user, corp images | **Optional operator** — not default CI (cost/non-hermetic) |
| **WSL2** | Linux-on-Windows; not a substitute for Git Bash or pwsh | Campaign only if work requires it |
| **Docker** | Linux userspace only — does **not** emulate PowerShell Desktop 5.1 or Git Bash | Useful for Linux CLI; Refuse as full Windows shell SoT |
| **Phone emulators / device farms** | Mobile UI | **Refuse** for this Python CLI product |

This repo today: **Confirmed** CI is Ubuntu + Python matrix only (`python-gates.yml`, `abi-tests.yml`) — no Windows/macOS shell matrix yet. That gap is real; the fix is OAS16 campaign jobs, not a fantasy universal emulator.

---

## 6. Epic sketch (fresh-chat ready)

### E-OAS0 — Spec (this memo) — **DRAFT**

Approve OAS1–OAS16.

### E-OAS1 — Implement grade surface (after Approve)

| Ticket | Acceptance |
| --- | --- |
| OAS1-1 | `RunContext` + doctor fail-closed; tests for venv / pin detection |
| OAS1-2 | JSONL receipt + headline for p1–p4 / hermetic-lite; remediation next_actions |
| OAS1-3 | `doc-engine grade` (or keep `.sh` calling Python module) — Windows Git Bash green |
| OAS1-4 | LOC ≤225 / complexipy ≤5 / no utils; claims OK; grading pack docs point at new entry |
| OAS1-5 | Human-review wording in grade/MCP docs: assistive only; no unattended merge claim |

### E-OAS2 — MCP parity (later)

Wire RunContext into `adapters/mcp` fault envelopes; stderr structured events;
still no SDK pin unless Spike.

### E-OAS3 — Retrieval eval harness (optional)

Campaign-only packet/recall sensors — never embedding citation SoT.

### E-OAS4 — Shell matrix campaign (optional after OAS1)

Windows `bash` + `pwsh` (+ optional `cmd`) smoke for `self-test` / doctor; not Cover% SoR.

### Explicit Refuse / Never

rich CI SoT · OTel tip SoT · embedding citation SoT · MCP codegen · megacli boil ·
parallel tip thrash with E-GND0 Implement · **unattended AI merge** · **universal OS/terminal/phone emulator as CLI SoT**.

---

## 7. Adversarial checklist

- [ ] Does Typer become a silent new SoT for all CLIs? → OAS7 prevents.
- [ ] Does “modern RAG” smuggle vector citation? → OAS11 Refuse.
- [ ] Does OTel become required for green? → OAS10 Refuse tip SoT.
- [ ] Does MCP stdout logging break Cursor hosts? → OAS3.
- [ ] Does doctor block offline remeasure (exit 3 path)? → doctor gates toolchain only; Artifactory remains exit-3 campaign semantics.
- [ ] process/ memo sprawl? → OAS14 synthesis; taxonomy reshape separate.
- [ ] Does MCP language imply AI replaces human review? → OAS15 Refuse.
- [ ] Does “test all terminals” become device-farm theater? → OAS16 Refuse phones; Adopt finite shell matrix.

---

## 8. Exit criterion for Spec

Human Approve of **OAS1–OAS16** recorded in
`docs/design/operator-agent-surface-design-2026-08-10.md` status line.
Until then: **no Implement** of Typer grade CLI / RunContext package.
