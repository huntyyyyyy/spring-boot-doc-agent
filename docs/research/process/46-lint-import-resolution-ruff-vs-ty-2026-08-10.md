---
title: E-LINT0 — Import/lint SoT revisit (ruff vs ty / type checkers)
status: RESEARCH COMPLETE — Spec Draft (no Implement until Approve)
date: 2026-08-10
epic: E-LINT0
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - .ruff.toml
  - scripts/ci/pre_pr.py
sources:
  deepwiki_ask:
    - https://deepwiki.com/search/does-ruff-resolve-python-impor_44f053f2-1e5c-42e0-9501-88ed257f8634
    - https://deepwiki.com/search/for-catching-broken-topoffile_a6d46c28-5873-485a-8502-ecf459ab9408
    - https://deepwiki.com/search/what-is-the-difference-between_8e91c8bd-3da4-409d-a56d-2dfb2aa3a82f
  llms_txt:
    - https://docs.astral.sh/ruff/llms.txt
    - https://docs.astral.sh/ty/llms.txt
  deepwiki_pages:
    - https://deepwiki.com/astral-sh/ruff
    - https://deepwiki.com/astral-sh/ty
    - https://deepwiki.com/DetachHead/basedpyright
  mcp: https://mcp.deepwiki.com/mcp (ask_question / read_wiki_*)
---

# Principal memo: was ruff “premature,” and how do we catch bad top-of-file imports?

**Product:** `doc-engine` Python CLI · deterministic `pre_pr` / CI gates.  
**Question.** Operators hit green local lint then red remote on import/path bugs. Is Embody-ruff wrong? What tool actually catches **broken top-of-file imports** (`ModuleNotFoundError`) locally?

**Method.** Problem-first classes → Astral `llms.txt` + DeepWiki pages + **DeepWiki MCP `ask_question`** (context-grounded Q&A) → Embody/Adopt/Refuse for *this* repo. Cartography only via DeepWiki; primary docs via `docs.astral.sh/*/llms.txt` and rule pages.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Was choosing **ruff** premature? | **No as flake8+isort+pyflakes replace** — still correct Embody `[Confirmed]` / E-STACK0. **Yes if we treated ruff as enough for “import failures.”** Astral’s own FAQ: ruff is a **linter, not a type checker**; complementary to type checkers. |
| What catches **unused** top-of-file imports? | **ruff `F401`** (pyflakes) — already gated in `pre_pr` / python-gates. |
| What catches **unresolved** top-of-file imports (`import foo` not installed / not on path)? | **Type checker import resolution** — preferably **`ty check`** rule **`unresolved-import`** (default **error**). Not ruff. |
| Popular modern repo with “awesome features”? | **Astral** monorepo story: **`astral-sh/ruff`** (~49k★) now hosts **ruff + ty**; packaging mirror **`astral-sh/ty`** (~19k★). Shared parser/AST; different semantic depth. `llms.txt` + DeepWiki + MCP `ask_question` are the fast learn path. |
| Replace ruff with pylint / flake8 / mega-linter? | **Refuse** as lint SoT — worsens tip thrash (E-STACK0). Orchestrators (mega-linter / super-linter / trunk) **Refuse** as merge SoT. |
| Next product move | **Spike → Spec Approve → wire `ty check` (import-focused) in `pre_pr`**, keep ruff. Optional later: deptry for *declared*-deps hygiene (different predicate). |

**Bottom line:** The premature step was **conflating lint with import resolution**. Keep ruff; **add ty** (or one peer) for unresolved imports — do not dual-type-check forever.

---

## 1. Problem classes (do not collapse)

| Class | Failure | Tool that owns it *here* | Status |
| --- | --- | --- | --- |
| **L1 Unused import** | `import x` never referenced | ruff `F401` | **Embody** `[Confirmed]` |
| **L2 Undefined name** | typo’d symbol | ruff `F821` | **Embody** |
| **L3 Unresolved module** | `import foo` → `ModuleNotFoundError` | **ty `unresolved-import`** (or pyright `reportMissingImports`) | **Gap** — not gated |
| **L4 Possibly-missing symbol** | conditional export / optional member | ty `possibly-missing-import` (default ignore) | Spike only — FP risk |
| **L5 Import cycles** | A↔B | **tach check** | Embody cycles |
| **L6 Declared-deps drift** | requirements vs imports | deptry DEP001/002 | Spike / optional sensor |
| **L7 Architecture layers** | forbidden edges | tach / import-linter | E-TACH0 Draft; refuse dual-gate |

Operator pain (“unused / not import / dependency”) usually mixes **L1 + L3 + L6**. Ruff only closes L1/L2.

---

## 2. Evidence (tiers)

### 2.1 Astral primary docs `[Evidenced]`

- **ruff `llms.txt`:** “extremely fast Python **linter and formatter**”; replaces Flake8/Black/isort/… — not a type checker.  
  <https://docs.astral.sh/ruff/llms.txt>
- **ty `llms.txt`:** “extremely fast Python **type checker**” + LSP; CLI `ty check`.  
  <https://docs.astral.sh/ty/llms.txt>
- **ruff FAQ:** “Ruff is a linter, not a type checker… use Ruff **in conjunction with** a type checker… Ruff will notify you if an import is **unused**; a type checker catches other classes of errors.”  
  <https://docs.astral.sh/ruff/faq/>
- **ty `unresolved-import`:** default **error** — “import statements for which the module cannot be resolved” → runtime `ModuleNotFoundError`.  
  <https://docs.astral.sh/ty/reference/rules/#unresolved-import>
- **ty module discovery:** first-party via `environment.root` / `src`; third-party via venv (`.venv` / `VIRTUAL_ENV` / `--python`).  
  <https://docs.astral.sh/ty/modules/>
- **ty + ruff complementarity** (coming-from guide): stricter setups combine `[tool.ty.rules]` with `[tool.ruff.lint] extend-select = ["ANN","PYI"]`.  
  <https://docs.astral.sh/ty/coming-from-mypy-or-pyright/>

### 2.2 DeepWiki cartography + Ask `[Evidenced — DeepWiki]`

DeepWiki indexes public repos; **Ask** is available on the site and via **MCP** `https://mcp.deepwiki.com/mcp` tool **`ask_question`** (no auth for public repos). Prefer `llms.txt` + Ask over scraping SPA HTML.

| Ask (repo) | Grounded answer (compressed) |
| --- | --- |
| `astral-sh/ruff` — does ruff resolve missing modules? | **No** for `ModuleNotFoundError`. Linter tracks bindings for **unused** imports; **ty** in the same monorepo owns import resolution / missing-import diagnostics. [search](https://deepwiki.com/search/does-ruff-resolve-python-impor_44f053f2-1e5c-42e0-9501-88ed257f8634) |
| `astral-sh/ty` — broken top-of-file imports? | Rule **`unresolved-import`**; auto-detects `.venv` / `VIRTUAL_ENV`; **complements ruff**, does not replace it. [search](https://deepwiki.com/search/for-catching-broken-topoffile_a6d46c28-5873-485a-8502-ecf459ab9408) |
| ruff+ty — `unresolved-import` vs `possibly-missing-import`? | **`unresolved-import`**: module not found (e.g. not installed) — default **error**, CI should keep error. **`possibly-missing-import`**: symbol maybe missing inside a found module — default **ignore**, FP-heavy. [search](https://deepwiki.com/search/what-is-the-difference-between_8e91c8bd-3da4-409d-a56d-2dfb2aa3a82f) |

DeepWiki overview (cartography): ruff monorepo contains **ruff + ty** sharing parser/AST/Salsa; ty packaging lives in `astral-sh/ty` with `ruff/` submodule.  
<https://deepwiki.com/astral-sh/ruff> · <https://deepwiki.com/astral-sh/ty>

### 2.3 This repo `[Confirmed]`

- `.ruff.toml` selects `F,E,W,I,B,UP` — unused imports yes; **no** unresolved-module gate.
- `pre_pr` / `python-gates.yml`: `ruff check --no-cache scripts/ src/doc_engine/`.
- E-STACK0 **Embody ruff**; **Refuse** flake8+black return; **Defer** mypy/pyright as required gates; E-RUST0 already **Spike** ty/basedpyright.
- No deptry / pyright / ty pin today.

### 2.4 Peers (stars 2026-08-10 GH API) `[Evidenced]`

| Tool | ★ | Role vs L3 |
| --- | ---: | --- |
| astral-sh/ruff | 49122 | L1/L2 Embody |
| astral-sh/ty | 19434 | L3 preferred Spike (Astral stack fit) |
| microsoft/pyright | 15580 | L3 mature peer |
| python/mypy | 20588 | L3 peer; slower |
| DetachHead/basedpyright | 3523 | pyright fork + baseline; &lt;10k★ |
| facebook/pyrefly | 6864 | Rust TC; &lt;10k★ |
| pylint-dev/pylint | 5710 | Some import inference; &lt;10k; Refuse replace ruff |
| osprey-oss/deptry | 1457 | L6 only |
| oxsecurity/megalinter | 2550 | Orchestrator — Refuse SoT |

---

## 3. Cross-domain isomorphism (I1–I5)

| ID | Map |
| --- | --- |
| **I1** | Objects: *syntax lint graph* vs *module resolution graph*. Morphisms: unused-edge delete (ruff) vs missing-node detect (ty). |
| **I2** | CS landing: compilers split lexer/linter vs linker/resolver for decades; Astral FAQ states the same split. |
| **I3** | Map does **not** preserve: type soundness ≠ merge Cover%; ty beta ≠ ruff stable. |
| **I4** | Landing: **adapter/sensor** (`ty check` in `pre_pr`) — not substrate swap of entire quality SoT. |
| **I5** | Does **not** change fail_under 98.7 / complexipy / LOC — boolean SoTs stay. |

---

## 4. Embody / Adopt / Refuse / Spike

| Stance | Item |
| --- | --- |
| **Embody (continue)** | ruff for L1/L2/I/B/UP; tach cycles; existing complexipy/size/oracle |
| **Adopt (after Spec Approve)** | `ty check` hard (or advisory→hard) focused on **`unresolved-import`**; pin + doctor; document venv discovery |
| **Spike** | ty vs pyright on `scripts/`+`src/doc_engine/` FP budget; `possibly-missing-import` stay ignore; deptry L6 sensor |
| **Refuse** | Replace ruff with pylint/flake8; mega-linter/super-linter/trunk as merge SoT; dual type checkers forever; oxc/biome as Python SoT; softening oracle for ty noise |

---

## 5. Epic E-LINT0 (Spec → later Implement)

**Goal.** Close the **L3 unresolved top-of-file import** gap locally without undoing ruff Embody.

| ID | Ticket | Acceptance |
| --- | --- | --- |
| LINT0 | Spec Approve this memo + design stub | Human Approve recorded |
| LINT1 | Spike: `uvx ty check` / pinned ty on `scripts/`+`src/doc_engine/` | Written FP table; exit criterion ≤N unresolved-import on tip |
| LINT2 | Pin ty; `tool_doctor`; `pre_pr` suite `ty_imports` | Hard or advisory→hard; receipt in telemetry |
| LINT3 | CONTRIBUTING: L1–L6 table; refuse conflating ruff with ModuleNotFound | Claims paths resolve |
| LINT4 | Optional deptry Spike | Sensor only; not Cover% SoT |
| LINT-S1 | basedpyright/pyrefly bake-off | Only if ty Spike fails exit |

**Exit.** Local `pre_pr` fails closed on unresolved first-party/third-party imports that would `ModuleNotFoundError` under `.venv`, while ruff remains lint SoT.

**Invariants.** Constitution gates unchanged; one tip writer; no `PRE_PR_MODE=fast` for tip push.

---

## 6. Companion: session-log nest (E-LOG0) — Spec seed

**Problem.** `docs/process/session-log.md` is a ~5k-line monolith — hard to navigate; violates cohesion / look-first.

**Adopt structure (Draft):**

```text
docs/process/session-log/
  README.md          # index + how to append
  2026-07.md         # or 2026-07-23.md shards
  2026-08.md
docs/process/session-log.md  → stub pointing at nest (keep claims stable)
```

**Refuse:** chat dumps as research SoT; rewriting history entries.  
**Implement** only after Approve; may land after #119 / with E-LINT0 or as small process tip.

---

## 7. Adversarial checklist

- [ ] Do not “fix imports” by removing ruff  
- [ ] Do not enable `possibly-missing-import` as hard without FP budget  
- [ ] ty must use project `.venv` or CI will false-red on third-party  
- [ ] Scope `scripts/` + `src/doc_engine/` first (match ruff); expand tests later  
- [ ] DeepWiki Ask is a **sensor** — still cite `llms.txt` / rule pages for Spec claims  
- [ ] Session-log nest must not break `check_repo_claims` path predicates  

---

## 8. Agent note — how to use DeepWiki here

1. **Browse:** `https://deepwiki.com/<owner>/<repo>`  
2. **LLM index:** `https://docs.astral.sh/<tool>/llms.txt` (Astral) or project docs `llms.txt`  
3. **Ask:** site UI **or** MCP `POST https://mcp.deepwiki.com/mcp` → `tools/call` / `ask_question` with `repoName` + `question` (public, no auth)  
4. Treat Ask answers as **Evidenced — DeepWiki**; verify critical rules on primary docs before Implement
