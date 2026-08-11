---
title: E-SCAN1 — AstGrepBackend modularity (scanning/astgrep)
status: E-SCAN1 APPROVED (2026-08-09) — plan accept attached Spec
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — Stage-0 ast-grep scanner backend
related:
- docs/research/bounded-contexts/12-pipeline-stage0-modularity-ports-2026.md
- docs/research/se-quality-synthesis-2026-08-08.md
- docs/research/quality-backlog.md
do_not:
- weaken fail_under 98.7, complexipy ≤5, FILE_LOC_HARD 225
- land on E-MOD3 tip; wire import-linter dual-SoT; DI containers; utils/
- swap to ast-grep-py / in-tree Rust; ApprovalTests goldens; ChaCo as floor
- split all scanning offenders in one tip
spec_gate: APPROVED E-SCAN1 (2026-08-09) — SCAN1-A–J
last_reviewed: '2026-08-10'
---

# Principal memo: E-SCAN1 AstGrepBackend split

**Question:** How do we pay down `_scanner_astgrep.py` (514 LOC) with MOD-S1 standards and
elegant 2026 product-fit (not generic Refuse theater)?

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| First offender? | `_scanner_astgrep.py` only — layout `scanning/astgrep/` + thin façade |
| `version_hash`? | CodeQL-style `_version_hash_paths()` over façade + package + rules |
| tach / import-linter? | tach.toml unchanged; IL Defer; optional neutral `errors` module |
| Elegant now? | Structure AST tests · VAPU phases · LEG8 monkeypatch · `AstGrepRunner` Protocol |
| Branch? | `cursor/e-scan1-astgrep-61f3` off main (not MOD3 tip) |

## 1. Confirmed seams

| Fact | Evidence |
| --- | --- |
| LOC 514 | `src/doc_engine/scanning/_scanner_astgrep.py` |
| Ports | `Scanner` Protocol + `ScannerBackend` ABC; registry `"ast-grep"` |
| Hash gap | hashes only `__file__` + rules; CodeQL/filesystem multi-file lists exist |
| Soft cycle | `_astgrep_errors` → `spring.AstGrepError`; `spring` → registry → backend |
| Poke | `chunk_paths_for_argv`, `_PATH_LIST_CHAR_LIMIT`, `_invoke_ast_grep`, `subprocess` |
| tach.toml | single `doc_engine` module — new subpackage needs no config edit |
| Pin | `ast-grep-cli~=0.45.0`; patch cov via existing diff-cover |

## 2. Evidenced external

| Claim | Tier | Source |
| --- | --- | --- |
| Structural/AST oracles for multi-file refactors | Evidenced | RefactorBench [arXiv:2503.07832](https://arxiv.org/abs/2503.07832) |
| Phase + verify; refuse MAS tip runtime | Evidenced | VAPU [arXiv:2510.18509](https://arxiv.org/abs/2510.18509) |
| Patch-coverage sensor ≠ oracle floor | Evidenced | ChaCo [arXiv:2601.10942](https://arxiv.org/abs/2601.10942) |
| SDD brownfield Spec | Evidenced | Macedo [arXiv:2606.04967](https://arxiv.org/abs/2606.04967) |
| ast-grep active CLI | Evidenced | [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) ★ / push 2026-08 |

DeepWiki = Tier C orientation only.

## 3. Deep product-fit

| Framework | Verdict | Elegant use here |
| --- | --- | --- |
| tach | Defer config | No `tach.toml` edit |
| import-linter | Defer wire | Move errors to `astgrep/errors.py`; spring re-exports |
| RefactorBench | Elegant now | Structure tests on façade exports + hash paths |
| VAPU | Process only | Spec → argv → invoke → ingest/hash/poke verify |
| ChaCo | Already covered | Rely on diff-cover; no second sensor |
| AstGrepRunner | Adopt | Protocol + subprocess adapter; no DI |
| monkeypatch LEG8 | Elegant now | Convert touched `mock.patch` suites |
| ast-grep-py / Rust | Refuse | CLI pin sufficient |
| ApprovalTests | Refuse | Field asserts + structure tests |

## 4. Spec decisions SCAN1-A–J

| ID | Decision |
| --- | --- |
| **SCAN1-A** | Keep ScannerBackend ABC + Scanner Protocol; stable façade import |
| **SCAN1-B** | `scanning/astgrep/` + thin `_scanner_astgrep.py` |
| **SCAN1-C** | `_version_hash_paths()` over façade + `astgrep/*.py` + rules |
| **SCAN1-D** | Poke inventory + façade re-exports |
| **SCAN1-E** | LEG8 on touched tests |
| **SCAN1-F** | Structure characterization tests |
| **SCAN1-G** | VAPU-shaped phased verify; Refuse MAS |
| **SCAN1-H** | tach unchanged; IL unwired; neutral errors module |
| **SCAN1-I** | `AstGrepRunner` Protocol |
| **SCAN1-J** | Refuse raise 225, DI, ApprovalTests, ast-grep-py, all-12 split |

## 5. Adversarial checklist

- [ ] version_hash under-hashing after split → use `_version_hash_paths`
- [ ] WinError-206 / `_PATH_LIST_CHAR_LIMIT` poke break → façade re-export
- [ ] Covering receipt desync → keep receipt builders cohesive
- [ ] Import cycle registry↔spring → errors module
- [ ] Scoped pytest green ≠ gates → `pre_pr --auto`

## Invariants

fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** · Spec → Implement → Verify → Archive
