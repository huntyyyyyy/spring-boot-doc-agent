#!/usr/bin/env bash
# Unified spring-signals plant entry (E-OCS0).
#
#   ./harness/run-plant.sh              # fixture (default)
#   ./harness/run-plant.sh fixture
#   SPRING_SIGNALS_PLANT=ocs ./harness/run-plant.sh
#   ./harness/run-plant.sh ocs          # needs checkout + Artifactory
#
# Fixture = CI/merge SoR. OCS = campaign; never soft-greens without credentials.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PLANT="${1:-${SPRING_SIGNALS_PLANT:-fixture}}"
export SPRING_SIGNALS_PLANT="$PLANT"

python3 "$HERE/plant_profile.py" --root "$ROOT" --plant "$PLANT"
status=$?
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

case "$PLANT" in
  fixture)
    exec "$HERE/create-test-db.sh"
    ;;
  ocs)
    CHECKOUT="$(python3 "$HERE/plant_profile.py" --root "$ROOT" --plant ocs --json \
      | python3 -c "import json,sys; print(json.load(sys.stdin)['checkout'])")"
    export REPO="$CHECKOUT"
    export DB="${DB:-$HERE/.codeql/ocs-api-service-db}"
    export EXPECTATIONS="${EXPECTATIONS:-$HERE/expectations/ocs-api-service.json}"
    "$HERE/create-db.sh"
    exec "$HERE/run.sh"
    ;;
  *)
    echo "ERROR: unknown plant $PLANT" >&2
    exit 2
    ;;
esac
