---
title: CLI / operator surfaces — problem-first inventory (A–J)
status: RESEARCH memo — deepens E-OAS0; no Implement
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (+ MCP adapter; Stage-0 retrieval)
related:
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/process/38-cli-dx-a11y-dual-sinks-2026-08-10.md
  - docs/design/operator-agent-surface-design-2026-08-10.md
  - docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md
  - docs/research/archive/claude-lore/research/s-stf-e-mcp-isolation-adr-2026-08-08.md
  - docs/research/se-quality-synthesis-2026-08-08.md
do_not:
  - implement Typer grade / RunContext before E-OAS0 Approve
  - treat Charm/Rich/Textual as CI or merge SoT
  - treat framework catalogs as the research question
  - unattended AI merge / universal OS×terminal emulator as CLI SoT
gh_api_stamp: 2026-08-10 (stars via GitHub REST)
spec_feeds: E-OAS0 (OAS1–OAS16 DRAFT)
---

# Problem-first CLI / operator surfaces (deeper than Charm/Clap catalogs)

**Question.** Before naming frameworks: what *operator/human failures* created
each tool class? What job does a response restore? What remains unsolved? Why
do **human-readable** and **machine-parseable** sinks both exist as *problems*
(not aesthetics)? Map every class to **doc-engine E-OAS0**.

**Method.** Problem inventory → tool responses → Embody / Adopt / Refuse for
this Python CLI product → Unknowns. Claim tiers: `[Evidenced]` primary ·
`[Confirmed]` this repo · `[Unknown]` not verified here.

**Not this memo.** Star tables of Typer/Click/Clap/Cobra/Charm as the answer.
Those are *responses* — see class **J**. Landing-pad catalogs live in
[`38-…`](38-cli-dx-a11y-dual-sinks-2026-08-10.md); Spec decisions in
[`37-…`](37-operator-agent-surface-cli-mcp-rag-2026.md).

---

## 0. Dual-sink meta-problem (why both exist)

| Audience | Failure without their sink | Failure if *only* their sink |
| --- | --- | --- |
| **Human operator** | Exit 1 + empty/cryptic stderr → StackOverflow loop (NoFAQ / CLAI) | JSON/JSONL alone is hostile at a TTY; no mental model of “what next” |
| **Machine / agent / CI** | Pretty tables, spinners, box-drawing → unparseable; pipe-exit masking | Human prose alone → brittle scrapers; agents invent remediation |

**Why both are problems.** Human-first output without a twin breaks agents and
CI. Machine-first output without a headline breaks operators and screen-reader
users who need plain structure. Industry SoR treats them as **two presenters
over one result object** (clig.dev; `gh --json`; ruff multi-format)
`[Evidenced]` — not as two competing products. Repo E-UX0 already **Embodies**
headline + detail dual sinks for CI `[Confirmed]`
(`docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md`).

**E-OAS0 map:** **OAS2** dual sink; **OAS3** MCP stderr; **OAS8** refuse rich as
CI SoT; **OAS15** human review floor (agents consume machine sink; humans
approve Spec/merge).

---

## 1. Problem classes A–J

For each class: **(1)** failure before the tool class · **(2)** job restored ·
**(3)** what it does *not* solve · **(4)** dual-sink angle · **E-OAS0**.

### A. Opaque failures (exit 1, no actionable next step)

| Lens | Content |
| --- | --- |
| **Failure** | Cryptic errors force leave-the-terminal search. NoFAQ documents novices cannot map “buggy command + opaque message” to a fix without forum search `[Evidenced]` [1608.08219](https://arxiv.org/abs/1608.08219). CLAI names the copy→browser→paste loop `[Evidenced]` [2002.00762](https://arxiv.org/abs/2002.00762). HotOS shell panel: shell lacks affordances; “?”-class errors are historical norm `[Evidenced]` [2109.11016](https://arxiv.org/abs/2109.11016). Google Cloud UXR playbook treats CLI + error messages as high-friction domains needing triangulated POV `[Evidenced]` [2605.31104](https://arxiv.org/abs/2605.31104). |
| **Job restored** | Errors as *documentation*: what failed, why, **concrete next command** (clig.dev Errors) `[Evidenced]`. Stable exit taxonomy so scripts branch. Structured `suggested_fix` / applicability for agents (industry dual-consumer pattern, 2026) `[Evidenced]` secondary. |
| **Does not solve** | Wrong product Spec; missing credentials; LLM-rewritten prose as gate truth (RCT: LLM-enhanced PEM ineffective in practice `[Evidenced]` [2409.18661](https://arxiv.org/abs/2409.18661)). Repair synthesis ≠ trustworthy auto-apply of destructive fixes (HotOS warns) `[Evidenced]`. |
| **Dual sink** | Headline: `FAIL · code · next: source .venv/bin/activate`. Receipt: `{code, next_actions[], artifact_paths}`. |
| **E-OAS0** | **OAS5** remediation strings; **OAS4** doctor fail-closed; plant exit 3/49 already Confirmed. |
| **Repo Confirmed** | Live grade: WindowsApps `python3` stub → EXIT 49 with opaque “Python was not found”; `python foo.cmd` NoFAQ-class failure (`37` §0). |

### B. Environment matrix hell (OS × shell × PATH × encoding)

| Lens | Content |
| --- | --- |
| **Failure** | Same binary, different truth: `python` vs `py` vs WindowsApps stub; Git Bash vs `pwsh` vs `cmd` quoting; `PATH`/`PATHEXT`; CRLF; locale/encoding; venv not activated. HotOS: shell is lingua franca *and* socio-technical failure — pedagogy and POSIX conventions retreat `[Evidenced]` [2109.11016](https://arxiv.org/abs/2109.11016). |
| **Job restored** | Real runners (GHA OS×shell), doctor that **names** the interpreter SoR, campaign matrices — not “works on my Mac.” Scenario harnesses for PATH/`NO_COLOR`/launch mode `[Evidenced]` (gh-aw-class; see `37` §5b). |
| **Does not solve** | Every corp image, Admin vs user Windows, phone farms. **No** honest universal OS×terminal×phone emulator as merge SoT `[Evidenced]` (`37` §5b). Docker ≠ PowerShell Desktop. |
| **Dual sink** | Doctor headline for humans; JSON profile (`prefix`, `python`, `shell`, `path_ok`) for CI/agents. |
| **E-OAS0** | **OAS16** campaign matrix; **OAS4** doctor; Refuse device-farm theater. |
| **Repo Confirmed** | CI today ≈ Ubuntu Python matrix only — Windows/macOS shell gap real (`37` §5b). |

### C. Progress / status lies (spinners hide hung processes)

| Lens | Content |
| --- | --- |
| **Failure** | Braille/Unicode spinners redraw the line: looks “alive” while hung; CI logs fill with cursor noise; screen readers vocalize frames as nonsense. GitHub CLI a11y work replaced spinners with static “Working…” `[Evidenced]` ([gh blog](https://github.blog/engineering/user-experience/building-a-more-accessible-github-cli/); `GH_SPINNER_DISABLED` [PR #10773](https://github.com/cli/cli/pull/10773)). gcloud `accessibility/screen_reader` → status trackers + % on stderr `[Evidenced]`. |
| **Job restored** | Honest liveness: heartbeat / step events / timeouts; textual progress; **progress twin** in machine sink. |
| **Does not solve** | Deadlocks inside black-box children without instrumentation; fake ETA. |
| **Dual sink** | TTY may show bar; JSONL `progress` events (or disable under non-TTY / `NO_COLOR` / spinner-disabled). Spinner as *sole* channel = Refuse. |
| **E-OAS0** | **OAS2** events include `duration_ms`; **OAS8** rich progress never CI SoT; align `DOC_ENGINE_SPINNER_DISABLED` with gh pattern (`38` §2.1). |

### D. Accessibility / non-visual operators

| Lens | Content |
| --- | --- |
| **Failure** | CLIs assume sighted TTY: color-only status, box-drawing tables, emoji PASS/FAIL, interactive redraw prompts. Non-visual operators and CI consumers share the same broken channel. |
| **Job restored** | `NO_COLOR` `[Evidenced]` [no-color.org](https://no-color.org/); `--plain`; accessible prompter / 4-bit palette (`GH_ACCESSIBLE_*`); gcloud screen_reader flattened tables; ACCESSIBLE=1 conventions. |
| **Does not solve** | Full WCAG for every terminal emulator; VoiceOver quirks per OS (campaign, not universal claim). |
| **Dual sink** | `--plain` / JSON are the a11y SoR; decorative Rich is optional TTY only. |
| **E-OAS0** | **OAS8**; Embody `NO_COLOR` / non-TTY quiet (`38`); Refuse emoji-as-status (E-UX0 **U7** `[Confirmed]`). |

### E. Scriptability vs interactive polish tension

| Lens | Content |
| --- | --- |
| **Failure** | Tools optimized for demos (fullscreen TUI, prompts, animations) break pipes, non-interactive CI, and MCP stdio. Tools optimized only for scripts feel “hung” to humans (classic UNIX silence). clig: human-first *and* composable `[Evidenced]`. HotOS: shell is both UI and programming language — tension is structural `[Evidenced]` [2109.11016](https://arxiv.org/abs/2109.11016). |
| **Job restored** | TTY detection; `--no-input`; quiet flags; dual modes (interactive doctor vs non-interactive grade). Charm Bubble Tea / Crush: interactive *and* `run` non-interactive `[Evidenced]` DeepWiki [charmbracelet/crush](https://deepwiki.com/charmbracelet/crush). |
| **Does not solve** | One UI that is best for both without mode split; Textual-as-grade SoR. |
| **Dual sink** | Interactive polish never the receipt; scripts consume JSON / exit codes. |
| **E-OAS0** | **OAS7** Typer thin façade; Refuse Textual/fullscreen as grade SoR (`38`); prompt_toolkit only if interactive doctor Spec’d. |

### F. Configuration discovery (which flag? which file wins?)

| Lens | Content |
| --- | --- |
| **Failure** | Operators cannot answer: flag vs env vs `.env` vs XDG vs `/etc` vs baked default. Wrong layer “wins” silently. Clap intentionally omits full layered merge — ecosystem builds `value_source()`-aware layers `[Evidenced]` (clap-layers DESIGN; DeepWiki [clap-rs/clap](https://deepwiki.com/clap-rs/clap)). |
| **Job restored** | Documented precedence (clig: flags > shell env > project > user > system) `[Evidenced]` [clig.dev §Configuration](https://clig.dev/#configuration); `doctor` / `--explain-config` provenance; XDG paths. |
| **Does not solve** | Infinite enterprise policy overlays; secret stores as CLI SoT. |
| **Dual sink** | Human: “using venv python from X (flag > env > default)”. Machine: `config_provenance[]`. |
| **E-OAS0** | **OAS1** RunContext policy ports; doctor surfaces provenance; avoid megacli config sprawl (**OAS7**). |

### G. Unsafe defaults / footguns (`rm`, `--force`)

| Lens | Content |
| --- | --- |
| **Failure** | Destructive defaults; `-f` suppresses prompts *and* diagnostics (POSIX `rm`) `[Evidenced]`; `y/N` confirmations without naming the resource. HotOS: NL→shell synthesis of “destroy all PDFs” → `shred` shows semantic risk `[Evidenced]` [2109.11016](https://arxiv.org/abs/2109.11016). |
| **Job restored** | Safe defaults; `--dry-run`; `--force` explicit and loud; confirmation effort ∝ risk (type resource name); state-change narration (clig) `[Evidenced]`. |
| **Does not solve** | Malicious operators; compromised automation with `--force` baked in. |
| **Dual sink** | Human confirmation on TTY; scripts require `--force` + machine audit event — never silent. |
| **E-OAS0** | **OAS12** refuse MCP write/codegen; **OAS15** human review floor for `--write` / merge; grade defaults non-destructive. |

### H. Plugin / extension isolation (MCP, go-plugin) — trust problem

| Lens | Content |
| --- | --- |
| **Failure** | In-process plugins share memory/crash domain; agent tools inherit host FS/network (confused deputy). Dynamic `dlopen` unacceptable for Vault-class hosts. |
| **Job restored** | **Process isolation + typed RPC:** HashiCorp go-plugin (subprocess, checksum, TLS; ★6064 2026-08-10) `[Evidenced]` DeepWiki [hashicorp/go-plugin](https://deepwiki.com/hashicorp/go-plugin); Vault containerized plugins / gVisor for stronger isolation `[Evidenced]`. MCP: capability negotiation, stdio JSON-RPC, **log to stderr** `[Evidenced]` [MCP architecture](https://modelcontextprotocol.io/docs/concepts/architecture). Repo ADR: server-derived root only; no caller `root` `[Confirmed]` `s-stf-e-mcp-isolation-adr`. |
| **Does not solve** | Supply-chain trust of the plugin *binary*; network MCP without auth; “relative security” ≠ full sandbox (go-plugin docs: host must protect SecureConfig). |
| **Dual sink** | Tool results = lean JSON envelopes; diagnostics on stderr — never stdout on stdio MCP. |
| **E-OAS0** | **OAS3**, **OAS11**, **OAS12**, **OAS15**; Embody `dispatch_tool` library SoR; Defer SDK pin (GND9). |

### I. Documentation drift (help ≠ README ≠ actual flags)

| Lens | Content |
| --- | --- |
| **Failure** | Three SoTs: generated `--help`, README tutorials, shipped flags. Drift is a *process* failure; READU: README bugs as inconsistency with internal/external facts `[Evidenced]` [2607.15780](https://arxiv.org/abs/2607.15780); DocPrism: incorrectness (not mere incompleteness) between code and docs `[Evidenced]` [2511.00215](https://arxiv.org/abs/2511.00215). |
| **Job restored** | Single definition → generate help/completions/man (clap `clap_mangen` / `clap_complete` pattern) `[Evidenced]`; CI claims/predicates on paths and literals (this repo’s `check_repo_claims.py`) `[Confirmed]`; drift sensors — never LLM docs as SoT. |
| **Does not solve** | Prose quality; aspirational README written ahead of code (claims checker decides *resolvable*, not *true* — CLAUDE.md). |
| **Dual sink** | `--help` human; `--help --json` / schema export machine (where offered); README examples tested or marked derived. |
| **E-OAS0** | Grade façade help generated from Typer/Click definitions (**OAS7**); claims verify for docs that cite grade flags once they exist. |

### J. Why Typer / Click / Clap / Cobra / Charm exist (problems, not frameworks)

These frameworks are **compressed responses** to recurring failures — not the
research question.

| Framework | Stars (2026-08-10) | Underlying problems they answer | Still unsolved alone |
| --- | --- | --- | --- |
| **Click** | ★17618 | Hand-rolled `argparse` sprawl; untested CLIs; no composable groups | Dual sinks; a11y; OS matrix; trust |
| **Typer** | ★19881 | Untyped Click boilerplate; help/exit inconsistency | Same; tempting megacli boil |
| **Clap** | ★16620 | Missing polished help/suggestions/completions; builder vs derive tension; “developer panic vs user error” split `[Evidenced]` DeepWiki | Config file layering (out of core); rich TUI |
| **Cobra** | ★44420 | Go service CLIs without subcommand UX; help/flag conventions | Often paired with Viper → class F complexity; not a11y SoT |
| **Charm (Bubble Tea, Lipgloss, …)** | Bubble Tea ★44272 | Stateful interactive terminal without Elm-like testable model; ad-hoc ANSI soup | Fullscreen vs scriptability (E); process isolation (H); CI SoT |

**Category error to refuse:** “pick Charm vs Typer” as architecture. Correct
frame: restore jobs A–I; frameworks are optional adapters.

**E-OAS0:** **Adopt** Typer *only* for thin `doc-engine grade` (**OAS7**);
**Adopt pattern** Charm Elm-MVU / clap help semantics; **Refuse** Charm/Go
runtime and rich-as-CI-SoT (**OAS8**).

---

## 2. arXiv / DeepWiki / GitHub evidence index

| ID / source | Class | Tier |
| --- | --- | --- |
| [1608.08219](https://arxiv.org/abs/1608.08219) NoFAQ | A | Evidenced |
| [2002.00762](https://arxiv.org/abs/2002.00762) Project CLAI | A, E | Evidenced |
| [2109.11016](https://arxiv.org/abs/2109.11016) HotOS Future of the Shell | A, B, E, G | Evidenced |
| [2605.31104](https://arxiv.org/abs/2605.31104) UXR POV / CLI + errors | A | Evidenced |
| [2409.18661](https://arxiv.org/abs/2409.18661) LLM PEM ineffective | A (Refuse LLM-as-gate) | Evidenced |
| [2210.11630](https://arxiv.org/abs/2210.11630) LLM enhance PEM | A (sensor only) | Evidenced |
| [2012.10206](https://arxiv.org/abs/2012.10206) CLI customization | F (aliases = missing defaults) | Evidenced |
| [2607.09510](https://arxiv.org/abs/2607.09510) CLI coding-agent failure trajectories | A, H (agents) | Evidenced |
| [2607.15780](https://arxiv.org/abs/2607.15780) READU README bugs | I | Evidenced |
| [2511.00215](https://arxiv.org/abs/2511.00215) DocPrism | I | Evidenced |
| [2607.17598](https://arxiv.org/abs/2607.17598) Progressive disclosure agents | E, dual-sink L0/L1/L2 | Evidenced (adjacent) |
| clig.dev | A–G, dual-sink | Evidenced |
| DeepWiki clap / go-plugin / crush | J, H, E | Evidenced (cartography) |
| gh / gcloud a11y | C, D | Evidenced |
| Repo E-UX0 U7; MCP isolation ADR; grade §0 | D, G, H, A | Confirmed |

**Gap `[Unknown]`:** no 2020–2026 arXiv that *prescribes* dual human/JSON sinks
as an HCI *standard* — industry SoR fills it (`38` already noted). No primary
study quantifying spinner→false-liveness incident rates in CI fleets.

---

## 3. Tool-class responses (problem → response map)

```text
A opaque errors     → remediation copy, exit taxonomy, rustc-like help, NoFAQ/CLAI
B env matrix        → doctor, real OS×shell campaign jobs, pinned interpreters
C progress lies     → textual progress, heartbeats, JSONL progress twin, timeouts
D a11y              → NO_COLOR, --plain, accessible prompter, no emoji-status
E script vs polish  → TTY detect, --no-input, dual mode (TUI | headless)
F config discovery  → precedence docs, provenance explain, XDG, value_source
G footguns          → safe defaults, dry-run, loud --force, human floor
H plugin trust      → subprocess RPC, checksum/TLS, MCP capabilities, FS roots
I docs drift        → generate help from one def; CI path/literal claims; drift sensors
J frameworks        → Click/Typer/Clap/Cobra/Charm = adapters for A–F polish — not SoT
```

---

## 4. Embody / Adopt / Refuse (doc-engine)

| Stance | Choice |
| --- | --- |
| **Embody** | Dual sinks (headline + JSON/JSONL receipt); exit taxonomy; `NO_COLOR` / non-TTY quiet; Stage-0 + `context_packet` retrieval SoR; MCP `dispatch_tool` + stderr-only stdio; **human Spec/operator review floor**; server-derived FS root |
| **Adopt** | clig.dev human-first; actionable remediation (NoFAQ class); gh-style `--json` + a11y env knobs; ruff multi-presenter pattern; Typer **thin** grade façade only; campaign OS×shell matrix; Charm/clap **patterns** only; progressive L0/L1/L2 disclosure |
| **Refuse** | Rich/emoji/progress as CI or merge SoT; Textual/fullscreen as grade SoR; Charm/Go stack as product dep; embedding as citation SoT; OTel as tip SoT; MCP write/codegen; megacli boil of all `scripts/ci`; LLM error prose as gate truth; unattended AI merge; universal OS×terminal×phone emulator as CLI SoT |

---

## 5. Map → E-OAS0 decisions (OAS1–OAS16)

| Classes | Primary OAS IDs |
| --- | --- |
| Dual-sink meta, C, E | **OAS2**, **OAS8** |
| A, F (doctor) | **OAS4**, **OAS5**, **OAS1** |
| H, MCP | **OAS3**, **OAS11**, **OAS12** |
| J (Typer) | **OAS7**, **OAS9** (structlog defer) |
| Observability theater | **OAS10** |
| Human floor / footguns | **OAS15**, **OAS12** |
| B matrix | **OAS16** |
| Process | **OAS6**, **OAS13**, **OAS14** |

**Spec gate unchanged:** no Implement of grade CLI / RunContext until human
Approve of OAS1–OAS16 in
[`docs/design/operator-agent-surface-design-2026-08-10.md`](../../design/operator-agent-surface-design-2026-08-10.md).

---

## 6. Adversarial checklist

- [ ] Is this memo a Charm/Clap shopping list? → No; frameworks only in **J** as responses.
- [ ] Does dual-sink imply two SoTs? → No; one `GradeReport` / receipt object, two presenters.
- [ ] Does a11y justify Rich in CI? → Opposite; plain/JSON are the a11y SoR.
- [ ] Does go-plugin imply we rewrite in Go? → Pattern only (**H** Adopt-pattern).
- [ ] Does agent trajectory paper justify unattended merge? → No; **OAS15** Refuse.
- [ ] Does OS matrix mean device farm? → **OAS16** finite campaign only.

---

## 7. Unknowns / spikes (non-blocking)

| ID | Question | Exit criterion |
| --- | --- | --- |
| U1 | Minimal Windows×`pwsh` + Git Bash smoke cost on GHA for grade self-test? | Timeboxed campaign job green or Explicit Defer |
| U2 | Is `--explain-config` worth a Spec ticket vs doctor JSON only? | One operator pilot transcript |
| U3 | MCP SDK pin vs keep thin adapter (GND9)? | Remains on E-GND0 — out of this tip |
| U4 | Quantitative spinner false-liveness rate? | Literature still Unknown — do not block Spec |

---

## Provenance

- Primary: clig.dev; arXiv IDs above; MCP architecture docs; POSIX `rm`;
  no-color.org; gh/gcloud a11y docs; DeepWiki clap / go-plugin / crush.
- GitHub stars: `gh api` 2026-08-10.
- Sibling synthesis: process/37 (E-OAS0), process/38 (DX/a11y landing pads).
- This tip: problem-first deepening only — **no Implement**.
