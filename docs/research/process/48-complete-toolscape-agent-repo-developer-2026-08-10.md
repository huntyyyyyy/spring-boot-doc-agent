---
title: E-TOOL0 — Complete toolscape for agents, repo gates, and developers (2026-08-10)
status: RESEARCH COMPLETE — Spec Draft (no mass installs until Approve)
date: 2026-08-10
epic: E-TOOL0
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_ask_question
  - llms_txt
related:
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - docs/research/process/39-polyglot-cli-toolkit-bfs-2026-08-10.md
  - docs/research/process/40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md
  - docs/research/process/41-language-excellence-domains-subdomains-2026-08-10.md
  - docs/research/process/46-lint-import-resolution-ruff-vs-ty-2026-08-10.md
  - docs/research/process/47-cursor-mdc-rules-devex-ai-repos-2026-08-10.md
  - adapters/claude/SEARCH.md
  - .cursor/rules/
sources:
  llms_txt:
    - https://docs.astral.sh/ruff/llms.txt
    - https://docs.astral.sh/ty/llms.txt
    - https://docs.astral.sh/uv/llms.txt
    - https://cursor.com/llms.txt
  deepwiki_ask:
    - astral-sh/ruff · astral-sh/uv · ast-grep/ast-grep · semgrep/semgrep
    - charmbracelet/bubbletea · spf13/cobra · hashicorp/go-plugin
    - ruby/ruby · babashka/babashka · clojure/clojure
  mcp: https://mcp.deepwiki.com/mcp
---

# Principal memo: who installs what — agent · repo · developer

**Product:** `doc-engine` Python CLI + Cursor/Claude agent DevEx.  
**Question.** Beyond “LLM prompts,” what is the **complete toolscape** humans and
agents should download and run — including **Ruby / Clojure / Go** — without
making polyglot the merge SoT?

**Method.** Fold Jul–Aug 2026 memos (22/33/39–41/46/47) + DeepWiki MCP Ask +
Astral/`cursor.com` `llms.txt` → Embody / Adopt / Pilot / Refuse by **audience**.

---

## 0. One-page verdict

| Audience | Must have today `[Confirmed]` | Next Adopt / Pilot | Refuse |
| --- | --- | --- | --- |
| **Repo / CI** | `.venv` pins: ruff, pytest, complexipy, tach, ast-grep, semgrep; CodeQL jobs; `pre_pr --auto`; claims | **ty** unresolved-import (E-LINT0); optional SARIF sensors | Mega-linter as SoT; dual Cover%; Sonar floor |
| **Developer laptop** | Same venv + `gh` + ripgrep + editor LSP; hooks via `install_git_hooks` | `uv` as installer Spike; AsciiDoc/RuboCop **sidecars** if Rails targets | Node husky; Go/Ruby/Clojure as tip kernel |
| **Cursor / Claude agent** | MDC pack + Skills + hooks; SEARCH playbook; DeepWiki MCP; WebFetch/`llms.txt` | Tip-probe MCP later (E-GND0); richer MCP sinks (E-OAS0) | Raw curl/clone; nested AGENTS path-SoT; alwaysApply bloat |
| **Ruby** | — | **Pilot-now:** Asciidoctor sink · RuboCop/Brakeman SARIF · Packwerk↔tach vocab | Ruby tip rewrite |
| **Go** | — | **Pattern / Pilot:** cobra/gh dual-sink · Bubble Tea TUI shape · go-plugin sensor host · Syft/Trivy | Go product rewrite |
| **Clojure** | — | **Pattern → Pilot-later:** Malli/Spec contracts · DataScript/XTDB facts · Babashka ops recipes | Clojure/SCI tip kernel |

**Bottom line:** Python kernel + Embodied Rust wheels stay SoT. Ruby/Go/Clojure
are **enhancement lanes** (patterns, sidecars, pilots) — already mapped in
E-POLY0 / E-POLY0b / E-LANG0 — not competing runtimes for `coverage.xml`.

---

## 0b. Bloom ladder

| Level | Evidence |
| --- | --- |
| **1 Remember** | Tool IDs + `llms.txt` + DeepWiki Ask on Astral / Charm / Babashka families |
| **2 Understand** | Audiences = repo gate / human DevEx / agent context — not one install list |
| **3 Apply** | Today: `.venv` + `pre_pr`; agents: MDC + SEARCH; pilots named with keep/drop |
| **4 Analyze** | Embody wheels vs Adopt-pattern vs Pilot-before-Refuse (memo 40 doctrine) |
| **5 Evaluate** | §7 adversarial — false-green from extra linters; false-red from ty without venv |
| **6 Create** | Tickets TOOL0–TOOL6 below — **Implement blocked until Approve** |

---

## 1. Problem classes (do not collapse)

| Class | Failure | Owner |
| --- | --- | --- |
| **T1 Gate SoT** | Local green ≠ CI 98.7 | `pre_pr` / oracle |
| **T2 Citation** | Text hit as structural proof | ast-grep (+ CodeQL/Semgrep) |
| **T3 Import resolution** | Unused ≠ unresolved | ruff vs **ty** (E-LINT0) |
| **T4 Agent context** | Always-on essay / missing tools | MDC modes + SEARCH |
| **T5 Human DX** | Opaque CLI / no dual-sink | E-OAS0 / gh patterns |
| **T6 Polyglot envy** | Rewrite tip in Go/Ruby/Clojure | Pilot-before-Refuse |

---

## 2. Ruby / Go / Clojure (explicit answer)

Already researched 2026-08-10 in [`39`](39-polyglot-cli-toolkit-bfs-2026-08-10.md),
[`40`](40-polyglot-open-bfs-pilot-before-refuse-2026-08-10.md),
[`41`](41-language-excellence-domains-subdomains-2026-08-10.md). DeepWiki Ask
this session reconfirmed shapes:

### Go — **yes, as patterns + optional helpers**

| Stick | Bucket | Why |
| --- | --- | --- |
| **cobra / gh `--json`** | Pattern | Subcommand + dual-sink UX for `doc-engine` / operator CLIs |
| **Bubble Tea / Lip Gloss** | Pattern → Pilot TUI | Elm-MVU review UX; host in Python, do not rewrite product in Go `[Evidenced — DeepWiki]` |
| **go-plugin** | Pattern → Pilot | Language-sensor sidecar shape (not in-proc merge) |
| **Syft / Trivy** | Pilot-now sensor | SBOM/vuln SARIF — never Cover% SoT |
| **Go rewrite of doc-engine** | **Refuse** | Category error vs Python kernel + Embodied Rust wheels |

### Ruby — **yes, for targets and sinks**

| Stick | Bucket | Why |
| --- | --- | --- |
| **Asciidoctor** | Pilot-now | Doc sink beside MkDocs |
| **RuboCop / Brakeman SARIF** | Pilot-now | When scanning Rails *targets*, not our Python tip |
| **Packwerk** | Pilot-later | Boundary vocabulary ↔ tach (E-TACH0) |
| **Bundler/Rake** | Dev helper only | If a Ruby sidecar exists — not tip deps `[Evidenced — DeepWiki]` |
| **Ruby tip kernel** | **Refuse** | Same as Go rewrite |

### Clojure — **yes, for contracts/facts/ops patterns**

| Stick | Bucket | Why |
| --- | --- | --- |
| **Malli / Spec** | Pattern → Pilot-later | Closed contract registries (FACT0/QUERY0 kin) |
| **DataScript / XTDB** | Pilot-later | As-of fact audits — sensors, not citation SoT |
| **Babashka** | Pilot-later ops | Fast native scripting binary **shape**; refuse as merge interpreter `[Evidenced — DeepWiki]` |
| **Clojure/SCI tip kernel** | **Refuse** | JVM/SCI as merge authority |

**Doctrine:** Pilot-before-Refuse (memo 40) — keep/drop exits required; stars are
cartography only.

---

## 3. Install matrix (download scope)

### 3.1 Already Embodied (do not re-debate)

`ast-grep-cli`, `semgrep`, `ruff`, `pytest`(+cov), `complexipy`, `tach`, CodeQL
(CI), `mkdocs-material`, `vacuous`, project hooks, `pre_pr`, claims checker,
ripgrep allowed (E-SEARCH0), Cursor MDC+Skills (E-MDC0).

### 3.2 Developer + agent recommended (not all pip-pinned)

| Tool | Who | Role |
| --- | --- | --- |
| **ripgrep** | Dev + agent | Prose/inventory |
| **gh** | Dev + agent | PR/CI JSON sinks |
| **DeepWiki MCP** | Agent (+ optional Dev) | Framework Ask |
| **uv** | Dev Spike | Fast venv/tool install (Astral) |
| **ty** | Repo gate after Approve | Unresolved imports |
| **Ruby/Go/Clojure sidecars** | Optional Dev/CI jobs | Only after named Pilot tickets |

### 3.3 Agent context (not downloads)

MDC glob lenses already teach tooling; Skills hold depth; hooks hard-deny raw
egress. Do not paste tool essays into alwaysApply.

---

## 4. Create — epic tickets

| ID | Acceptance |
| --- | --- |
| **TOOL0** | This memo + backlog Draft row |
| **TOOL1** | Publish `docs/process/toolscape.md` thin pointer index (audiences × Embody list) — docs-only |
| **TOOL2** | Wire **ty** per E-LINT0 after Approve |
| **TOOL3** | Document laptop bootstrap (`uv`/`venv`/`gh`/`rg`) in CONTRIBUTING — no husky |
| **TOOL4** | Ruby Pilot-now scorecard (Asciidoctor **or** RuboCop SARIF) with keep/drop |
| **TOOL5** | Go pattern landing: dual-sink CLI checklist stolen from gh/cobra (Python impl) |
| **TOOL6** | Clojure pattern note → FACT0/contracts; Babashka only if ops Spike named |

**Refuse until Approve:** mass `apt`/`brew` of Ruby/Go/Clojure toolchains on tip;
replacing Python oracle; mega-linter orchestrators.

---

## 5. Adversarial

| Risk | Mitigation |
| --- | --- |
| “Complete scope” → install everything | Audience matrix + Pilot exits |
| ty without `.venv` | E-LINT0 false-red checklist |
| Go TUI as CI SoT | Pattern-only; CI stays JSON/text |
| Babashka merge scripts | Refuse SCI authority |
| DeepWiki as Spec proof | Primary `llms.txt` for merge-critical |

---

## 6. Pointers for agents

- Search playbook: `adapters/claude/SEARCH.md`
- Polyglot depth: process/39–41
- Stack ★ bar: process/22
- MDC activation: process/47 + `.cursor/rules/`
