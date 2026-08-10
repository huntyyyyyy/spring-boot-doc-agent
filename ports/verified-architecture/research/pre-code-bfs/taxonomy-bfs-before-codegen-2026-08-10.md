---
title: Pre-code BFS domain taxonomy — classify before AI generates code
status: RESEARCH COMPLETE — Spec Draft
date: '2026-08-10'
claim_tiers: Evidenced / Confirmed / Unknown
bloom_gate: required-through-create
audience: [developer, agent, rag]
related:
  - research/papers-2026-may-aug/README.md
  - research/INDEX.md
  - 11-science-transfer/locked-transfers/README.md
  - docs/standards/no-code-gate.md
---

# Pre-code BFS — domains, models, workflows before AI codegen

**Method.** Breadth-first enumeration of every concern that must be *classified and
gap-closed* before an agent is allowed to emit product code. Depth (filling each
folder) comes after this map is stable.

**Hard rule.** Incomplete QAS, unresolved `blocks-code` open questions, and
Proposed ADRs without alternatives packs **do not** authorize Design influence
or `Cargo.toml` / `pyproject` product trees.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is the current tree deep enough? | **No** — flat `docs/` + language nests encode answers early |
| Correct nesting axis | **Lifecycle concern → problem → open gap → decision** |
| Language monorepo scaffold | **Demote** to `07-system-design/options/` until ICDs + QAS exist |
| Science substrates (neuromorphic, PRC, IMC…) | **Refuse tip**; locked transfers only (see §5) |
| RE-MASTER-001 AI draft | **Severe critique required** — theater metrics + model lock-in (§6) |
| Next gate | Fill BFS Level-0…3 gap templates; Approve wave-1 Must REQs |

---

## 1. BFS levels (classification)

Process order is **left-to-right by level**. Do not deep-dive Level 4 until Level
1–3 gaps for that wave are closed.

### Level 0 — Governance (always on)

| Domain | Folder | Workflow before code |
| --- | --- | --- |
| Constitution / DoR / DoD | `00-governance/` | Machine-checkable Definition of Ready for each wave |
| Claim tiers | `00-governance/claim-tiers/` | Evidenced / Confirmed / Unknown discipline |
| Promotion | `00-governance/promotion/` | research → docs only via explicit promote |

### Level 1 — Problem & people

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| Vision / problem frame | `01-vision/` | One-sentence system boundary (verify engine ≠ RAG SaaS confusion) |
| Non-goals | `01-vision/non-goals/` | Explicit refuse list |
| Success measures | `01-vision/success-measures/` | Wave-scoped Accept predicates |
| Stakeholders / actors | `02-stakeholders/actors/` | Who cares; measurable proxy |
| OpsCon | `02-stakeholders/opscon/` | Local vs org modes as *concepts*, not infra theater |
| Sign-off log | `02-stakeholders/signoff/` | Human Approve trail |

### Level 2 — Requirements & constraints (separate)

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| StRS | `03-requirements/strs/` | Needs without implementation |
| SRS | `03-requirements/srs/` | Impl-free REQ-*; MoSCoW |
| Use cases / abuse cases | `03-requirements/use-cases/` | Happy + adversarial paths |
| QAS (ATAM six-part) | `03-requirements/qas/` | **Every Must NFR** = stimulus→…→measure |
| RTM | `03-requirements/rtm/` | need↔REQ↔design↔accept + **gap column** |
| Waves / MoSCoW | `03-requirements/moscow-waves/` | Wave-1 Must closed set |
| Constraints | `04-constraints/*` | Fixed; change needs ADR |
| Assumptions | `04-constraints/assumptions/` | ASSUM-* + invalidate condition |
| Open questions | `04-constraints/open-questions/` | OQ-* `blocks-code` flag |

### Level 3 — Quality architecture & domain model

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| ATAM utility tree | `05-quality-architecture/atam/` | Prioritized scenarios |
| Tactics | `05-quality-architecture/tactics/` | Tactic → QAS map |
| Tradeoffs / sensitivity | `05-quality-architecture/tradeoffs/` | Named conflict points |
| Formal boundaries | `05-quality-architecture/formal-boundaries/` | trust-boundary vs proved |
| Ubiquitous language | `06-domain/ubiquitous-language/` | Lock, receipt, Unknown, SoR |
| Bounded contexts | `06-domain/bounded-contexts/` | **Problem BCs**, not languages |
| Information model | `06-domain/information-model/` | Registry / graph / receipt schemas |

### Level 4 — System design (still pre-code)

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| C4 Context+Container | `07-system-design/c4/` | Cite ADR IDs; **no Code level yet** |
| Ports & adapters | `07-system-design/ports-and-adapters/` | Index, Registry, Resolve, LockCheck, Receipt |
| ICDs | `07-system-design/icd/` | Inter-BC contracts |
| ADRs | `07-system-design/adr/` | Nygard; Accepted vs Proposed |
| Options | `07-system-design/options/` | Language/tech candidates + Pilot/Refuse |

### Level 5 — Verification stack & product tours

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| L1 Navigate | `08-verification/l1-navigate/` | tree-sitter / sg / SCIP predicates |
| L2 Policy | `08-verification/l2-policy/` | locks / MDC / claims boolean SoR |
| L3 Proof | `08-verification/l3-proof/` | Z3/Kani/WASM — optional; own Accept |
| Receipts | `08-verification/receipts/` | Proof-tour schema |
| V&V plan | `08-verification/vv-plan/` | Fixture specs named |
| Five tours | `09-product-tours/*` | MoSCoW: v1 = receipts+locks; LSP/ghost/bell Pilot |

### Level 6 — RAG product surface & science transfer

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| Corpus catalog | `10-rag-corpus/catalog/` | INDEX / pack manifests |
| Retrieval contracts | `10-rag-corpus/retrieval-contracts/` | Retrieve ≠ verify |
| RAG eval | `10-rag-corpus/eval/` | Faithfulness measures (when RAG is in-wave) |
| Locked transfers | `11-science-transfer/locked-transfers/` | Only allowed metaphors |
| Refuse substrates | `11-science-transfer/refuse-substrates/` | DNA/CRN/ionic/… stay science |
| Papers | `11-science-transfer/papers/` + `research/papers-2026-may-aug/` | Cross-ref evidence |

### Level 7 — Delivery gate

| Domain | Folder | Must answer before code |
| --- | --- | --- |
| Waves | `12-delivery/waves/` | Wave charter |
| Spike charters | `12-delivery/spike-charters/` | Question + keep/drop |
| No-code gate | `12-delivery/no-code-gate/` | Checklist = DoR |
| Pilot-before-Refuse | `12-delivery/pilot-before-refuse/` | Per-BC language Pilot rules |

---

## 2. Models that must exist as *artifacts* (not chat)

| Model | Kind | Pre-code artifact |
| --- | --- | --- |
| Stakeholder model | Social | Actors + OpsCon |
| Requirements model | Spec | StRS/SRS/RTM |
| Quality model | ATAM | Utility tree + QAS files |
| Constraint model | Fixed | CON-* ledger |
| Domain model | DDD | Ubiquitous language + BC map |
| Information model | Data | Registry/graph/receipt schemas |
| Architecture model | C4 + ports | Context/Container + ICD |
| Decision model | ADR | Context/Decision/Status/Consequences |
| Verification model | L1/L2/L3 | Predicate per layer + SoT column |
| Threat / abuse model | Security | Abuse cases for locks/index/RAG |
| Science-transfer model | Metaphor | Locked vs Refuse table |
| Delivery model | Wave | DoR predicate |

---

## 3. Workflows (ordered) before AI codegen

```text
BFS Level0 governance
  → vision + stakeholders
  → StRS / SRS / use-cases
  → constraints ∥ assumptions ∥ OQs   (parallel, then merge)
  → rewrite every Must NFR as six-part QAS
  → ATAM tactics + tradeoff table
  → domain BCs + information model
  → ports/ICDs (language-agnostic)
  → ADRs (Accepted only for irreversible)
  → V&V + receipt schema
  → wave DoR green
  → ONLY THEN Spike code / agent codegen for that wave
```

Agent loop once authorized: **reason → act → verify(L1→L2→optional L3) → correct**  
with verify = deterministic sensors, not vibes.

---

## 4. Polyglot portfolio — classified, not scaffolded

Map the desired monorepo *names* onto **options**, not tip folders:

| Desired name | Role | Pre-code bucket |
| --- | --- | --- |
| Rust core-engine | AST/index/LockCheck/WASM host | `options/engine-rust` after ports exist |
| wasm-runtime | Sandbox guest | `08-verification/l3-proof` + options |
| Go chassis | Daemon/watch/OS | `options/chassis-go` Pilot |
| Clojure brain | Graph/Datalog | `options/graph-clojure` Pilot — not merge SoT |
| Python interface | ACI/translator | Peer option — not default identity |
| SQLite + CTE | Derived registry | Information model first |
| TypeScript IDE/LSP | Squiggles / panel | Tour Pilot after receipt schema |
| C / Zig | Earned FFI | Defer until one kernel + one index SoR |

**Refuse:** mass `Cargo.toml` before Approve; WASM-as-universal-language-runtime;
embeddings as symbol SoR; LLM text as verify witness.

---

## 5. Locked science transfers (E-DYN1)

Only these leave the lab:

| Transfer | Allowed use |
| --- | --- |
| Saliency / debounce | Event interest, not Loihi runtime |
| Advisory hysteresis | Dual-sink noise discipline |
| Remeasure cost language | Green-AI / work-budget *language* |
| climb→oracle ≈ reservoir→readout | Pattern analogy only |

Everything else in §papers stays **science** — not tip SoT.  
Full table: `11-science-transfer/locked-transfers/`.

---

## 6. Severe critique — inbound RE-MASTER-001 (AI draft)

Treat as **hostile input**, not Spec.

| Defect | Why it fails principal bar |
| --- | --- |
| Pins Phi-3 / Ollama / LanceDB as FR | Implementation leakage; model choice will change |
| Embeddings as “symbol indexing” | Category error vs SCIP |
| Org-wide Kuzu + social graph as Must | Scope explosion; local-first violated |
| Bare ms budgets without six-part QAS | Assumptions dressed as NFRs |
| Corpus/bench IDs without corpus | False verifiability |
| WASM capability deny-list as “proof” | Engineering control ≠ Watt/Iris theorem |
| FR/BR theater (priority formula, headers) | Compliance cosplay without stakeholder Approve |

**Disposition:** extract *actor concerns* only; rewrite Must spine as graph + locks +
receipts + Unknown; send model/RAG/org-MCP to Could/Pilot after QAS.

---

## 7. Bloom Create — Spec tickets (no Implement)

| ID | Acceptance |
| --- | --- |
| **BFS-1** | This taxonomy + folder stubs exist; DOMAIN_MAP points here |
| **BFS-2** | Wave-1 OQ ledger with `blocks-code` flags |
| **BFS-3** | Every Must NFR rewritten as six-part QAS or demoted |
| **BFS-4** | Ports + ICD stubs for Index/Registry/Resolve/LockCheck/Receipt |
| **BFS-5** | SoR\|derived matrix (ADV-1) Accepted Draft |
| **BFS-6** | Paper pack cross-ref + locked transfers Confirmed in-repo |
| **BFS-7** | RE-MASTER findings folded; no Phi/Lance as Must |

**Implement remains Refuse** until wave DoR green.

---

## 8. Adversarial checklist

- [ ] Dual product identity (Spring verify vs RAG SaaS) unresolved?
- [ ] Language nests pretending Design is done?
- [ ] Science metaphors smuggled into merge gates?
- [ ] QAS measures still TBD on Must NFRs?
- [ ] Proof tour schema missing while “explainable” claimed?
- [ ] SCIP treated as Spring DI?
- [ ] WASM treated as universal interpreter?
- [ ] Single oracle writer not named as constraint?

If any box is yes → **not ready for AI codegen**.
