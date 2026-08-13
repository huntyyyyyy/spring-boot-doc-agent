---
title: E-CX0-S0 — Adopt Serena (operator)
status: DRAFT Spec — parked; operator runbook; no product code
research date: 2026-08-13
spec_gate: DRAFT E-CX0-S0
bloom_gate: required-through-create
parent: docs/design/code-intel/README.md
do_not:
  - add Serena as a Python dependency of doc-engine
  - write questions after seeing misses
  - treat star counts as stewardship
  - start S1 if the frozen questions are answered
sources:
  primary:
    - https://github.com/oraios/serena
    - https://oraios.github.io/serena/02-usage/010_installation.html
    - https://oraios.github.io/serena/02-usage/030_clients.html
    - https://oraios.github.io/serena/01-about/020_programming-languages.html
    - https://oraios.github.io/serena/02-usage/050_configuration.html
  deepwiki:
    - https://deepwiki.com/oraios/serena
---

# S0 — Adopt Serena

**Goal:** Give the agent IDE-grade **navigation** on the Spring tree without
building an index. Kill criterion for S1 lives here.

**How to add Serena:** [`s0-operator-runbook.md`](s0-operator-runbook.md)
(any MCP client: Cursor, Claude Code, IntelliJ). Kill criterion, not install.

```text
Iso: LSP symbol graph ≅ IDE go-to / find-refs | I3: does not preserve
Spring meta-annotations or inherited @Transactional | I5: no merge SoT
```

## Bloom

| Level | Evidence |
| --- | --- |
| Remember | Tools: `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`; edits include `replace_symbol_body` `[Evidenced — tools.md]`. Install: `uv tool install -p 3.13 serena-agent` then `serena init` `[Evidenced — README]`. Java listed under language servers `[Evidenced — programming-languages.html]`. **Do not install via MCP marketplace** `[Evidenced — README IMPORTANT]`. |
| Understand | Serena is an MCP façade over LSP (SolidLSP) or JetBrains. This product’s Stage-0 default is ast-grep (no classpath). S0 measures whether **jdtls** closes the precision gap in `CONSTRAINTS.md` Known precision tradeoffs §1. |
| Apply | Operator runbook: `uv tool install` → `serena project create --index` on `ocs-api-service` → Cursor MCP `start-mcp-server --context ide --project <abs>`. See `s0-operator-runbook.md`. |
| Analyze | **Adopt** Serena. **Refuse** rebuilding `find_symbol`. **Refuse** enabling Serena writes as *our* attested apply. Stars (~28k on 2026-08-13) ≠ pin/stewardship. |
| Evaluate | § False-green |
| Create | Tickets below |

## Frozen question bank (write answers into the run log; do not edit this list after T2)

Twelve questions, frozen **before** the first Serena session. Each answer must
cite `file:line` or record **UNANSWERED** with the tool that failed.

1. Which types inherit `@Transactional` from an **interface** (not the impl source line)?
2. Which types are `@Service` / `@Component` only via a **meta-annotation** not in `SpringMetaEdges.qll`?
3. What is the **effective** HTTP mapping (class + method) for a given handler?
4. Constructor injection vs field `@Autowired` — same bean, both call sites?
5. `@ConditionalOnProperty` — is the bean present under the named profile?
6. Self-invocation of a `@Transactional` method on `this` — proxy skip?
7. `@Async` — which executor actually runs the method?
8. JPA entity inheritance — which concrete type maps to which table?
9. Effective security matcher / filter order for one path?
10. `@ConfigurationProperties` prefix → bound fields?
11. Profile-specific `@Bean` of the same type — which wins for `prod`?
12. Request mapping composed via a **custom** stereotype annotation?

If LSP + grep answer **all twelve** with citations, **S1 is not authorized**.
S1 starts only when a **named recurring miss** remains (typical: 1, 2, 3).

## FR / NFR

| ID | Requirement | Acceptance |
| --- | --- | --- |
| **FR-S0-01 Pin** | Serena installed from the official path (uv / git SHA), not a marketplace blob. Version recorded in the operator log. | Log names SHA or `uv` package version. |
| **FR-S0-02 Java** | Language-server backend can symbol-search Java on the plant tree. JetBrains plugin is optional, not required. | `find_symbol` returns ≥1 class from `src/main/java`. |
| **FR-S0-03 Freeze** | The twelve questions above are copied into the run log **before** tool use. | Timestamp on the question file ≤ first `find_symbol` call. |
| **FR-S0-04 Cite** | Each answer is `path:line` or `UNANSWERED` + tool name. | 12 rows; no “looks like”. |
| **FR-S0-05 Fallback** | Empty LSP → one grep pass, labeled `grep`, not `lsp`. | Provenance column. |
| **FR-S0-06 Writes** | Do not use `replace_symbol_body` / `replace_content` as program DoD. Navigation only. | Run log has zero edit tools **or** an explicit “out of scope” note. |
| **NFR-S0-01** | No `serena` / `jdtls` in this repo’s `requirements.txt`. | `rg` empty in that file. |
| **NFR-S0-02** | Plant is operator checkout (Artifactory). Not `harness/fixture-repo`. | Path in log. |

## Tickets

| ID | Title | Acceptance |
| --- | --- | --- |
| **CX0-S0-1** | Pin Serena + Java LS | Follow `s0-operator-runbook.md`. FR-S0-01, FR-S0-02, NFR-S0-01 |
| **CX0-S0-2** | Freeze the twelve questions to a dated log file | FR-S0-03. Log: `s0-ocs-run-log-2026-08-13.md` (freeze after smoke `find_symbol`) |
| **CX0-S0-3** | Run on `ocs-api-service`; fill the 12-row table | FR-S0-04, FR-S0-05, NFR-S0-02. Table in that log (**grep**, not LSP) |
| **CX0-S0-4** | Go / no-go memo | **S1 not authorized** — same log. FR-S0-06 |

## False-green

| Failure | Why it looks green | Bite |
| --- | --- | --- |
| Questions edited after misses | Bank fits the tool | T2 timestamp |
| Grep labeled as LSP | Inflated “Serena works” | Provenance column |
| Fixture repo instead of OCS | Easy symbols, no Spring graph | NFR-S0-02 |
| Star count as Adopt proof | Popularity ≠ classpath fidelity | Analyze row |
| One answered question → skip S1 | Undersample | Need all 12 **or** a named miss |

## Definition of Done

Operator log + go/no-go memo. **No PR to `src/`.** S1 may be scheduled only
if CX0-S0-4 names a recurring Spring miss the LSP did not cite.
