# Export to a new GitHub repository

This tree is the **planning SoR** for Verified Architecture Engine (docs only).

## Create the remote (on your machine)

```bash
# 1) Create empty repo on GitHub (UI or):
gh repo create huntyyyyyy/verified-architecture --public --description "Polyglot verified architecture — RE, constraints, C4, ADRs before code"

# 2) From a clean clone of this port:
cd ports/verified-architecture   # or copy this folder out of spring-boot-doc-agent
git init -b main
git add -A
git commit -m "Initial planning SoR: RE, constraints, C4, polyglot ADRs"
git remote add origin git@github.com:huntyyyyyy/verified-architecture.git
git push -u origin main
```

Alternatively restore from the agent bundle (if you have it):

```bash
git clone /path/to/verified-architecture-initial.bundle verified-architecture
cd verified-architecture
git remote add origin git@github.com:huntyyyyyy/verified-architecture.git
git push -u origin main
```

## What is different from spring-boot-doc-agent ADRs

- Product identity = **polyglot-first** (ADR-0001); Python is peer glue, not majority engine
- Oracle writer is **language-neutral** (ADR-0006) — supersedes “Python tip writer”
- Rust owns engine (ADR-0007); Go chassis; Ruby locks; Clojure brain; TS IDE/MCP
- **No product code** until CONTRIBUTING gate (ADR-0008)
