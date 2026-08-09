---
title: E-CPL0 — Control-plane closed-loop (evidence-gated quality gates)
status: DRAFT Spec — pending Approve of CPL1–CPL12
research date: 2026-08-09
research_window: 2026-06-01 → 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`)
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/23-concern-to-solution-remedies-2026.md
  - docs/research/process/24-codegen-quality-dimensions-mechanism-depth-2026.md
  - docs/research/process/28-local-stalker-telemetry-etl-2026.md
  - docs/research/process/30-local-oracle-push-parity-2026.md
  - docs/research/process/31-stalker-path-parity-sensors-2026.md
  - docs/design/ddia-north-star/meta/effective-remedies.md
  - docs/research/quality-backlog.md
do_not:
  - Embody Nix/TEE/Kettle/HermBuild/SLSA-L3 as tip merge SoT
  - dual-wire Proof-or-Stop daemon or OTel/APM as SoT
  - adopt ArchUnitPython / new <10k★ linter as external SoR
  - treat Cover% or LLM-judge as proof the control plane is sealed
  - weaken fail_under / complexipy / size
spec_gate: DRAFT E-CPL0 (2026-08-09) — CPL1–CPL12 pending Approve
gh_sor_bar: "≥10000★ for new external SoR; Confirmed pins Embody-continue (pytest/tach/ast-grep)"
critique: >
  Human 2026-08-09: open-loop control of quality clones wherever a new gate
  lands without hermeticity + observability; one-suite patches do not stop cloning.
---

# Principal memo: control-plane closed-loop invariant

**Question.** How do modern frameworks, algorithms, and high-adoption repos
**close the quality control loop** so every new gate inherits hermeticity +
observability — instead of rediscovering plant asymmetry, empty logs, and
unstable SoT?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| What is the failure class? | **Open-loop control of the control plane** — actuators claim green without fail-closed witnesses on the same plant. `[Confirmed]` |
| What research names the fix? | **Evidence-gated lifecycle / Proof-or-Stop** (arXiv [2607.14890](https://arxiv.org/abs/2607.14890)): agent outputs are *claims*; transitions advance only on fresh, source-state-bound, mechanically verifiable evidence. `[Evidenced]` |
| What architecture practice installs it? | **Architecture fitness functions** (Ford / Parsons / Kua): objective, automated, continuous integrity checks on architectural *characteristics* — here: sealed observation, HEAD-bound harness, labeled predicates. `[Evidenced]` |
| What supply-chain papers transfer (pattern only)? | Hermetic sealed inputs (Bazel ★≥25k); attestation *shape* (in-toto / SLSA — receipt digests). **Refuse** TEE/Nix tip SoT for this CLI. `[Evidenced]` + product Refuse |
| What stops cloning? | One standing **control-plane closed-loop fitness** package (CPL-G*) that every gate must pass — not N instance patches. `[Confirmed]` + `[Evidenced]` |

```text
OPEN LOOP (today, recurring)              CLOSED LOOP (target)
────────────────────────────              ────────────────────
gate runs → exit code → "overall=pass"    gate runs → RECEIPT (body, digest,
empty suite.log still "green"             exit, HEAD pin, plant label)
dirty harness = "product red"             dirty harness = plant invalid
advisory soft-masks hard plant            hard plant cannot claim pass
sensor confused with SoT                  SoR named; sensors cannot promote
```

---

## 1. Source verification (hype filter)

| Source | Result | Tier | Product stance |
| --- | --- | --- | --- |
| arXiv [2607.14890](https://arxiv.org/abs/2607.14890) Proof-or-Stop | Evidence-gated lifecycle; agent-as-claim; receipts bind head hash + command + exit + output digest; ablation cuts visible-pass/hidden-fail amplification | `[Evidenced]` | **Adopt** *semantics* (claim ≠ state; proof-or-stop); **Refuse** embedding their daemon as product runtime |
| arXiv [2604.05080](https://arxiv.org/abs/2604.05080) Nidus | Persist only states that pass active verification gate; gate-sequence proof obligations with required witness types | `[Evidenced]` | **Adopt** “no overall=pass without witnesses”; **Refuse** write-ahead daemon theater |
| Ford *Building Evolutionary Architectures* | Fitness function = objective integrity assessment of architectural characteristic(s); triggered vs continual | `[Evidenced]` | **Embody** as remedy class (already SOL2 / effective-remedies) |
| ArchUnit ([TNG/ArchUnit](https://github.com/TNG/ArchUnit) ★~3794) | Rules-as-tests; architecture as CI fitness | `[Evidenced]` | **Adopt** pattern; **Refuse** Java runtime; pytest Confirmed vehicle |
| ArchUnitTS empty-rule protection | Vacuous match fails (silent false pass) | `[Evidenced]` | **Adopt** for empty suite.log / empty witness |
| Bazel hermetic builds ([bazelbuild/bazel](https://github.com/bazelbuild/bazel) ★~25695) | Sealed declared inputs → deterministic outputs | `[Evidenced]` | **Adopt** *hermetic plant* concept for gate inputs; **Refuse** Bazel as tip SoR |
| Nix ([NixOS/nix](https://github.com/NixOS/nix) ★~17476) + arXiv [2605.21089](https://arxiv.org/abs/2605.21089) TEE CI | Deterministic builds + TEE attestations | `[Evidenced]` | **Refuse** as tip merge SoT (supply-chain / hardware theater) |
| in-toto ★~1026 / SLSA ★~1906 / Kettle arXiv [2605.08363](https://arxiv.org/abs/2605.08363) | Provenance statements; subject digests; predicate types | `[Evidenced]` | **Adopt** *receipt shape* (subject digest + predicate); **Refuse** SLSA-L3 / TEE as gate SoT (`<10k★` also fails SOL8 for *new* SoR) |
| tach ★~2786 (Confirmed pin) | Python modular boundary fitness | `[Confirmed]` | **Embody-continue** structural fitness vehicle |
| pytest ★≥14k | Test-native fitness host | `[Evidenced]` | **Embody** CPL witnesses as pytest |
| ArchUnitPython ★~248 | ArchUnit-style Python | `[Evidenced]` | **Refuse** new SoR (`≪10k★`) |
| E-TEL0/1/2, E-HOOK2, oracle_push_policy | Local plant ≠ remote; G7–G10; telemetry ETL | `[Confirmed]` | Incomplete: suite logs still **0 bytes** on tip runs (2026-08-09) |
| E-CGQ0 / effective-remedies | Concern→Remedy→Depth→Witness Accept shape | `[Confirmed]` | CPL Spec must use CGQ3 rows |

---

## 2. Confirmed local open loops (this tip)

| Mechanism | Evidence | Failure shape |
| --- | --- | --- |
| **Vacuous telemetry** | `.git/pre-pr-telemetry/*/suites/*.log` size **0** on run `310f9200…` | Gate “observed” without body — Proof-or-Stop would reject receipt |
| **Advisory soft overall** | `pre_pr._suite`: `kind=="advisory"` never fails overall | Sensor without actuator bite when mislabeled |
| **Harness dirt as product red** | Dirty `spring-signals/harness/check-assertions.py` ≡ mutant M8 → mutation entrypoint fails | Plant ≠ HEAD; no preflight witness |
| **Plant asymmetry (historical)** | Local `--skip-coverage` vs remote fail_under | Open loop push actuator (E-HOOK2 sealed partially) |
| **CodeQL always-run / skip blind** | Fingerprint gate fail-closed → run | Absence of skip witness ≠ free skip; waste if always dirty |

These are **one class**: missing fail-closed witness on the control plant.

---

## 3. Remedy mechanisms (depth for CPL)

### 3.1 Evidence-gated lifecycle (Proof-or-Stop / Loop Engineering)

| Depth | Content |
| --- | --- |
| Theory | Claim admissibility: actor output proposes lifecycle claim; gate admits iff evidence satisfies predicate bound to tracked source state |
| Math / algo | Receipt `R = (cmd, args, cwd, exit, out_digest, head_hash, policy_hash)`; admit iff `fresh(R) ∧ bind(R, HEAD) ∧ predicate(R)` |
| DS | Per-suite receipt + index ledger (already TEL `index.json` shape) |
| ETL | Suite stdout/stderr → non-empty body → digest → excerpt (success *and* fail) |
| Traversal | Before interpreting any red/green: verify receipts → else STOP (no design pass) |

**Stance:** **Adopt** semantics into `pre_pr` / stalker; **Refuse** vendor daemon.

### 3.2 Architecture fitness function (Ford)

| Depth | Content |
| --- | --- |
| Theory | Protect architectural *characteristics* with objective continuous checks |
| Characteristic here | Control-plane closed-loop: hermetic inputs, full observation, labeled predicates, single tip writer |
| Vehicle | pytest tests + `pre_pr` hard fail — not README |

**Stance:** **Embody** CPL-G* as standing fitness (SOL2 / CGQ).

### 3.3 Hermetic plant (Bazel concept transfer)

| Depth | Content |
| --- | --- |
| Theory | Outputs determined only by declared sealed inputs |
| Transfer | Mutation engine input = `HEAD` blob of harness, not dirty WT; oracle predicate = labeled `mode=oracle` |
| Refuse | Full Bazel/Nix rewrite |

### 3.4 Vacuous-witness fail-closed (ArchUnit empty-rule)

| Depth | Content |
| --- | --- |
| Theory | A check that matches nothing / observes nothing must fail |
| Transfer | Hard suite with `log_bytes==0` ⇒ overall cannot pass; empty fingerprint skip ⇒ run (already CQL fail-closed) |

### 3.5 Single-write-derive (already Embodied)

Oracle XML vs climb; sensors cannot promote. CPL adds: **overall=pass is a derived claim** that may only derive from admissible hard receipts — never from narrative.

---

## 4. Embody / Adopt / Refuse

| Item | Stance |
| --- | --- |
| Proof-or-Stop claim≠state + receipt binding | **Adopt** (semantics) |
| Ford fitness functions for control-plane characteristics | **Embody** |
| Empty-log / empty-witness fail-closed | **Embody** |
| HEAD-bound mutation harness preflight | **Embody** |
| Labeled oracle vs climb predicates (16-A / HOOK) | **Embody-continue** |
| pytest as fitness host (≥10k★) | **Embody** |
| tach / ast-grep / ruff Confirmed wheels | **Embody-continue** |
| Suite telemetry ETL non-empty body (TEL repair) | **Embody** (fix landed E-TEL incomplete witness) |
| Nix / TEE / Kettle / HermBuild / SLSA-L3 tip SoT | **Refuse** |
| Proof-or-Stop / Nidus product runtime | **Refuse** |
| ArchUnitPython / new low-★ arch linter as SoR | **Refuse** |
| OTel/APM as tip SoT | **Refuse** (TEL) |
| LLM-judge / scoped Cover% as closed-loop proof | **Refuse** |

---

## 5. Spec decisions (CPL1–CPL12) — pending Approve

| ID | Decision |
| --- | --- |
| **CPL1** | Control-plane closed-loop is a **first-class architectural characteristic** protected by standing fitness (not chat diagnosis) |
| **CPL2** | Every `pre_pr` **hard** suite must produce a **receipt**: non-empty log body *or* explicit skip receipt with reason code; else overall≠pass |
| **CPL3** | Success receipts still keep WARNING/advisory excerpts (Proof-or-Stop: green≠silent) |
| **CPL4** | Mutation / assertion harness: refuse run if engine file bytes ≠ `HEAD` (hermetic plant); dirt is plant-invalid, not product-red |
| **CPL5** | `overall=pass` is a **derived claim** admitted only when all hard suite receipts are admissible (agent narrative never suffices) |
| **CPL6** | Advisory suites cannot authorize merge/push; mislabeled hard-as-advisory fails G7/G10 parity sensors |
| **CPL7** | New gates MUST register: SoR\|derived label, local↔remote plant map, receipt path, fitness witness test — else Spec incomplete (CGQ3) |
| **CPL8** | Adopt Proof-or-Stop / Nidus **semantics only**; refuse their daemons and TEE CI as tip SoT |
| **CPL9** | ≥10k★ bar for new external SoR; pytest/tach/ast-grep remain vehicles |
| **CPL10** | CodeQL / expensive suites: fingerprint skip is the *only* sealed skip; fail-closed → run; no silent always-skip |
| **CPL11** | Multi-workspace / N tips: one tip writer; cross-worktree coverage combine remains Refuse; receipts bind to **this** worktree HEAD |
| **CPL12** | Instance patches for open-loop incidents without expanding CPL-G* fitness = **Fail** (SOL6 clone) |

---

## 6. Epic sketch

### E-CPL0 — Spec gate (this memo + design)

Exit: human Approve CPL1–CPL12; design memo status → APPROVED.

### E-CPL1 — Implement (only after Approve)

| Ticket | Title | Acceptance |
| --- | --- | --- |
| CPL1-1 | Fix tee/capture so suite logs non-empty (TEL repair) | Live sink + post-`with` read; pytest proves inside+after; integration: log size>0 after hard suite |
| CPL1-2 | `control_plane_receipts` fitness | Hard suite with empty body ⇒ overall fail; unit tests |
| CPL1-3 | Harness HEAD pin | `mutation_driver` / assertion entry refuse dirty engine vs HEAD; tests with planted dirt |
| CPL1-4 | Success excerpt ratchet | WARNING on exit 0 appears in index excerpt |
| CPL1-5 | Gate registry stub | Doc + claims predicate: new hard suite lists SoR\|derived + receipt path |
| CPL1-6 | Archive | CONTRIBUTING / session-log only if steering moves |

### Explicit Defer

- SLSA provenance upload, TEE CI, Nix hermetic rebuild — Defer until supply-chain epic; not required to close *this* loop.
- Full Proof-or-Stop product — Refuse.

---

## 7. Adversarial checklist

- [ ] Does Accept only say “fix empty logs” without standing fitness? — **Fail CPL1/CPL12.**
- [ ] Is TEE/Nix offered as the merge SoT? — **Fail CPL8.**
- [ ] Can overall=pass with 0-byte suite logs? — **Fail CPL2/CPL5.**
- [ ] Can dirty harness be interpreted as product mutation failure? — **Fail CPL4.**
- [ ] Is Cover% used as proof the control plane is sealed? — **Fail Refuse.**
- [ ] New gate without SoR\|derived + receipt path? — **Fail CPL7.**

---

## 8. Exit

**E-CPL0 DRAFT** until human Approve of CPL1–CPL12.

This memo answers the critique: recurrence is **open-loop control cloning**.
Modern remedy is **evidence-gated fitness on the control plane** (Proof-or-Stop
semantics + Ford fitness + hermetic plant + vacuous-witness fail-closed),
installed once as CPL-G*, not rediscovered per suite.
