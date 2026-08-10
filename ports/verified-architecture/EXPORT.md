# Export to a new GitHub repository

This folder is a **self-contained planning repository**: standards, requirements,
constraints, C4, ADRs, **full research corpus**, and **nested BC packages** with
MDC for progressive agent context.

```bash
gh repo create huntyyyyyy/verified-architecture --public \
  --description "Polyglot verified architecture — RE/ATAM/C4/ADR + research nests (working draft)"

# copy this directory out of spring-boot-doc-agent, then:
cd verified-architecture
git init -b main
git add -A
git commit -m "Planning SoR: ISO/ATAM draft, research corpus, nested MDC BCs"
git remote add origin git@github.com:huntyyyyyy/verified-architecture.git
git push -u origin main
```

Cloud agent tokens often cannot `createRepository` — run the create step from
your account.
