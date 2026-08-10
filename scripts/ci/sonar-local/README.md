# Local SonarQube (advisory only)

**Not** Cover% / complexipy / merge SoT. In-repo hard gates remain
`doc-engine quality-gates` + `pre_pr`. SonarCloud in CI stays soft.

## Bring up Community (Docker)

```bash
docker compose -f scripts/ci/sonar-local/docker-compose.yml up -d
# open http://localhost:9000 — change admin password; create project token
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=squ_…
python3 scripts/ci/sonar_local_advisory.py
```

`pre_pr --full` runs this script as an **advisory** suite when present; missing
env → skip exit 0.
