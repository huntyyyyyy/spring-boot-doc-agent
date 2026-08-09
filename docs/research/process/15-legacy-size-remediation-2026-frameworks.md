---
title: Legacy size-offender remediation — 2026 frameworks + intentionality (2026)
status: E-LEG0 APPROVED (2026-08-09) — this conversation (legacy must update; research modern frameworks)
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — grandfathered LOC debt across scanning/tools/pipeline/query/stf
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md
  - docs/research/modularity/13-tools-wave2-modularity-2026.md
  - docs/research/process/14-facade-poke-research-hooks-2026.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under 98.7, complexipy ≤5, or FILE_LOC_HARD 225
  - raise size/complexipy baselines to “make room”
  - mechanical part2 chops or utils/ grab-bags
  - DI containers, mesh/Backstage/ECS theater, Spec Kit WorkflowEngine runtime
  - ungated LLM multi-agent rewrite of the tip without MOD-S1 + poke + intentionality bar
  - treat ChaCo / VAPU / RefactorBench as merge SoT (sensors / process lessons only)
spec_gate: APPROVED E-LEG0 (2026-08-09) — LEG1–LEG10 (human: update legacy + 2026 framework research)
---

# Principal memo: pay down size-baseline legacy with 2026 design, not forever-grandfather

**Questions**

1. Must the ~30 `size_baseline.json` file offenders (>225 LOC) stay forever, or is there a Spec’d remediation program?
2. Which **2026** frameworks / papers / fitness tools should guide each wave — without category errors?
3. How do remediations avoid the **intentionality smells** (composite asserts, manual global state, multi-throw `raises`) that gate-gaming produces?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Leave >225 forever? | **No.** Grandfathering is a **debt ledger**, not a license. Remediations are the product stream after E-MOD3. `[Confirmed]` constitution + CONTRIBUTING |
| Raise 225? | **Refuse.** Split along concepts; `--update` only after shrink. `[Confirmed]` |
| 2026 stack for *this* CLI? | **Embody** DDD BCs + vertical slices + Protocol/Strategy ports (already E-MOD*); **Embody** tach boundary fitness; **Adopt** Feathers characterization + façade poke (E-FAC0); **Adopt** pytest `monkeypatch` + one-act exception tests as intentionality bar; **Adopt** OpenSpec-style SDD deltas; **Refuse** DI containers / mesh / ungated LLM-MAS tip rewrites. |
| First impl wave? | **E-SCAN1** — scanning BC (12 offenders, ~4029 LOC sum) under existing `ScannerBackend`. Then tools → pipeline → query → stf. |
| Tests during splits? | Prefer **separate assertions / methods**, `monkeypatch` for env/attrs/path, **one** invocation inside `pytest.raises` — never pack smells to dodge statement-growth. |

---

## 1. Confirmed debt inventory (this tip)

Source: `scripts/ratchets/size_baseline.json` (`schema_version` 2, `file_offender_count` **30**, `fn_offender_count` **0**). Hard = LOC **>225**; soft advisory 150–225. Roots: `src/doc_engine`, `src/stf`, `tests/` (`doc_engine.ci.size_ratchet`).

| BC cluster | n | Σ LOC (baseline) | Highest offenders |
| --- | --- | --- | --- |
| **scanning** | 12 | ~4029 | `_scanner_astgrep` 514, `gap_probe/registry` 482, `_build_signal_extract` 450, `facts` 442 |
| **tools** | 6 | ~1968 | `build_cross_group_edges` 438, `semantic_eval_helpers` 388, `pipeline_validators` 359 |
| **pipeline** | 5 | ~1624 | `local_runner_phases/support` 464, `compliance` 367, `live_gates` 319 |
| **query** | 4 | ~1151 | `packet` 346, `providers` 296, `rank` 259 |
| **stf** | 3 | ~879 | `ingest/review` 337, `validators/lint_tasks` 286, `__main__` 256 |

**Mechanism reminder `[Confirmed]`:** baselined offenders may remain >225 **only** at ≤ recorded LOC; new files >225 fail; offender-count must not rise; shrink + `--update` ratchets down. Outside roots (`scripts/`, `.cursor/hooks/`, …) are invisible to this gate — still prefer ≤225 cohesion.

---

## 2. Evidence inventory (2025–2026)

### 2.1 Architecture / process (primary)

| Claim | Tier | Source |
| --- | --- | --- |
| Spec-driven closed loop beats isolated prompts; prefer brownfield *delta* specs | Evidenced | Macedo arXiv:[2606.04967](https://arxiv.org/abs/2606.04967) (Spec Kit / OpenSpec taxonomy) — already Embody in segment 04 |
| Hexagonal / ports & adapters for I/O seams; outer wiring, inner logic | Evidenced | Cockburn lineage + 2026 practice (e.g. Hex CLI case studies); repo E-MOD* Protocol façades `[Confirmed]` |
| Vertical / semantic slices over type-layered `utils/` | Confirmed | segment 04 + constitution; E-MOD1–3 playbook |
| Multi-file refactors need dependency exploration + **structural** (AST) oracles, not string-exact only | Evidenced | RefactorBench arXiv:[2503.07832](https://arxiv.org/abs/2503.07832) (ICLR 2025) |
| Phased verify after modernization steps reduces silent breakage | Evidenced | VAPU arXiv:[2510.18509](https://arxiv.org/abs/2510.18509) — **Adopt** phase+verify; **Refuse** importing their multi-agent stack as tip runtime |
| PR last-mile patch-coverage augmentation is a *sensor*, not floor | Evidenced | ChaCo arXiv:[2601.10942](https://arxiv.org/abs/2601.10942) (ICSE 2026) — never substitute for 98.7 oracle |

### 2.2 Fitness tools (GitHub activity this session)

| Tool | Stars / push | Stance |
| --- | --- | --- |
| **tach** ([tach-org/tach](https://github.com/tach-org/tach)) | **2786★**, `pushed_at` **2026-06-11**, `updated_at` 2026-08-08 | **Embody** — already wired; keep as boundary SoT during splits |
| **import-linter** ([seddonym/import-linter](https://github.com/seddonym/import-linter)) | **1130★**, push **2026-08-07** | **Defer** dual-SoT unless tach leaves a *measured* gap (memo 14 FAC4) |
| **pytest** ([pytest-dev/pytest](https://github.com/pytest-dev/pytest)) | **14398★**, push **2026-08-09** | **Embody** — `monkeypatch` is the maintained temporary-mod API |

DeepWiki pages for tach / import-linter remain **Tier C orientation only** — re-verify against primary docs/`tach.toml` before any claim.

### 2.3 Intentionality (tests) — product rule from this conversation

Sonar-style findings (composite asserts that should be separate; prefer `monkeypatch`; one throw site in exception tests) are **intentionality**, not a license to weaken size/complexipy. Statement-growth in `check_code_quality.py` must not push agents to pack smells. `[Confirmed]` tip discussion + CONTRIBUTING size remediation prose.

---

## 3. Embody / Adopt / Refuse → LEG1–LEG10

| ID | Decision | Stance |
| --- | --- | --- |
| **LEG1** | Treat `size_baseline.json` offenders as an **ordered remediation backlog**, not permanent exceptions | Embody |
| **LEG2** | Never raise `FILE_LOC_HARD` (225) or complexipy ≤5; never raise offender maps without a shrink | Refuse weaken |
| **LEG3** | Each wave: MOD-S1 playbook — concept modules ≤225 + thin façade + Protocol/Strategy ports + same-commit `size-ratchet --update` | Embody (memo 12) |
| **LEG4** | Before/after split: façade **poke inventory** (`check_facade_poke_surface`) + characterization seams | Embody (E-FAC0) |
| **LEG5** | Design-shaped tip requires research Spec memo with arXiv + active GitHub (E-RES0 / E-CUR0) | Embody |
| **LEG6** | Wave order by BC debt & existing ports: **E-SCAN1 → E-TOOL4 → E-PIPE1 → E-QUERY1 → E-STF1** (names = epic IDs) | Adopt |
| **LEG7** | Keep **tach** as architecture fitness; do not dual-wire import-linter without Spec | Embody / Defer |
| **LEG8** | **Intentionality bar** on touched tests: prefer separate assert methods for distinct contracts; use pytest `monkeypatch` (not manual `sys.path`/`os.environ` edits); `raises` wraps **one** act | Adopt |
| **LEG9** | LLM-MAS / VAPU / ungated auto-refactor = **advisory process lesson** only; tip remains human+agent SDD with deterministic verify | Refuse as SoT |
| **LEG10** | ChaCo / climb / mutation = **sensors**; oracle Cover% 98.7 remains merge SoT (policy 16-A) | Embody DDIA |

Human Approve = this conversation (“legacy needs updated” + research modern 2026 frameworks while refactoring).

---

## 4. Epic tickets

| Epic | Status | Goal / Acceptance |
| --- | --- | --- |
| **E-LEG0** | **Done (this memo)** | Spec LEG1–LEG10 recorded; backlog wired; inventory table current |
| **E-SCAN1** | **Suggested next** (after E-MOD3 Archive) | Split ≥1 scanning offender cluster (prefer `_scanner_astgrep` / gap_probe / facts) via MOD-S1; poke green; size offender count ↓; complexipy ≤5; intentionality bar on touched tests |
| **E-TOOL4** | Later | Remaining tools giants (`build_cross_group_edges`, `semantic_eval_helpers`, …) after scan wave |
| **E-PIPE1** | Later | `local_runner_phases/support`, `compliance`, `live_gates` — ports at phase edges |
| **E-QUERY1** | Later | `packet` / `providers` / `rank` concept modules |
| **E-STF1** | Later | `stf` ingest/validators/`__main__` thin CLI |
| **LEG-S1** | Spike (optional) | “Does tach alone miss a coupling class that import-linter would catch on scanning?” Exit: measured gap or Defer |

**Exit (program):** `file_offender_count` trending to **0** without raising hard caps; each Archive tip leaves CONTRIBUTING / backlog stamps.

**Invariants:** fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** · Spec → Implement → Verify → Archive · claim tiers · DeepWiki Tier C only.

---

## 5. Adversarial checklist

- [ ] Did we propose raising 225 / complexipy? → **block**
- [ ] Is the split a `part2` / utils bag? → **block**
- [ ] Did we skip poke / characterization before façade move? → **block**
- [ ] Are tests packed to dodge CQ statement growth? → **rewrite for LEG8**
- [ ] Is ChaCo/VAPU cited as merge proof? → **demote to sensor**
- [ ] Dual tach+import-linter SoT without LEG-S1? → **Defer**
