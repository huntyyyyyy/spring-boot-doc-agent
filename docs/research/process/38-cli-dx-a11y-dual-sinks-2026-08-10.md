---
title: CLI DX · terminal a11y · dual human/JSON sinks (landing pads)
status: RESEARCH memo — feeds E-OAS0 / doc-engine grade (no impl)
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (+ future RAG/agent retrieval; structure-first citation SoT)
related:
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/research/process/39-cli-operator-problem-classes-2026-08-10.md
  - docs/research/ci/11-ci-output-ux-progressive-disclosure-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
do_not:
  - implement grade/MCP sinks in this tip
  - treat rich tables / emoji / progress UI as merge or CI SoT
  - treat embeddings as citation SoT
gh_api_stamp: 2026-08-10 (stars + pushed_at via GitHub REST)
---

# CLI developer experience research — 2026-08-10

**Question.** What modern GitHub + arXiv evidence should shape a **beautiful-but-honest** Python CLI (`doc-engine grade` + MCP dual sinks) that later grows toward RAG/agent retrieval while keeping **structure-first facts as citation SoT** (refuse embedding-as-SoT)?

**Tiers:** `[Evidenced]` primary docs/API · `[Confirmed]` this repo · `[Unknown]` not verified here.

---

## 1. Landing pads (≥8 high-★ / elegant repos)

Stars and `pushed_at` from GitHub REST on **2026-08-10**. Patterns mapped to **Adopt** vs **Refuse** for doc-engine.

| # | Repo | ★ | Last push | Pattern | Adopt / Refuse for doc-engine |
| --- | ---: | ---: | --- | --- | --- |
| 1 | [fastapi/typer](https://github.com/fastapi/typer) | 19881 | 2026-08-08 | Type-hint CLI, subcommands, Rich-optional printing | **Adopt** thin `doc-engine grade` façade only (typed cmds, help, exit codes). **Refuse** boiling all `scripts/ci` into one Typer megacli in one tip. `[Evidenced]` |
| 2 | [pallets/click](https://github.com/pallets/click) | 17617 | 2026-08-09 | Composable groups, testing harness, ANSI helpers | **Adopt** Click semantics Typer already wraps; **Refuse** new Click-only surface beside Typer (two CLIs). `[Evidenced]` |
| 3 | [Textualize/rich](https://github.com/Textualize/rich) | 57044 | 2026-06-23 | Tables, progress, markup, `NO_COLOR` / `FORCE_COLOR` | **Adopt** optional TTY polish behind env gates. **Refuse** rich tables/progress as CI/merge SoT (E-UX0 U7). `[Evidenced]` + `[Confirmed]` |
| 4 | [Textualize/textual](https://github.com/Textualize/textual) | 36893 | 2026-07-11 | Full-screen TUI apps | **Refuse** as grade/MCP SoT (clig.dev excludes fullscreen; operators need scriptable receipts). Optional future demo only. `[Evidenced]` |
| 5 | [prompt-toolkit/python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) | 10548 | 2026-07-26 | Interactive prompts, completion, a11y-friendly prompts | **Adopt** only if interactive doctor/remediation is Spec’d; default grade stays non-interactive. `[Evidenced]` |
| 6 | [httpie/cli](https://github.com/httpie/cli) | 38405 | 2024-12-17 | Human-first HTTP UX; selective `-p`/`-b` output; sessions | **Adopt** “say enough, not dump”; selective streams. **Refuse** emoji pie branding as status vocabulary. `[Evidenced]` (push stale — still elegant UX SoR) |
| 7 | [cli/cli](https://github.com/cli/cli) (`gh`) | 45764 | 2026-08-10 | `--json` + `--jq`/`--template`; `NO_COLOR`; `GH_FORCE_TTY`; `GH_ACCESSIBLE_PROMPTER`; `GH_SPINNER_DISABLED` | **Adopt** dual sinks + a11y env knobs as gold pattern. `[Evidenced]` primary: [gh formatting](https://cli.github.com/manual/gh_help_formatting), [gh environment](https://cli.github.com/manual/gh_help_environment) |
| 8 | [cli-guidelines/cli-guidelines](https://github.com/cli-guidelines/cli-guidelines) → [clig.dev](https://clig.dev/) | 3815 | 2026-05-16 | Human-first + `--json` / `--plain`; TTY detection; exit clarity | **Adopt** as written Spec philosophy for grade. `[Evidenced]` |
| 9 | [charmbracelet/bubbletea](https://github.com/charmbracelet/bubbletea) | 44270 | 2026-08-07 | Elm-ish TUI (Go) | **Adopt pattern only** (state → view; testable model). **Refuse** Go runtime / Charm stack as product dep. `[Evidenced]` |
| 10 | [charmbracelet/lipgloss](https://github.com/charmbracelet/lipgloss) | 11680 | 2026-07-26 | Declarative styles | **Adopt pattern only** (style tokens ≠ SoT). `[Evidenced]` |
| 11 | [astral-sh/ruff](https://github.com/astral-sh/ruff) | 49120 | 2026-08-09 | Dual formats: `full`/`concise`/`grouped` **and** `json`/`github`/`junit` | **Adopt** “one engine → many presenters”. `[Evidenced]` [ruff output-format](https://docs.astral.sh/ruff/settings/#output-format) |
| 12 | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | 14398 | 2026-08-10 | `-q`/`-v` progressive disclosure; junit/CI reporters; FORCE_COLOR listed | **Adopt** quiet default + escalate verbosity; machine receipt twin. `[Evidenced]` [pytest output](https://docs.pytest.org/en/stable/how-to/output.html) |
| 13 | [vercel/pkg](https://github.com/vercel/pkg) | 24361 | 2024-01-03 | Single-binary packaging | **Refuse as active SoR** — **archived**. Prefer PyInstaller/Nuitka *only if* packaging epic opens. `[Evidenced]` |
| alt | [pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) | 13054 | 2026-08-09 | Frozen Python binaries | **Defer** packaging; not grade UX. `[Evidenced]` |
| alt | [simonw/llm](https://github.com/simonw/llm) | 12337 | 2026-08-09 | Plugin CLI + structured tool output | **Adopt** plugin/envelope discipline for MCP; **Refuse** LLM text as citation SoT. `[Evidenced]` |

**Minimum bar satisfied:** rows 1–12 (≥8). Charm/bubbletea = pattern-only. pkg = anti-pattern (archived).

---

## 2. Accessibility dimensions (terminals)

Primary citations via WebFetch **2026-08-10**.

### 2.1 Color / motion / TTY

| Dimension | Primary rule | Source | doc-engine stance |
| --- | --- | --- | --- |
| Disable color | `NO_COLOR` set and non-empty ⇒ no ANSI color | [no-color.org](https://no-color.org/) `[Evidenced]` | **Embody** |
| Force color | `FORCE_COLOR` non-empty ⇒ force ANSI; Rich: `NO_COLOR` wins over `FORCE_COLOR` | [force-color.org](https://force-color.org/); [Rich Console](https://rich.readthedocs.io/en/stable/console.html) `[Evidenced]` | **Adopt** |
| Dumb terminal | `TERM=dumb` ⇒ no color (clig) | [clig.dev §Output](https://clig.dev/#output) `[Evidenced]` | **Embody** |
| Non-TTY | No animations/progress Christmas trees in CI logs | clig.dev; Rich strips animations when not a terminal `[Evidenced]` | **Embody** |
| Force TTY-style | `GH_FORCE_TTY` pattern (cols / %) | [gh environment](https://cli.github.com/manual/gh_help_environment) `[Evidenced]` | **Adopt** as `DOC_ENGINE_FORCE_TTY` *if* Spec’d |
| Spinner a11y | `GH_SPINNER_DISABLED` → textual progress | gh env `[Evidenced]` | **Adopt** — spinner never sole status channel |

### 2.2 Screen-reader / semantic structure

| Dimension | Finding | Tier | Stance |
| --- | --- | --- | --- |
| Speech/braille prompts | `GH_ACCESSIBLE_PROMPTER` (preview) for speech synthesis + braille | Evidenced (gh) | **Adopt** when interactive prompts land |
| Accessible colors | `GH_ACCESSIBLE_COLORS` → 4-bit customizable palette | Evidenced (gh) | **Adopt** over truecolor-only status |
| Semantic vs decorative | Box-drawing / Unicode tables are decorative; screen readers need plain line/JSON structure | Confirmed (repo U7) + Evidenced (clig `--plain`) | **Embody** `--plain` / JSON twin; **Refuse** box art as only receipt |
| Emoji-as-status | clig allows emoji “where clearer” but warns of toy/clutter; gh still uses color/labels carefully | Evidenced | **Refuse** emoji as PASS/FAIL vocabulary (repo Confirmed U7) |

### 2.3 Progressive disclosure

| Layer | Human sink | Machine sink |
| --- | --- | --- |
| L0 headline | 1–3 lines: PASS/FAIL · exit · next action | `status`, `exit_code`, `remeasure_ok` |
| L1 groups | collapsible / `--verbose` sections | JSONL events per step |
| L2 evidence | paths to logs / coverage.xml / claims | schema-versioned receipt file |

Aligns with landed E-UX0 summary-first `[Confirmed]` and clig “saying just enough” `[Evidenced]`.

### 2.4 Exit codes & machine-readable receipts

| Rule | Source | Stance |
| --- | --- | --- |
| Stable, documented exit taxonomy (0 ok · non-zero class of failure) | UNIX + clig robustness; repo plant exit 3/49 already used | **Embody** `[Confirmed]` plant grades |
| `--json` / receipt file is SoR for agents/CI; TTY is presentation | clig `--json`; gh `--json`+`--jq`; ruff `json`/`github` | **Embody** |
| stderr for diagnostics; don’t treat stderr as log file by default | clig.dev Errors/Output | **Adopt** (MCP stdio: logs → stderr only — already Confirmed in E-OAS0) |

---

## 3. arXiv (≥3, 2020–2026)

| ID | Year | Title | Why it matters | Tier |
| --- | --- | --- | --- | --- |
| [2012.10206](https://arxiv.org/abs/2012.10206) | 2020→ESE 2022 | *An Empirical Investigation of Command-Line Customization* | Alias mining ⇒ usability gaps (colorize, override defaults, shortcuts). Grade should ship sane defaults + `--json` rather than forcing users to alias. | Evidenced |
| [2210.11630](https://arxiv.org/abs/2210.11630) | 2022 | *Using Large Language Models to Enhance Programming Error Messages* | LLM-rewritten errors can help novices — but are **explanations**, not SoT. | Evidenced |
| [2409.18661](https://arxiv.org/abs/2409.18661) | 2024 | *Not the Silver Bullet: LLM-enhanced Programming Error Messages are Ineffective in Practice* | Classroom RCT: LLM-enhanced messages **not** effective in practice. | Evidenced → **Refuse** LLM prose as grade/CI truth |
| [2607.17598](https://arxiv.org/abs/2607.17598) | 2026 | *Is Progressive Disclosure All You Need for Long-Context Agents?* | Progressive disclosure as agent skill loading (description → passage). Maps to L0/L1/L2 sinks + future RAG **without** embedding-as-citation. | Evidenced (adjacent) |
| [2606.03854](https://arxiv.org/abs/2606.03854) | 2026 | *CLI-Anything: Towards Agent-Native Computer Use* | Argues CLI/agent-native beats brittle GUI agents — supports MCP+CLI dual surface. | Evidenced (context) |

**Bonus (weaker fit):** [2607.00140](https://arxiv.org/abs/2607.00140) CogTax (CLI education taxonomy) — pedagogical, not product UX. `[Evidenced]` skim only.

**Gap `[Unknown]`:** no strong 2020–2026 arXiv found that *prescribes* dual human/JSON CLI sinks as an HCI standard; industry SoR (clig/gh/ruff) fills that gap.

---

## 4. Bloom Evaluate → Create — invent for `doc-engine grade` / MCP

**Evaluate (external → repo):** clig/gh/ruff dual presenters beat “pretty tables in CI.” Repo already has RunContext / receipt seeds and E-UX0 dual sinks `[Confirmed]`. Embeddings must stay retrieval sensors, not citation SoT `[Confirmed]` constitution.

**Create (principal SE invent — not yet Spec-approved):**

1. **`GradeReport` port** — one immutable result object (steps, exit taxonomy, remediation tips, artifact paths). OCP presenters: `HeadlinePresenter`, `PlainPresenter`, `JsonReceiptPresenter`, optional `RichTtyPresenter` (TTY-only, never CI SoT).
2. **`doc-engine grade`** — Typer thin façade over existing grading pack; default human L0; `--json` / `--receipt PATH` always available; `--plain` kills box-drawing.
3. **MCP twin** — same `GradeReport` via `dispatch_tool`; tool return = lean JSON; logs only on stderr; no rich markup in MCP payloads.
4. **Progress twin** — if TTY shows a bar/spinner, emit JSONL `progress` events (or disable under `NO_COLOR` / non-TTY / `DOC_ENGINE_SPINNER_DISABLED`). Opaque bar alone = Refuse.
5. **Remediation copy** — actionable next commands (clig + NoFAQ class); optional LLM rewrite behind flag = **sensor**, never exit-code SoT (arXiv 2409.18661).
6. **Retrieval future** — progressive disclosure of `context_packet` / Stage-0 facts (arXiv 2607.17598); RAG ranks candidates; **citations resolve to structured facts**, not embedding nearest-neighbor as SoT.

---

## 5. Explicit Refuse

| Refuse | Why |
| --- | --- |
| **Rich tables as merge proof** | Decorative density ≠ oracle; E-UX0 U7; coverage/claims remain boolean SoT |
| **Emoji-as-status** (`✅`/`❌` as PASS/FAIL) | Non-semantic for screen readers; brittle in logs; repo U7 |
| **Opaque progress bars without JSON twin** | CI “Christmas trees”; agents can’t parse spinner frames |
| **Embedding / vector similarity as citation SoT** | Structure-first facts only; RAG is sensor |
| **Textual/fullscreen TUI as grade SoR** | Breaks scripting + MCP |
| **vercel/pkg as packaging SoR** | Archived 2024 |
| **LLM-enhanced error text as gate truth** | arXiv 2409.18661 |

---

## 6. One-page Embody / Adopt / Refuse

| Stance | Choice |
| --- | --- |
| **Embody** | Dual sinks (headline + JSON receipt); exit taxonomy; `NO_COLOR`; non-TTY quiet; structure-first citations |
| **Adopt** | Typer thin grade CLI; gh-style `--json`; ruff multi-format presenters; clig.dev human-first; optional Rich TTY; Charm Elm pattern only |
| **Refuse** | Rich-as-CI-SoT; emoji status; progress-without-receipt; embedding-as-citation; Textual-as-grade; archived pkg |

**Next:** Spec gate tickets under E-OAS0 (`OAS*` for grade façade + shared sinks) — no impl in this memo.

---

## Provenance

- GitHub stars/`pushed_at`: `gh api repos/...` on 2026-08-10.
- WebFetch: clig.dev, no-color.org, force-color.org, cli.github.com manuals, Rich Console, Typer printing, Ruff settings, pytest output.
- arXiv API: queries for CLI usability, programming error messages, progressive disclosure, agent-native CLI (2026-08-10).
