---
title: Kitchen harness modernization — setUpModule / run_chain / fixtures (2026)
status: RESEARCH COMPLETE — Spec gate PENDING E-KH0
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine kitchen-sink domain_integration suite
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/04-implementation-frameworks.md
  - docs/research/06-test-suite-bounded-contexts-parallel.md
  - docs/research/08-rust-test-runners-bottlenecks.md
  - docs/research/09-test-adequacy-vs-coverage-inflation-2026.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225
  - treat Spec Kit / WorkflowEngine as mandatory test runtime
  - suite-wide xdist on shared mutable kitchen _STATE
  - replace chapter fault-injection claims with LLM fixture generators
spec_gate: PENDING E-KH0 — human approve K1–K12 before fixture migration code
---

# Principal memo: kitchen harness vs 2026 test frameworks

**Question:** Do “best” 2026 projects require a revolutionary rewrite of kitchen-sink
`setUpModule` / `run_chain` / shared dependencies — or is the aggressive move a
*principled Adopt* of pytest’s native DI (fixtures) plus ports, not a new product
framework?

**Product fit filter (same as segment 04):** Python CLI + hermetic Stage-0 tools +
chapter-shaped domain integration tests. Not a K8s farm, not a DB product, not a
greenfield Spec Kit app.

**Claim tiers:** `[Evidenced]` primary docs/paper/GitHub · `[Confirmed]` this repo ·
`[Unknown]` missing ID / open product choice.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Revolutionary rewrite of kitchen around a new 2026 “harness framework”? | **No — Refuse.** |
| Is unittest `setUpModule` + global `_STATE` the modern SoT? | **No** — pytest fixtures are the industry DI for tests `[Evidenced]`. |
| Highest-leverage Adopt? | Migrate kitchen to **session/package pytest fixtures** + frozen/read-only context + function-scoped mutable copies; keep `run_chain` as a **domain port**. |
| Was slowness a framework-shape bug? | **Mostly no** — cold-import × N subprocesses `[Confirmed]`; already fixed (~47s→~3.7s). Do not rescope for speed alone. |
| Pull Testcontainers / Spec Kit / Guice-style DI / pytest-bdd as kitchen SoT? | **Refuse** for this product (wrong problem class). |
| Hypothesis / Fixturize / FlakyDoctor as chapter replacements? | **Refuse as SoT**; Hypothesis **Adopt later** only on pure helpers (aligns E-QA3). |

**Management framing:** Modernize the *test BC boundary* (fixtures + ports + immutability),
not the *product*. Spec → Implement → Verify. One tip writer.

---

## 1. Framing — what kitchen is (domain, not “setup utils”)

Kitchen-sink is a **test bounded context** `[Confirmed]`:

| Concept | Module today | Role |
| --- | --- | --- |
| Hostile Spring fixture plant | `repo_builder` / `repo_plants_*` | Arrange |
| Pipeline recipe | `chain.run_chain` | Act (Stage-0 → mock LLM → gates → drift) |
| Tool invoke adapter | `tool_invoke.run_argv` | Port: argv → CompletedProcess-like |
| Shared artifact bag | `constants._STATE` + `harness.setUpModule` | Cross-chapter amortised setup |
| Chapter claims | `test_kitchen_sink_ch*.py` | Assert (unittest.TestCase + `pytestmark`) |

**SOLID / DRY / OCP / DDD read of today**

| Principle | Kitchen status | Gap |
| --- | --- | --- |
| SRP | Builder / chain / invoke already split | `_STATE` dict is a grab-bag DTO |
| OCP | `tool_invoke` is a good adapter | Chapters hard-import harness re-exports |
| DIP | Weak — tests depend on global dict + unittest hooks | Should depend on a `KitchenArtifacts` view |
| DRY | Shared chain once (post-share) | 9× re-export of `setUpModule` is ceremony |
| ISP | Read-only chapter tests share mutable bag | Need read-only vs scratch APIs |
| DDD | Chapter files ≈ subdomains | BC still speaks unittest lifecycle, not pytest DI |
| TDD / TTT | Characterization + fault chapters exist | Migration must keep chapter oracles |

---

## 2. Alternatives considered

| ID | Alternative | Shape |
| --- | --- | --- |
| A0 | Status quo (`setUpModule` + `_STATE` + in-process chain) | Working; already fast |
| A1 | **pytest session/package fixtures** in `tests/support/kitchen_sink/conftest` or domain conftest | Native DI, scopes, yield teardown |
| A2 | Full DI container (`dependency-injector` / `injector`) for tests | Guice-like graph |
| A3 | Testcontainers for “real” deps | Docker throwaways |
| A4 | pytest-bdd / Gherkin chapters | Narrative layer over claims |
| A5 | Hypothesis property suites replace kitchen chapters | Generative inputs |
| A6 | Spec Kit / agent WorkflowEngine drives kitchen | SDD toolkit as runtime |
| A7 | Suite-wide xdist + shared session fixture | Parallel wall-clock |
| A8 | LLM Fixturize / FlakyDoctor as harness SoT | Research repair/gen |

---

## 3. Evidence index (hype filter)

### 3.1 Primary frameworks (GitHub activity — surveyed 2026-08-09)

| Repo | Stars | Last push | Latest release (sample) | Fit to kitchen |
| --- | --- | --- | --- | --- |
| `pytest-dev/pytest` | 14397 | 2026-08-09 | 9.1.1 (2026-06-19) | **Core SoT for test DI** |
| `HypothesisWorks/hypothesis` | 8851 | 2026-08-09 | v6.165.2 (2026-08-05) | Pure helpers / properties — not enterprise plant |
| `ets-labs/python-dependency-injector` | 4909 | 2026-08-04 | (active) | App DI; overkill for hermetic CLI tests |
| `testcontainers/testcontainers-python` | 2268 | 2026-07-31 | v4.15.0 (2026-07-24) | DB/broker throwaways — **no kitchen need** |
| `pytest-dev/pytest-xdist` | 1892 | 2026-08-03 | v3.8.0 (2025-07-01) | Parallel workers; fights shared mutable session state |
| `pytest-dev/pytest-bdd` | 1459 | 2026-08-05 | (active) | Extra narrative layer; chapters already named |
| `syrupy-project/syrupy` | 871 | 2026-08-09 | v5.5.3 (2026-07-11) | Snapshot assertions — optional Adopt for artifacts |
| `github/spec-kit` | 125936 | 2026-08-07 | v0.16.1 (2026-08-07) | **SDD process kit**; its own tests use plain pytest fixtures |
| `astral-sh/uv` | 88528 | 2026-08-09 | 0.12.3 (2026-08-07) | Env/install — not harness |

All counts/pushes/releases `[Evidenced]` via `gh api` this session.

### 3.2 DeepWiki cartography (not architecture SoT)

| Target | Indexed | Takeaway for us | Tier |
| --- | --- | --- | --- |
| `pytest-dev/pytest` | 2026-04-16 | Fixtures = DI + lifecycle; setup/call/teardown protocol; pluggy plugins | `[Evidenced]` cartography |
| `HypothesisWorks/hypothesis` | 2026-01-08 | Warns: function-scoped fixtures + `@given` are a health-check footgun; prefer wider scopes for fixtures under properties | `[Evidenced]` |
| `testcontainers/testcontainers-python` | 2026-04-19 | Docker lifecycle / Ryuk cleanup — wrong dep class for kitchen | `[Evidenced]` |

### 3.3 Official fixture doctrine `[Evidenced]`

pytest docs (`scope=function|class|module|package|session`): widen only for
**expensive + safe-to-share**; mutable state stays narrow; factories-as-fixtures;
yield teardown. Blog consensus 2025–2026 restates the same rule (narrowest correct
scope). Primary: https://docs.pytest.org/en/stable/how-to/fixtures.html

### 3.4 arXiv / research (fixture *generation* ≠ harness SoT)

| ID | Title | Relevance | Stance |
| --- | --- | --- | --- |
| **2601.06615** | Fixturize: Bridging the Fixture Gap in Test Generation | LLM test-gen needs fixtures; FixtureEval benchmark | **Refuse** as kitchen runtime; optional research spike only |
| **2404.09398** | FlakyDoctor (neuro-symbolic flaky repair) | OD/ID flaky repair | **Refuse** as gate; Embody isolation so OD flakiness does not appear |
| **2511.14002** | FlakyGuard | Industry flaky repair via call graphs | Same refuse |
| **2606.04967** | SDD taxonomy (via synthesis 04) | Spec Kit / OpenSpec process | **Adopt process**; Refuse Spec Kit WorkflowEngine as test runner |

### 3.5 Confirmed local seams

| Claim | Evidence |
| --- | --- |
| 9 kitchen chapter modules re-export unittest `setUpModule` | `tests/doc_engine/test_kitchen_sink_ch*.py` |
| Shared amortised setup via `_STATE` + atexit cleanup | `tests/support/kitchen_sink/harness.py` |
| `run_chain` is the documented tool series; now in-process | `chain.py` + `tool_invoke.py` |
| Perf root cause was import tax, not setUpModule API | cold `python -m` ~0.65s → ~0.05s after lazy imports; suite ~47s → ~3.7s |
| Marker `domain_integration` already on kitchen | chapter `pytestmark` |
| Constitution refuses suite-wide xdist before shards; kitchen shared state would be OD-flaky under xdist | synthesis + research 06 policy **T-A** |

---

## 4. Embody / Adopt / Refuse

| Item | Stance | Rationale |
| --- | --- | --- |
| Kitchen as DDD **test BC** (plant / chain / chapter claims) | **Embody** | Concept modules already exist; keep cohesion |
| In-process tool invoke port (`tool_invoke`) | **Embody** | Correct adapter; preserves exit-code observability |
| Lazy package imports (sqlfluff deferred) | **Embody** | Green-AI / cost; already landed |
| pytest **session/package fixtures** replacing `setUpModule`/`_STATE` | **Adopt** | Industry DI; explicit deps; yield teardown; no global dict |
| Frozen / read-only `KitchenArtifacts` + function-scoped scratch copies | **Adopt** | Isolation; OD-flake prevention `[Evidenced]` flaky lit |
| `run_chain` as injectable port (callable / protocol) | **Adopt** | OCP: mock/thin chain in unit tests of chapters that only need docs |
| syrupy snapshots for selected artifacts | **Adopt optional** | High-signal, low ceremony; never sole SoT for gates |
| Hypothesis on pure helpers | **Adopt later** | Align E-QA3; not kitchen chapters |
| unittest.TestCase chapter bodies (interim) | **Embody until migrated** | Characterization stability |
| Convert chapters to plain pytest functions | **Adopt** (same epic as fixtures) | Drop dual framework tax |
| dependency-injector / injector for tests | **Refuse** | pytest fixtures already are DI; extra framework ≠ clarity |
| Testcontainers | **Refuse** | No Docker DB/broker in kitchen threat model |
| pytest-bdd as chapter SoT | **Refuse** | Chapters already narrative; Gherkin adds indirection |
| Spec Kit as kitchen orchestrator | **Refuse** | Process kit; even Spec Kit tests use fixtures `[Evidenced]` |
| Suite-wide xdist on kitchen session fixture | **Refuse** | Shared mutable/expensive plant → OD flaky; policy **T-A** |
| Fixturize / FlakyDoctor as harness | **Refuse** | Research tools; not deterministic SoT |
| Rewriting kitchen for “revolutionary” speed | **Refuse** | Already ~3.7s; next wins are design clarity |

---

## 5. Target architecture (Spec sketch — not implemented)

```text
tests/support/kitchen_sink/
  plants/          # arrange (already)
  chain.py         # act recipe (port)
  tool_invoke.py   # adapter
  artifacts.py     # KitchenArtifacts (frozen dataclass / MappingProxy)
  conftest.py      # session fixture: build + run_chain once; yield; cleanup

tests/doc_engine/test_kitchen_sink_chXX.py
  def test_…(kitchen: KitchenArtifacts, kitchen_docs_scratch):
      ...
```

**Scope rule `[Evidenced]` pytest doctrine**

1. `kitchen` session (or package) — expensive, **treat as read-only**.
2. `kitchen_docs_scratch` / `kitchen_repo_copy` function — mutable fault paths.
3. Never mutate `kitchen.signals` / `kitchen.docs` in place.

**Open/Closed:** new chapter = new tests depending on fixtures; do not reopen chain
unless the pipeline recipe changes.

---

## 6. Adversarial checklist

| # | Attack | Response |
| --- | --- | --- |
| C1 | “Modern = new framework” | Stars ≠ fit; Spec Kit itself uses fixtures |
| C2 | “setUpModule is fine forever” | Works but violates DIP/ISP; blocks xdist-ready isolation |
| C3 | “Migrate everything now for speed” | Speed already fixed; migration is design debt |
| H1 | Session fixture + mutation = OD flaky | Mandatory scratch copies; flake lit |
| H2 | Hypothesis replaces Ch01 fault thesis | Wrong tool; faults are intentional deviations |
| H3 | Testcontainers for “real Spring” | Real-repo lane already opt-in; Docker not required |
| M1 | Keep unittest + pytest dual forever | Tax; migrate chapter bodies in same epic |
| M2 | Global `_STATE` “just a cache” | Untyped dual-write surface across modules |

---

## 7. Epic E-KH — Kitchen harness ports (fresh-chat ready)

### Epic goal

Replace kitchen global `setUpModule`/`_STATE` with pytest-native fixtures and a
typed read-only artifacts port **without** diluting chapter claims or weakening
coverage/size/complexipy gates.

### E-KH0 — Spec gate (this memo)

| Field | Value |
| --- | --- |
| Tickets | Approve **K1–K12** below |
| Exit | `spec_gate: APPROVED E-KH0` recorded in this file + backlog P9.0 |
| Invariants | fail_under 98.7; complexipy ≤5; LOC ≤225; no utils bag |

**Decisions K1–K12 (propose Approve)**

| ID | Decision |
| --- | --- |
| K1 | Kitchen remains a **test BC**, not product code |
| K2 | pytest fixtures are the harness DI SoT (not Guice-style containers) |
| K3 | `run_chain` stays a **recipe port**; invoke stays an **adapter** |
| K4 | Shared artifacts are **read-only**; mutations use function-scoped copies |
| K5 | Do **not** introduce Testcontainers / pytest-bdd / Spec Kit runtime |
| K6 | Do **not** suite-wide xdist kitchen until isolation proven (policy **T-A**) |
| K7 | Perf narrative is closed unless new measurement regresses ≫1s |
| K8 | Chapter claim vocabulary (fault ≠ failure, drift statuses, …) unchanged |
| K9 | Migration is characterization-preserving (TTT): green before/after |
| K10 | New modules concept-named (`artifacts`, `plants`); no `utils/` |
| K11 | syrupy optional only; never replaces gate subprocess/in-process checks |
| K12 | Hypothesis stays out of kitchen chapters (E-QA3 lane) |

### E-KH1 — Implement (only after E-KH0)

| ID | Title | Acceptance |
| --- | --- | --- |
| KH1-1 | Introduce `KitchenArtifacts` (frozen) built from today’s `_STATE` keys | typed fields; no public `_STATE` |
| KH1-2 | Session/package fixture + yield cleanup (replace atexit + setUpModule) | one build/chain per process; tmp removed |
| KH1-3 | Function-scoped `docs_scratch` / `repo_copy` fixtures | Ch01/Ch10/Ch12 fault tests use copies only |
| KH1-4 | Migrate chapter modules off unittest `setUpModule` re-exports | no `setUpModule` in `test_kitchen_sink_ch*.py` |
| KH1-5 | Prefer pytest functions or thin TestCase with fixture injection | dual-framework tax reduced |
| KH1-6 | Durations: kitchen suite wall ≤ **8s** on CI-like host (sensor, not SoT) | `--durations` receipt; do not weaken claims |
| KH1-7 | size/complexipy/ruff green; no LOC offender growth | ratchets |

### Spikes (optional)

| Spike | Question | Exit |
| --- | --- | --- |
| KH-S1 | package vs session scope for kitchen | Pick one; document xdist interaction |
| KH-S2 | syrupy for `covering_proof` / drift clean report | Adopt only if review time drops without hiding diffs |

### Exit criteria (epic done)

- E-KH0 approved; E-KH1 merged; kitchen green; no `_STATE` / `setUpModule` in chapter modules;
  constitution gates green.

---

## 8. Mapping to prior epics (do not thrash)

| Prior | Interaction |
| --- | --- |
| E-TEST / policy **T-A** | Kitchen stays `domain_integration`; no suite-wide xdist |
| E-RUN | Durations sensor may watch kitchen regress; not floor |
| E-QA | Adequacy ≠ Cover%; kitchen chapters are metamorphic/fault witnesses — keep |
| E-CM | Unrelated to coverage climb artifact policy |

---

## 9. Recommended next single stream

1. **Human Approve E-KH0 (K1–K12)** — Spec only.  
2. Then **E-KH1** one tip.  
3. Do **not** open parallel “revolutionary framework” spikes (Testcontainers, Spec Kit runtime, DI containers).

**Bottom line:** The revolutionary 2026 move for *this* harness is not a new
framework — it is **using the framework you already run (pytest) as designed**:
fixtures as DIP, scopes as lifecycle, ports for chain/invoke, immutability for
shared expensive setup. Everything else with a high star count fails the product
fit filter.
