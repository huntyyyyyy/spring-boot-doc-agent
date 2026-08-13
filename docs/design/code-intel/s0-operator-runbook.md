---
title: E-CX0-S0 — Operator runbook (add Serena in Cursor)
status: DRAFT — how-to for S0; no product code
parent: docs/design/code-intel/s0-serena-adopt.md
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_cartography
claim tiers: Evidenced / Confirmed / Unknown
sources:
  primary:
    - https://oraios.github.io/serena/02-usage/010_installation.html
    - https://oraios.github.io/serena/02-usage/020_running.html
    - https://oraios.github.io/serena/02-usage/030_clients.html
    - https://oraios.github.io/serena/02-usage/040_workflow.html
    - https://oraios.github.io/serena/02-usage/050_configuration.html
  deepwiki:
    - https://deepwiki.com/oraios/serena
    - https://deepwiki.com/oraios/serena/2.1-mcp-server-implementation
    - https://deepwiki.com/oraios/serena/2.2-language-server-integration
  deepwiki_ask: not in this cloud MCP catalog; run locally (see §6)
---

# S0 — How to add Serena (Cursor + Java plant)

The adopt spec (`s0-serena-adopt.md`) is the kill criterion. **This file is
the install.** Nothing here is committed into `doc-engine`. Serena is an
operator MCP server pointed at **`ocs-api-service`**, not this Python repo.

Do **not** add Serena from an MCP marketplace.
`[Evidenced — oraios/serena README IMPORTANT]`

## 1. Install once (your machine)

Need `uv` on PATH. Then:

```bash
uv tool install -p 3.13 serena-agent
command -v serena
serena init
uv tool list
```

`[Evidenced — installation.html]`: Python via uv; `serena init` = language-server
backend (not JetBrains). Log the `uv tool list` line (version). That is FR-S0-01.

If Cursor cannot find `serena`, use the **absolute path** from `command -v serena`.
`[Evidenced — clients.html Common Pitfalls]`

## 2. Create the Serena project on the Java tree

```bash
cd /ABS/PATH/TO/ocs-api-service
serena project create --index
```

This writes `.serena/project.yml` and pre-caches symbols.
`[Evidenced — workflow.html]` First `find_symbol` is slow without `--index`.

Confirm `languages` includes `java` (auto-detect from `src/main/java`). If not,
add it in `.serena/project.yml`. Prefer `project.local.yml` for machine-local
JDK paths (gitignored by default).

Optional health: `serena project health-check`.

## 3. Wire Cursor MCP (this is “adding Serena”)

Cursor launches Serena as a **stdio subprocess**. You do not start it yourself.
`[Evidenced — running.html Standard I/O]`

**Where:** Cursor Settings → MCP → add server, **or** `~/.cursor/mcp.json`
(user), **or** `.cursor/mcp.json` **inside the `ocs-api-service` workspace**.
Do **not** put this in `spring-boot-doc-agent` unless that window’s job is
the Java plant (wrong tree → Python symbols, S0 is invalid).

```json
{
  "mcpServers": {
    "serena": {
      "command": "/ABS/PATH/TO/serena",
      "args": [
        "start-mcp-server",
        "--context", "ide",
        "--project", "/ABS/PATH/TO/ocs-api-service",
        "--mode", "planning"
      ]
    }
  }
}
```

| Flag | Why |
| --- | --- |
| `--context ide` | Cursor already has read/grep/shell. `ide` drops duplicates. `[Evidenced — configuration.html; clients.html Cursor/Cline]` DeepWiki: `ide` is the Cursor context. |
| `--project <abs>` | Single-project: plant is activated at start; `activate_project` is off. `[Evidenced — workflow.html; configuration.html]` |
| `--mode planning` | S0 is navigation. Do not pass `editing`. Do not treat `replace_symbol_body` as DoD. |

Restart MCP (or reload the window). In Agent mode, Serena tools should list
`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`.

Smoke (before the 12 questions): “Using Serena `find_symbol`, name one class
under `src/main/java` with `file:line`.” Empty → Java LS not up (step 4), not
a Spring miss.

## 4. Java language server (jdtls)

Serena’s Java backend is **eclipse.jdt.ls**, two modes
`[Evidenced — configuration.html Java (eclipse.jdt.ls)]`:

| Mode | When | What happens |
| --- | --- | --- |
| **Default vscode-java VSIX** | Laptop can reach GitHub + `services.gradle.org` | First Java query downloads JDTLS + bundled JRE 21 + Lombok + Gradle. No extra config. |
| **Upstream JDTLS** | Corporate / Artifactory / no GitHub | Set **both** `jdtls_path` and `lombok_path`. JDK 21+. Gradle via `./gradlew`. |

OCS is Gradle-shaped. If import fails, in `.serena/project.local.yml`:

```yaml
ls_specific_settings:
  java:
    gradle_wrapper_enabled: true
    use_system_java_home: true
```

`JAVA_HOME` must be JDK 21+ (upstream mode rejects older).
If the plant targets a newer `--release` than 21, register `runtimes`
(same page). Heap default `jdtls_xmx: 3G` — raise if index OOMs.

JetBrains plugin is **optional**, not required for S0 (FR-S0-02).

## 5. Then freeze and run the 12 questions

Copy the bank from `s0-serena-adopt.md` into a dated log **before** the next
Serena call (FR-S0-03). Ask only symbol tools; empty LSP → one grep, labeled
`grep`. Fill CX0-S0-3 / CX0-S0-4.

## 6. DeepWiki Ask (your local MCP — this cloud session does not have it)

This agent’s MCP catalog has **no** `deepwiki` / `ask_question` server.
Pages fetched: DeepWiki install + client-integration (indexed 2026-08-04).
Your Cursor DeepWiki MCP (`https://mcp.deepwiki.com/mcp`, no auth for public
repos) `[Evidenced — docs.devin.ai DeepWiki MCP]`.

Call **`ask_question`** with `repoName`: `oraios/serena`:

1. How do I register Serena in Cursor with `--context ide` and `--project`?
2. How is Java `eclipse.jdt.ls` installed (VSIX vs `jdtls_path` + `lombok_path`)?
3. Which tools does context `ide` disable vs `desktop-app`?

Paste the Ask URLs into the S0 log. Primary docs above still win on conflict.
