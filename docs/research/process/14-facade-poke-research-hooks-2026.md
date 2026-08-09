---
title: Façade poke-surface fitness + design-research hooks (2026)
status: E-FAC0 / E-RES0 / E-CUR0 APPROVED (2026-08-09) — Cursor-native hooks this tip
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — agent hooks + CI fitness functions
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md
  - docs/research/modularity/13-tools-wave2-modularity-2026.md
  - docs/process/steering-prompts/00-shared-research-standards.md
  - .cursor/skills/principal-se-research-epic/SKILL.md
do_not:
  - treat LLM-judge or Cover% climb as merge SoT for façade correctness
  - adopt DI containers or microservice decomposition theater for this CLI
  - replace tach (already Adopted) with a second conflicting architecture linter without Spec
spec_gate: APPROVED E-FAC0 + E-RES0 + E-CUR0 (2026-08-09) — FAC1–FAC6 · RES1–RES6 · CUR1–CUR4
---

# Principal memo: why modularity splits leaked CI, and how to catch it in any tip

**Questions**

1. How did E-MOD3 miss ruff / domain markers / kitchen `run_manifest.json` after a “green” local loop?
2. What *general* fitness functions catch god-file façade splits in a modern high-quality Python codebase?
3. How do we **force** contextual 2026 research (arXiv + active GitHub + DeepWiki orientation) on ambiguous / design-shaped asks — not hope the agent remembers the skill?

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Root miss class? | **Process gap + incomplete characterization inventory** — not “LOC too high alone.” Agent ran a pytest *subset*; `pre_pr --fast`/`ad-hoc` skipped CI hard surface; façade DIP re-exported `os`/`subprocess` but not every name tests `patch.object` (`json`). `[Confirmed]` |
| Catch god-split regressions generally? | **Characterization poke-surface gate** (inventory of patched attrs → façade must expose them) + **parity pre_pr ↔ python-gates** + existing **tach** boundaries. `[Evidenced]` Feathers seams + `[Confirmed]` this repo’s climb/kitchen patches |
| Force research? | Skill/constitution text is **not** a control. Add a **commit PreToolUse hook** (same pattern as `require_hardened_tests.py`) + receipt that research tiers were filed. `[Confirmed]` repo hook doctrine |
| Microservices / MARS / VAPU full autonomy? | **Refuse** for this one-CLI product. Adopt *verification-after-phase* and *test-oracle-before-refactor* ideas only. |

---

## 1. Incident autopsy (Confirmed)

| Failure | Where | Why local missed it |
| --- | --- | --- |
| ruff I001 | python-gates | Scoped ruff / no `pre_pr --auto` full `scripts/`+`src/` |
| domain markers | python-gates **3.11 only** | New test filename not in `FilenamePrefixRule`; `pre_pr` historically omitted markers (now added) |
| kitchen Ch07 `run_manifest.json` | ABI serial | Climb tests patched `os`/`subprocess`; kitchen patched `json.dump` — not in the hand inventory |
| 3.12 / matrix noise | fail-fast cancel | Looked like multi-version product bugs; was cascade |

**Lesson (DDIA):** boolean SoT is CI hard gates; a green sensor (scoped pytest) is not merge proof. Same vocabulary as Cover% oracle vs climb.

**Lesson (SOLID/OCP):** thin façade is an Anti-Corruption Layer. Late-import DIP only works if **every** characterization seam is on the façade. Hand checklists fail; inventory the *tests*.

---

## 2. Evidence inventory (tiers)

### 2.1 Characterization / seams / golden masters

| Claim | Tier | Source |
| --- | --- | --- |
| Characterization tests pin *current* behavior before refactor; seams enable monkeypatch without editing call sites | Evidenced | Feathers *Working Effectively with Legacy Code* practice (secondary digest: techdebt.now characterization technique; skill distillations cite same algorithm) |
| pytest `monkeypatch.setattr` is the maintained Python seam API | Evidenced | [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest) — **14398★**, `pushed_at` **2026-08-09** (GitHub API this session) |
| Approval / golden-master tests for opaque outputs | Evidenced | [`approvals/ApprovalTests.Python`](https://github.com/approvals/ApprovalTests.Python) — **209★**, push **2026-08-09** (below star floor of 00 but *active*; note weakness) |
| Refactor agents need AST/structure tests, not string-exact only | Evidenced | RefactorBench (ICLR 2025) — multi-file refactor tasks evaluated by structural tests |
| Multi-agent legacy updaters gain from phased verify | Evidenced | VAPU arXiv:[2510.18509](https://arxiv.org/abs/2510.18509) — verifying agent pipeline; **Refuse** importing their full stack; **Adopt** phase+verify |

### 2.2 Architecture fitness functions (Python 2025–2026)

| Tool | Stars / activity | DeepWiki | Stance for *this* CLI |
| --- | --- | --- | --- |
| **tach** (`tach-org/tach`) | **2786★**, release v0.35.0 (2026-05-12), push 2026-06-11 · [github.com/tach-org/tach](https://github.com/tach-org/tach) | Indexed (orientation 2025-12-17) — re-verify claims against `tach.toml` / docs.gauge.sh | **Embody** — already in `requirements-dev.txt` + quality-gates |
| **import-linter** (`seddonym/import-linter`) | **1130★**, push **2026-08-07**, PyPI 2.13 (2026-07-03) · [github.com/seddonym/import-linter](https://github.com/seddonym/import-linter) | Indexed (2025-12-25) — layered contracts via grimp | **Adopt carefully** as *complement* only if tach contracts leave a proven gap; **Refuse** dual SoT thrash without Spec |
| Microservice decomposition RL (MARS / similar) | IEEE 2025 | N/A | **Refuse** — product is one Python CLI with BCs, not a mesh |

### 2.3 This repo’s own controls (Confirmed)

| Control | Forces research? | Forces façade poke completeness? |
| --- | --- | --- |
| `principal-se-research-epic` skill + constitution prose | No (advisory) | No |
| `deny_raw_network` / `deny_text_search` | Forces *channel* (WebFetch / ast-grep), not *that* research happened | No |
| `require_hardened_tests` on `git commit` | No | No |
| `pre_pr --auto` | No | Partial (markers now; still no poke inventory) |
| Climb / kitchen monkeypatches | No | Partial — only attrs someone remembered |

**Unknown:** whether Cursor Cloud PreToolUse can see user-query text for “research ask” classification (may need Agent-tool matcher + prompt heuristics). Spec locks Claude-plugin commit hook first; Cursor rule points at same skill.

### 2.4 Cursor-native hooks portability (E-CUR0)

| Claim | Tier | Source |
| --- | --- | --- |
| Cloud agents load **project** `.cursor/hooks.json` command hooks; user `~/.cursor/hooks.json` is **not** available in Cloud VMs | Evidenced | [Cursor Hooks docs — Cloud agent support](https://cursor.com/docs/hooks) (fetched this session) |
| `beforeShellExecution` + `preToolUse` are supported on Cloud; exit 0 + JSON `permission` deny/allow | Evidenced | same docs — Supported hooks table + `beforeShellExecution` / `preToolUse` schemas |
| Claude `Bash` ↔ Cursor `Shell`; Claude `PreToolUse` ↔ Cursor `preToolUse` / shell-specific `beforeShellExecution` | Evidenced | Cursor docs tool schemas; Claude plugin hooks under `adapters/claude/hooks/` `[Confirmed]` |
| Optional Claude third-party hook import in Cursor is **not** a reliable Cloud SoT | Confirmed | this tip’s local-green / remote-red gap: Claude hooks did not fire on Cloud commits |

---

## 3. Embody / Adopt / Refuse → FAC1–FAC6 · RES1–RES6

### Façade / modularity fitness (E-FAC0)

| ID | Decision | Stance |
| --- | --- | --- |
| **FAC1** | Before/after god-module splits, build a **poke-surface inventory** from tests: `monkeypatch.setattr(mod, name)`, `patch.object(mod, name)`, `patch("pkg.mod.name")` where `mod` is a stable façade | Embody (Feathers seams + Confirmed incident) |
| **FAC2** | Deterministic gate: every inventoried name must exist on the façade module object (or be documented exempt with reason) | Adopt |
| **FAC3** | Local `pre_pr` standard must stay a **superset of fast CI hard checks** that catch split hygiene (ruff, markers, poke gate); oracle Cover% + quality-gates remain CI SoT | Embody (DDIA SoT vs sensor) |
| **FAC4** | Keep **tach** as boundary fitness; do not silently add import-linter contracts in the same tip | Embody / Defer |
| **FAC5** | Domain marker classifier alignment is part of split DoD (filename prefix rules) | Confirmed / Embody |
| **FAC6** | Refuse raising LOC/complexipy caps to “make room” for gods | Refuse |

### Research-forcing (E-RES0)

| ID | Decision | Stance |
| --- | --- | --- |
| **RES1** | Design-shaped commits (ports/strategies/SoT/gates/new research memos that claim architecture) require a `docs/research/*` file in the tip with `spec_gate:` + claim-tier vocabulary | Embody (skill → control) |
| **RES2** | That memo must cite **≥1 arXiv abs URL that resolves**, **≥1 GitHub repo with stars+`pushed_at` within ~18 months**, and note DeepWiki as **orientation only** (Tier C — never sole citation) per steering `00` / `10` | Adopt |
| **RES3** | Enforce at **`git commit` PreToolUse** (fast, fail-open on hook crash, fail-closed on finding) — same doctrine as `require_hardened_tests.py` | Embody |
| **RES4** | Ambiguous user asks (“how should we…”, “research…”, “modern approach…”) → agent **must** load `principal-se-research-epic` before Write to `src/` (Cursor alwaysApply + Claude Agent instruction); mechanical commit hook still backs it | Adopt |
| **RES5** | Refuse LLM-as-judge as research Spec gate; refuse DeepWiki-only “evidence” | Refuse |
| **RES6** | One tip writer; research memo + fitness gate land before claiming Archive on modularity tips | Embody SDD |

### Cursor-native policy portability (E-CUR0)

| ID | Decision | Stance |
| --- | --- | --- |
| **CUR1** | Ship project `.cursor/hooks.json` so Claude PreToolUse policies run in Cursor Desktop **and** Cloud without third-party Claude import | Embody |
| **CUR2** | Keep policy SoT in `adapters/claude/hooks/` + `.claude/hooks/`; thin `.cursor/hooks/bridge_claude_policy.py` only normalizes stdin/stdout (Shell→Bash, Claude deny → Cursor `permission`) | Embody (DRY / OCP) |
| **CUR3** | Wire `beforeShellExecution` for Bash-equivalent policies; `preToolUse` matcher `Grep` for the Grep tool (Shell already covered by beforeShell — do not double-run) | Adopt |
| **CUR4** | Refuse depending on `~/.cursor/hooks.json` or Claude third-party toggle as the Cloud control plane | Refuse |

Human Approve = this conversation’s request for a general catch + research hook (2026-08-09), plus native Cursor PreToolUse portability (same thread).

---

## 4. Epic tickets

| Epic | Status | Goal / exit |
| --- | --- | --- |
| **E-FAC0** | **Active (this tip)** | Ship `check_facade_poke_surface` + wire pre_pr/CI; inventory covers `run_manifest` / known façades |
| **E-RES0** | **Active (this tip)** | Ship `require_design_research` commit hook + wire `.claude/settings.json` / plugin hooks; AGENTS pointer |
| **E-CUR0** | **Active (this tip)** | Ship `.cursor/hooks.json` + bridge; Grep + shell policies fire on Cursor Cloud/Desktop; tests for normalize/deny map |
| **E-FAC1** | Suggested next | Expand inventory auto-discovery; optional approvaltests for opaque CLI golden masters — only if poke gate false-negatives recur |
| **E-RES1** | Superseded by E-CUR0 | Was “Cursor-native hook if PreToolUse parity differs” — landed as E-CUR0 |

---

## 5. Explicit refuse

- Microservice / mesh decomposition frameworks as default modernization  
- Dual tach + import-linter SoT without a measured gap  
- Research theater (paste DeepWiki prose as `[Evidenced]`)  
- Softening fail_under / LOC / complexipy  

---

## Invariants

fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** · Spec → Implement → Verify → Archive · claim tiers · DeepWiki Tier C only.
