#!/usr/bin/env bash
# Run the spring-signals queries against a database and emit CSV, then assert.
#
#   DB            database path
#   PACKS         pack search root
#   OUT           output directory
#   CODEQL        codeql executable
#   QUERIES       space-separated query basenames (default: the wave 1 set)
#   EXPECTATIONS  JSON file of expected counts. Default: the ocs-api-service
#                 spec, so the Messaging=0 gate is ON by default -- a gate
#                 that is opt-in is a gate that is silently off. Set to "off"
#                 for a deliberate report-only run.
#   EXTRA_PACKS   optional air-gap tree for codeql/java-all (see create-db.sh)
#
# Note on `@kind table`: these queries produce raw result tables, not alerts.
# `codeql database analyze` will NOT interpret them into SARIF -- it needs
# @kind problem/path-problem. Raw tables must go through `query run` +
# `bqrs decode`, which is what this script does. If a downstream consumer
# expects SARIF, that is a schema decision to make deliberately, not a
# side effect of query metadata.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CODEQL_ROOT="$(cd "$HERE/../codeql" && pwd)"
DB="${DB:-$PWD/.codeql/ocs-api-service-db}"
PACKS="${PACKS:-$CODEQL_ROOT/packs}"
OUT="${OUT:-$PWD/out}"
CODEQL="${CODEQL:-codeql}"
EXPECTATIONS="${EXPECTATIONS:-$HERE/expectations/ocs-api-service.json}"

# Workspace packs resolve via codeql-workspace.yml (cwd=$CODEQL_ROOT). Only
# EXTRA_PACKS needs --additional-packs (offline java-all). --no-strict-mode is
# pack-install-only (query run/compile reject it).
PACK_INSTALL_ARGS=(--no-strict-mode)
QUERY_ARGS=()
if [[ -n "${EXTRA_PACKS:-}" ]]; then
  PACK_INSTALL_ARGS+=(--additional-packs="$EXTRA_PACKS")
  QUERY_ARGS+=(--additional-packs="$EXTRA_PACKS")
fi

# Wave 1 only. References/Security/Observability/Testing still emit the legacy
# 3-column schema and are excluded on purpose. Override QUERIES to run a subset.
DEFAULT_QUERIES="ApiSurface Configuration ErrorHandling HibernateTypes JakartaMigration Messaging NativeSql OpenApiSurface OutboundClients Persistence"
read -r -a WAVE1 <<< "${QUERIES:-$DEFAULT_QUERIES}"

# Clean, then recreate. A CSV whose query was dropped from the wave list would
# otherwise survive into the assertion step as stale data; derived output is
# rebuilt from scratch every run. The engine's unexpected-CSV check is the
# backstop; this is the hygiene.
rm -rf "$OUT"
mkdir -p "$OUT"

# Precompile into a cache the query runs actually use. `pack create` alone wrote
# a compiled pack that the loop then ignored, recompiling from source on every
# query -- so the wall-clock term this step exists to remove was still in every
# CodeQL-vs-ast-grep timing.
(
  cd "$CODEQL_ROOT"
  "$CODEQL" pack install "${PACK_INSTALL_ARGS[@]}" packs/spring-signals >/dev/null
)
export CODEQL_COMPILATION_CACHE="${CODEQL_COMPILATION_CACHE:-$OUT/.compcache}"
mkdir -p "$CODEQL_COMPILATION_CACHE"
(
  cd "$CODEQL_ROOT"
  "$CODEQL" query compile --ram=16384 \
    "${QUERY_ARGS[@]}" \
    --compilation-cache="$CODEQL_COMPILATION_CACHE" \
    packs/spring-signals >/dev/null
)

for q in "${WAVE1[@]}"; do
  echo "== $q"
  (
    cd "$CODEQL_ROOT"
    "$CODEQL" query run --ram=16384 \
      --database="$DB" \
      "${QUERY_ARGS[@]}" \
      --compilation-cache="$CODEQL_COMPILATION_CACHE" \
      --output="$OUT/$q.bqrs" \
      "packs/spring-signals/$q.ql" >/dev/null
  )
  "$CODEQL" bqrs decode --format=csv --entities=string \
    "$OUT/$q.bqrs" > "$OUT/$q.csv"
  echo "   rows: $(( $(wc -l < "$OUT/$q.csv") - 1 ))"
done

echo
if [[ "$EXPECTATIONS" != "off" ]]; then
  python3 "$HERE/check-assertions.py" --out "$OUT" --expectations "$EXPECTATIONS"
else
  echo "EXPECTATIONS=off: row counts reported but nothing asserted (deliberate)."
fi
