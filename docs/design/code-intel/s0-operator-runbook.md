---
title: E-CX0-S0 — Operator runbook (add Serena; any MCP client)
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

# S0 — How to add Serena (Java plant; Cursor, Claude, or IntelliJ)

The adopt spec (`s0-serena-adopt.md`) is the kill criterion. **This file is
the install.** Serena is an MCP server pointed at **`ocs-api-service`**.
The client can be Cursor, Claude Code, Claude Desktop, or IntelliJ — pick
**one**. Do not install from an MCP marketplace.
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

If the client cannot find `serena`, use the **absolute path** from `command -v serena`.
`[Evidenced — clients.html Common Pitfalls]`

For IntelliJ’s **JetBrains plugin backend** instead of jdtls: `serena init -b JetBrains`
`[Evidenced — installation.html]`. Then skip default VSIX in §4.

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

## 3. Wire the MCP client (this is “adding Serena”)

The client launches Serena as a **stdio subprocess**. You do not start it
yourself. `[Evidenced — running.html Standard I/O]` Always pass
`--project /ABS/PATH/TO/ocs-api-service` (or `cd` there and `--project "$(pwd)"`).
`--mode planning` for S0. Do not pass `editing`.

| Client | What to run / paste | `--context` |
| --- | --- | --- |
| **Claude Code** | `serena setup claude-code` or `claude mcp add serena -- serena start-mcp-server --context claude-code --project /ABS/PATH/TO/ocs-api-service` | `claude-code` `[Evidenced — clients.html]` |
| **Cursor / VS Code / Cline** | MCP json below (`~/.cursor/mcp.json` or the **Java** workspace `.cursor/mcp.json`) | `ide` |
| **Claude Desktop** | Same launch command in `claude_desktop_config.json`; ask the agent to activate the plant (global config). | `desktop-app` |
| **IntelliJ Copilot** | Settings → Tools → GitHub Copilot → MCP → `serena start-mcp-server --context jb-copilot-plugin --project …` | `jb-copilot-plugin` `[Evidenced — clients.html]` |
| **IntelliJ Junie / AI Assistant** | `--context junie` or `jb-ai-assistant` (same `--project`) | see clients.html |

Cursor/VS Code example:

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

Neither Claude app has a form that adds a **local** Serena process the way
Connectors adds Slack. Desktop edits a JSON file; Code uses the CLI, then
`/mcp` inside the session.

**Claude Desktop (chat app)** `[Evidenced — oraios clients.html; MCP local-servers]`:

1. macOS: menu bar **Claude → Settings** (not the in-chat account gear).
   Windows: gear → Settings.
2. Left sidebar **Developer** → **Edit Config**
   (Serena’s page: File → Settings → Developer → MCP Servers → Edit Config).
3. That opens `claude_desktop_config.json`:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
4. Put Serena under `mcpServers` with `"command"` = **absolute** path to
   `serena`, `"args"`: `start-mcp-server`, `--context=desktop-app`,
   `--project`, plant path, `--mode`, `planning`.
5. Save. **File → Exit** (window close only minimizes). Reopen.
6. Hammer icon in the chat = tools loaded.

**Connectors** (Desktop **+** next to the prompt, or Settings → Connectors)
is for catalog remote servers, not local `serena`.
`[Evidenced — code.claude.com/docs/en/desktop]`

**Claude Code** `[Evidenced — code.claude.com/docs/en/mcp-quickstart]`:

There is no in-session “Add local server” wizard. In a **terminal**
(not inside `claude`), from the Java plant:

```bash
cd /ABS/PATH/TO/ocs-api-service
claude mcp add --scope user serena -- serena start-mcp-server --context claude-code --project "$(pwd)" --mode planning
```

Or `serena setup claude-code`. Then start `claude`, type **`/mcp`**, confirm
`serena` is connected. Toggle/reconnect there; adding is CLI.

Claude Code **desktop** Code tab: Connectors UI is the same catalog. Custom
stdio still goes through `claude mcp add` / `~/.claude.json`.


Smoke (before the 12 questions): “Using Serena `find_symbol`, name one class
under `src/main/java` with `file:line`.” Empty → Java backend not up (§4), not
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
Your local DeepWiki MCP (`https://mcp.deepwiki.com/mcp`) `[Evidenced — docs.devin.ai]`.

Call **`ask_question`** with `repoName`: `oraios/serena`:

1. How do I register Serena for Claude Code vs Cursor (`ide`) vs IntelliJ Copilot?
2. How is Java `eclipse.jdt.ls` installed (VSIX vs `jdtls_path` + `lombok_path`)?
3. When should I use `serena init -b JetBrains` instead of jdtls?

Paste the Ask URLs into the S0 log. Primary docs above still win on conflict.
