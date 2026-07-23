#!/usr/bin/env bash
# Smoke gate: Keycloak normalize path.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== identity-trust-lab quick_test =="
bash scripts/normalize_smoke.sh
echo ""
echo "PASS: normalize smoke green."
exit 0
