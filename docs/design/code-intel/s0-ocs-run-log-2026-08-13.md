---
title: E-CX0-S0 — OCS operator log + go/no-go
status: operator record — grep table; S1 not authorized
parent: docs/design/code-intel/s0-serena-adopt.md
date: 2026-08-13
do_not:
  - treat this as LSP proof
  - start S1 Implement
  - add serena to requirements.txt
---

# S0 OCS run log (2026-08-13)

Plant: operator unzip
`C:\Users\16145\Downloads\ocs-api-service-develop\ocs-api-service-develop`
(NFR-S0-02: not `harness/fixture-repo`). Java 17 via Scoop Temurin
`C:\Users\16145\scoop\apps\temurin17-jdk\current` (17.0.20). Serena **1.7.0**
(`uv tool`). `serena project health-check` **pass**. MCP stdio reached Claude
Desktop (`mcp_20260813-131529_10468.txt`); `--mode planning` was **additive**
on `editing`+`interactive`. First `find_symbol` was a smoke **before** this
file (FR-S0-03 stain). Bank copied **verbatim** from `s0-serena-adopt.md`
after that smoke; questions were **not** rewritten. Scoring used **ripgrep**
on `src/main/java` (and `src/main/resources` where noted). **Not LSP.**
Zero Serena edit tools (FR-S0-06).

## Table (CX0-S0-3)

| # | Answer (path:line or UNANSWERED) | Tool |
|---|---|---|
| 1 | none: no `interface` file contains `@Transactional`. Hits are impl/class: `EolsCollectionCaseStudyServiceImpl.java:45,60`; `LearningObjectServiceImpl.java:684,735`; `TaxonomyServiceImpl.java:43,60`; `TaxonomyMappingService.java:164`. `CachingConfig.java:39-40` comment. | grep |
| 2 | none: `rg -l "@interface" src/main/java` empty. Beans use Spring stereotypes already in `SpringMetaEdges.qll`. | grep |
| 3 | `HomeController.java:7-9` `@Controller` + method `GET /`. Effective: **GET /**. | grep |
| 4 | none dual-site. Field `@Autowired` is the style (`CachingConfig.java:97`, `TopicController.java:44-46`). Zero `@RequiredArgsConstructor` / `@AllArgsConstructor`. | grep |
| 5 | no `@ConditionalOnProperty`. Closest: `OpenAPIConfig.java:13` `@Profile({"local","unitTest"})` — absent on prod. No `spring.profiles` in `src/main/resources`. | grep |
| 6 | **UNANSWERED** for `this.` proxy-skip. `@Transactional` methods: `TaxonomyMappingService.java:164`; `TaxonomyServiceImpl.java:43,60`; `LearningObjectServiceImpl.java:684,735`; `EolsCollectionCaseStudyServiceImpl.java:45,60`. | grep |
| 7 | `ThreadPoolConfig.java:13` `@EnableAsync`; `:34` `@Bean(name=BACKGROUND_TASK_EXECUTOR)`. Named: `TopicJDBCRepository.java:101,106`; `LearningObjectJDBCRepository.java:112,118`. Bare `@Async`: `TaxonomyMappingService.java:163` → default executor, not proven to be that bean. | grep |
| 8 | no `@Inheritance` / `@Discriminator*`. Mapped superclasses: `BaseIdObject.java:21`, `BaseDataObject.java:16`, `BaseVtwObject.java:11`, `BaseSynapticaObject.java:11`. Example: `Concept.java:16-17` → `content.concept`. | grep |
| 9 | none in this tree: no `SecurityFilterChain` / `WebSecurityConfigurer` / `antMatchers` / `requestMatchers`; no `spring.security` in resources. | grep |
| 10 | none: no `@ConfigurationProperties` in `src/main/java`. | grep |
| 11 | no two `@Bean`s of the same type split prod vs other. Only profiled: `OpenAPIConfig.java:13-15` (local, unitTest). Unprofiled (present in prod): `ThreadPoolConfig.java:34`, `AspectLoggerConfig.java:11`, `CachingConfig.java:99,106,117,151`. | grep |
| 12 | none: `rg -l "@interface" src` empty. No custom mapping stereotype. | grep |

## CX0-S0-4 — Go / no-go

**S1 is not authorized.**

Most rows are “that Spring pattern is **not in this plant**,” with citations.
That is not a recurring LSP miss on a fact that exists. Q6 is grep-incomplete
(`this.` not proven), not a named Spring-resolution hole. Q9 is “not in this
module.” Q3 was answerable from source text.

This log **does not** prove Serena/jdtls can answer the bank. Health-check
proved one `find_symbol` class; the twelve were scored with grep on purpose
(no Claude tokens). A later LSP pass may reuse this frozen bank; do not edit
the questions.

Active tip stays **#119 then E-COH1**. No `src/` on this record.
