---
title: E-IK0 — Intent Kernel v2 spike-first plan (adversarial review)
status: DRAFT Spec — parked; no Implement
research date: 2026-08-13
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine (read/scan/certify); proposed write kernel is a category change
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_cartography  # session catalog had no DeepWiki MCP; pages fetched
  - llms_txt
related:
  - docs/research/quality-backlog.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/process/35-control-plane-closed-loop-2026.md
  - docs/research/process/37-operator-agent-surface-cli-mcp-rag-2026.md
  - docs/reviews/9bc7851_PR_94.md
  - docs/research/process/50-intent-kernel-v3-consolidated-2026-08-13.md
  - DOMAIN_MAP.md
do_not:
  - implement an intent kernel on this tip
  - open a parallel Active stream beside #119 / E-COH1
  - treat harvest of spring_drift / certification / run_manifest as CAS-before-write
  - use ocs-api-service Artifactory plant as CI / spike DoD
  - add MCP write/codegen tools (OAS12) without human Spec Approve
  - adopt OPA/Rego or Moderne as tip runtime
  - install unpinned LiteLLM / treat gateway as spike dependency
spec_gate: DRAFT E-IK0 (2026-08-13) — evidence record; plan SoT is process/50 (three-item unblock)
plan_sot: docs/research/process/50-intent-kernel-v3-consolidated-2026-08-13.md
sources:
  llms_txt:
    - https://ast-grep.github.io/llms.txt
  primary:
    - https://ast-grep.github.io/guide/rewrite-code.md
    - https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees
    - https://arxiv.org/abs/2606.30970
    - https://arxiv.org/abs/2607.14890
    - https://github.com/quangdang46/hashline
    - https://github.com/jamjet-labs/agentboundary
  deepwiki:
    - https://deepwiki.com/ast-grep/ast-grep
    - https://deepwiki.com/open-policy-agent/opa
---

# Principal review: Intent Kernel v2 (measure first)

**Disposition (2026-08-13).** Plan SoT is **v3** (`process/50`). This file stays
the evidence record. **Conceded:** C1–C3, H1, H4–H6, M1–M2, harvest verb,
homonym pin. **Overreach withdrawn:** IK0-4…IK0-8 as pre-spike Approve gates —
three-item unblock (D-00, D-01, five failing tests). **Still in v3:** §8 is
same *rule* (name the denominator), different *plant* (not a spike
dependency); 5b pinned to `DRIFT`; routing 98%/100% left `[Unknown]` until
cited; LiteLLM only via official image after GHSA-5mg7-485q-xm76.

**Subject.** Spike-first plan v2 for an “Intent Kernel” (CAS + fail-closed policy +
receipts around one Java `match_rewrite`). **Not** a PR of kernel code.

**Claim tiers:** `[Evidenced]` primary docs/papers · `[Confirmed]` this tree ·
`[Unknown]` missing ID or unprobed product.

**Iso:** DB compare-and-swap + all-or-nothing commit ≅ `expected_pre_hash` +
atomic apply + receipt → land as **pattern** (spike tests / join contract) |
non-preserved: isolation, multi-object txn, crash durability, short-hash
freshness | **I5:** MCP write tools **would** retype OAS12 / merge predicates —
default **no** until Spec Approve.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Approve v2 as Spec and Implement? | **No.** Park as Draft Spec **E-IK0**. |
| Is the ordering correction vs v1 sound? | **Yes** — do not write 11 ISA docs before one executable join. |
| Does v2 invert SDD? | **No, and it should not.** Spec **the spike** (five tests + D-00/D-01 lock), then implement, then spec the ISA from measurement. Decision 21 stays. `[Confirmed]` |
| Is the harvest a kernel? | **No.** It is a **structure** map (hash → admit/deny → provenance). Substrate is a **read/certify doc pipeline**, not CAS-before-write. |
| Kill-switch ≥90% of an unnamed FR list? | **Reject.** That is `coverage_climb` as a product gate. Score the **join contract**. |
| Active tip? | **Do not start.** Backlog Active is #119 / E-COH1. This memo is parked. |

**Keep from v2:** D-01/D-02/D-03 as blocking design questions; cut `CORPUS≥150`
and `unknown-deferred`; receipts as provenance not “verified architecture”;
bake-off **before** a spec pack; ~25 sources only on questions a spike cannot
answer.

**Block before any spike code (v3, three items):** D-00 (where tests live),
D-01 locked before Phase 0, five behaviours as named failing tests on
`fixture-repo`. Bake-off rubric / RQs / ISA are post-spike.

---

## 1. What v2 gets right

v1’s failure mode is real: a literature-process that never executes is
process tautology. This repo already named the isomorphic defect — ranking
uncovered units then adding `test_coverage_climb_*` until Cover% moves, without
raising discriminative power (`coverage-quality/09` §4.2). `[Confirmed]`
`CORPUS≥150` as an ADR gate is that failure in research form. Cutting it is
correct.

D-03 is correct: CAS + policy + receipts is **transactional integrity and
provenance**, not proof of refactor correctness. `verified-architecture` would
over-claim. `[Evidenced]` AgentBound (arXiv:2606.30970) itself separates
authorization from “should this action occur,” and still does not claim program
equivalence.

Removing `unknown-deferred` as a terminal RQ state is correct. An escape hatch
on every item makes DoD unfalsifiable. `answered` / `refuted` / `blocking` +
named waiver matches this repo’s human-review floor (OAS15). `[Confirmed]`

---

## 2. Understand — this product’s types (Bloom 2)

`DOMAIN_MAP.md`: **doc-engine** is Stage-0 scan + optional generative Path B →
certified fourteen-view Spring docs. Truth classes: SoR / derived / sensor /
product / meta / adapter. MCP today is a **read** query surface.
`dispatch_tool` drops caller `root` (confused-deputy fix). `[Confirmed]`

```145:161:src/doc_engine/query/mcp_tools.py
def dispatch_tool(name: str, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
    args = dict(arguments or {})
    # Never honor caller-supplied root (confused deputy).
    args.pop("root", None)
    ...
        raise QueryError(f"unknown MCP tool: {name}")
```

E-OAS0 **OAS12** Refuse: MCP write/codegen. `[Confirmed]` A mutating intent
kernel is a **new product BC**, not a nest of `scanning` or `compliance_gates`.

v2 never answers **D-00 — product home:** this repo’s new BC vs a greenfield
repo that only *cites* this tree as prior art. That choice changes every later
gate (98.7, OAS12, OCS plant, Active tip).

---

## 3. Harvest — structure vs substrate (I1–I5)

v2: S3/S4/S5 analogues already exist (`spring_drift_*` “15 modules”,
certification/gates, `run_manifest_*` “9 modules”). Counts and verbs are
wrong.

| Plan claim | This tree `[Confirmed]` | What the map preserves | What it does **not** |
| --- | --- | --- | --- |
| S3 CAS / drift | **12** `spring_drift_*.py` files, not 15. `tier1_scan` / `classify_files` hash files and re-verify **citations** after the tree already moved. | Cheap whole-tree hash, then targeted recheck | **Not** compare-and-swap **before** a write. No `expected_pre_hash` in `src/` (ast-grep: zero). |
| S4 policy | `certification.py` fail-closes on schema then **refolds** `certified` from stamped stage/gate facts. `gates.py` / `live_gates.py` run **doc-pipeline** validators. | Admit/deny, fail-closed fold | **Not** policy-before-mutate of customer Java. |
| S5 receipt | **9** `run_manifest*.py`. `git_commit_hash` records `rev-parse HEAD`. `_write_json_atomic` is temp+`os.replace`. | Provenance record; staged-write-then-rename | Binds a **scan run** to HEAD, not pre/post hashes of an apply. `git_commit_hash` degrades to `None` (warning), not fail-closed. |

```25:35:src/doc_engine/tools/run_manifest_io.py
def _write_json_atomic(path, data):
    ...
        rm.os.replace(tmp_path, path)
```

```34:47:src/doc_engine/tools/spring_drift_tier1.py
def tier1_scan(repo_path, scan_context=None):
    """Fresh sha256 per file currently in repo_path.
    ...
        current[rel] = spring_signal_scan.compute_file_signature(full)
```

**Better in-repo analogues (still not a kernel):**

- **Atomic single-file publish:** `_write_json_atomic` — Embody as Phase 0
  default for D-02; do not bake-off journal vs git-index on one `match_rewrite`.
- **Receipt semantics:** E-CPL0 Proof-or-Stop (arXiv:2607.14890) — claim ≠
  state; bind command + exit + digest + HEAD. `[Evidenced]` + `[Confirmed]`
- **Apply witness not RC:** `Mutator._apply_structural` already refuses
  ast-grep `--update-all` exit codes. `[Confirmed]`

```68:84:scripts/ratchets/mutator.py
def _apply_structural(path: Path, mutator: Mutator) -> Optional[str]:
    """Rewrite via ast-grep, so the anchor survives reformatting.

    The exit code cannot carry this decision. Measured against ast-grep
    0.44.1: ``--update-all`` exits 1 both when the pattern matches nothing and
    when the invocation genuinely fails...
    """
    before = path.read_text(encoding="utf-8")
    ...
    if path.read_text(encoding="utf-8") != before:
        return None
```

Same quirk is indexed in `docs/process/tool-quirks.md` (2026-07-25). Phase 0
“zero bytes written” **must** be pre/post hash, not `ast-grep` status.

---

## 4. Apply — how a spike would run *here* (Bloom 3)

ast-grep rewrite is real and already a pin. `[Evidenced]`
[rewrite-code](https://ast-grep.github.io/guide/rewrite-code.md): `--rewrite`
shows a diff; `-U` / `--update-all` applies; YAML `fix` rewrites **one target
node** per rule (expand range is explicit). Java is a built-in language
(`[llms.txt](https://ast-grep.github.io/llms.txt)`; DeepWiki cartography
[ast-grep/ast-grep](https://deepwiki.com/ast-grep/ast-grep)).

This repo already applies `--update-all` in the mutator harness. A walking
skeleton is: pytest over `spring-signals/harness/fixture-repo/` (hermetic Java
shapes), not `ocs-api-service`. `[Confirmed]` E-OCS is an **operator** plant
(Artifactory). Cold-BC Refuse: Artifactory OCS as CI SoT.

Phase 0 “no telemetry exporter” vs “histogram for `C-LOCATE-P95`” is an
internal contradiction. Keep a **local timer + JSONL** in the test; refuse an
OTel exporter (E-TEL Refuse as tip SoT).

---

## 5. Analyze — bake-off candidates (Bloom 4)

v2 Phase 1: “Assemble Moderne + hashline + OPA + AgentBoundary against the
Phase 0 five.” Those four do not occupy the same slot.

| Name | What it actually is | Covers Phase 0 five? |
| --- | --- | --- |
| **Moderne / OpenRewrite** | LST in memory → transform → **overwrite changed files**. Nothing stored between runs. `[Evidenced]` [LST lifecycle](https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees) | S2 apply (Java recipes) **yes**. S3 `expected_pre_hash` **no**. S4 fail-closed kernel policy **no**. S5 intent receipt **no**. |
| **hashline** | A **family**, not a product. `quangdang46/hashline`: 4-hex xxh3 file tag + line anchors + temp+rename. `ck0i/hashline-mcp`: 2-hex SHA-256, all-or-nothing edit. `makcimbx/opencode-better-hashline`: short hashes are **display**, never freshness authority. `[Evidenced]` | Stale-edit reject **maybe**, depending on which pin. Cryptographic CAS **Unknown** / often **no**. |
| **OPA** | Decision∖enforcement split. `[Evidenced]` [DeepWiki OPA](https://deepwiki.com/open-policy-agent/opa). This repo: **Adopt split, Refuse Rego/WASM runtime** (cold-BC taxonomy). | Algebra **shape** only. Not a Java rewrite CAS. |
| **AgentBound / AgentBoundary** | **Three different things.** (1) arXiv:2606.30970 — 3-authority governance + receipts. (2) FSE AgentBound — MCP capability sandbox. (3) jamjet `agentboundary` — portable action-receipt spec. `[Evidenced]` | v2 Phase 1 says Agent**Boundary**; RQ-POL-01 says Agent**Bound** 3-authority. Homonym bake-off. |

**≥90% of FR checklist → stop and wrap other people’s engines** fails two
ways: the FR list is unnamed, and “Moderne rewrites Java” would inflate
coverage without covering the **join** that is the product.

Correct kill-switch (named denominator): for each of the five Phase 0
behaviours, can the candidate **alone** produce that behaviour with a
witness? Count **5**, not “% of v1 docs.” If 5/5, the product is an
integration layer. If 0–2/5, the gap *is* the kernel. Partial (e.g. 2/5 =
apply + stale-hash) is the interesting case — spec **only** the join.

---

## 6. Evaluate — adversarial findings (Bloom 5)

### C1 — D-00 missing: product home and category

Severity: **Critical (scope)**. v1 assumed an empty repo. v2 harvests
`huntyyyyyy/spring-boot-doc-agent` as if the spike lands **here**, without
saying so. Here: new BC, OAS12, one-tip rule, 98.7 on any Python that enters
the wheel. Greenfield: harvest is citation, not copy. **Decide D-00 before
Phase 0.**

### C2 — Phase 0 is defined not to answer D-01 / D-02

Severity: **Critical (internal contradiction)**. Phase 0: one language, one
`match_rewrite`, no index. Table: “D-01, D-02 answered by the first multi-node
intent you try to write.” A single-node spike cannot falsify transaction
coordination vs planner-above-kernel. Rollback cost (staged-write vs journal
vs git-index) does not appear on one successful file rewrite. Crash-mid-apply
is not in the five behaviours.

**Lock D-01 before Phase 0.** Recommendation: **(b)** single-node kernel +
planner above — smaller, and it honestly drops “the kernel delivers safe
refactoring.” Do not let YAML `fix` multi-match inside one file silently
become “we solved D-01.”

### C3 — 90% FR coverage is an unfalsifiable kill switch

Severity: **Critical (gate type)**. Same class as `CORPUS≥150` and climb
Cover%. A percentage of an unpublished checklist cannot be a product
decision. Replace with the 5-behaviour join matrix above.

### H1 — Harvest overclaim (count + verb)

`spring_drift_*` is 12 modules; citations re-verified **after** mutation, not
CAS. `certification` refolds **docs**. `run_manifest` records HEAD of a scan.
Structure-Adopt; substrate-Refuse. Module-count errors are the same evidence
discipline v2 criticizes in v1.

### H2 — AgentBound ≠ AgentBoundary ≠ MCP AgentBound

Bake-off and RQ-POL-01 name different objects. Pin one primary (recommend
arXiv:2606.30970 for **decision algebra**; jamjet receipts for **field
mapping** RQ-REC-01; FSE paper for **MCP sandbox** — not interchangeable).

### H3 — Unpinned “hashline” reopens RQ-HASH-01 as collision theater

4-hex / 2-hex / CRC32 families are **sensors** for stale reads, not SoR CAS.
Better-hashline states that explicitly. Phase 0 should use **file sha256**
(this repo’s `compute_file_signature`) as expected_pre_hash. Line-anchor
protocols are a later interop RQ, not the kernel hash.

### H4 — OCS as Phase 0 exit criterion

`ocs-api-service` needs Artifactory; CI uses `fixture-repo`. `[Confirmed]`
Phase 0 DoD = hermetic fixture reproducing the five. OCS = E-OCS **campaign**
after, never the spike’s merge bar.

### H5 — “Unhit ⇒ imagined” drops Confirmed hazards

Phase 0 has no MCP, so it will not hit confused-deputy / write-tool policy.
Those are **Confirmed** in this repo (PR #94 C1; OAS12), not imagined. Surviving
RQs must include **RQ-MCP-WRITE-01** (containment, server-pinned root, no
caller path) if D-00 is this repo **or** if `06_MCP_SURFACE` remains in the
section list. Proof-or-Stop receipts (E-CPL0) similarly survive without being
“hit” by a happy-path rewrite.

### H6 — p95 from a walking skeleton is false precision

`04_CONSTRAINTS.md` bounds as “measured p95s” on one op × one repo are the
literature-placeholder error with a histogram costume. Record **probe**
latencies with conditions. Promote to constraint only after bake-off + a
stated plant. Boolean `C-*` (e.g. apply atomicity) do not “cite a p95.”
DoD “every `C-*` bound cites a measurement” over-applies.

### M1 — ast-grep apply-all vs single-node story

`--update-all` rewrites **every** match. A method-name pattern in one file
can hit declaration + calls (official YAML example does exactly that). Phase 0
must pin: one file, one match, or admit intra-file multi-site and still refuse
to call that D-01.

### M2 — Dirty-tree item underspecified

“Re-run (2) and (3) on a dirty tree does not corrupt it” — dirty from a prior
**successful** apply, from unrelated edits, or from a crashed apply? Split
into three tests. Crashed apply **is** D-02 and is missing.

### M3 — Kept process vs this repo’s SDD

Pre-register hypotheses, SYNTHESIS excerpts, temporal citations, `C-*`/`T-*`
IDs: keep. Do not keep “spike then spec” as a license to skip a **spike Spec**.
The five behaviours **are** the Spec. pytest is the vehicle (this repo already
works that way).

---

## 7. Embody / Adopt / Refuse (this product)

| Stance | Choice |
| --- | --- |
| **Embody** | Spec-the-spike → implement → spec-the-ISA. File sha256 pre-hash. Witness = bytes/hash, not process RC. `_write_json_atomic` for single-file publish. Server-pinned roots if any MCP. One Active tip. |
| **Adopt (pattern)** | OPA decision∖enforcement **split** without Rego. AgentBound 3-authority **algebra** as a paper, not a runtime. AgentBoundary receipt **field names** for RQ-REC-01. OpenRewrite LST as S2 competitor in bake-off. Proof-or-Stop receipt shape (2607.14890). ast-grep `-U` as S2 engine for Phase 0. |
| **Refuse** | v2 as Implement on this tip. `CORPUS≥150` revival. `unknown-deferred`. OPA/Moderne/hashline as **tip kernel**. MCP write tools without Approve. OCS Artifactory as spike DoD. ≥90% unnamed FR. Short content hashes as CAS SoR. `verified-architecture` naming. Spec sections for unexercised stages. Research-process CI that outgrows the artifact. |

---

## 8. Create — parked epic (three-item unblock)

Plan SoT: [`process/50`](50-intent-kernel-v3-consolidated-2026-08-13.md).
IK0-4…IK0-8 are **post-spike writing**, not Approve gates.

**Epic goal.** Decide whether an intent join (CAS + deny + receipt) is worth
building — by locking home and cardinality, then failing tests, not by
writing an ISA pack.

**Exit.** D-00 + D-01 + five named failing tests. Then one Implement stream
**after** the current Active tip.

| ID | Title | Acceptance |
| --- | --- | --- |
| **IK0-0** | D-00 product home | (A) this repo or (B) greenfield. Names where pytest files live (committing here implies A). |
| **IK0-1** | Lock D-01 | Default **(b)**; one-match pin so `--update-all` does not fake multi-node. |
| **IK0-2** | Five failing tests | Apply / Drift / Deny / Receipt / 5a–5c as in v3 §4. Witness = sha256. Fixture = `harness/fixture-repo`. JSONL probes in-test. 5b = `DRIFT`. 5c = kill between temp write and replace. |

**After spike (not gates):** fill bake-off matrix; surviving RQs including
RQ-MCP-WRITE-01 if D-00=A; ISA from survivors. Gateway/LiteLLM is a
**different plant** — not this unblock.

**Invariants:** fail_under 98.7 / complexipy ≤5 / size ≤225 if D-00=A;
one-stream; no utils bag; policy 16-A untouched.

---

## 9. Definition of done for *this* review

- v2 is **not** Spec Approve. v3 is Draft, parked.
- E-IK0 unblock is **three** items, not nine.
- No kernel or LiteLLM implementation on this branch.
