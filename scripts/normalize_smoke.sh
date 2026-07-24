!/usr/bin/env bash
# Normalize smoke — raw token material → methodology fields.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="artifacts/normalize-smoke/keycloak-normalized.json"
mkdir -p "$(dirname "$OUT")"

python3 drivers/keycloak/normalize.py \
  fixtures/keycloak-token-raw.json \
  -o "$OUT"

python3 - <<'PY'
import json, sys
from pathlib import Path
p = Path("artifacts/normalize-smoke/keycloak-normalized.json")
n = json.loads(p.read_text())
required = [
    "http_status", "error", "token_type", "expires_in",
    "refresh_issued", "claim_keys_id", "claim_keys_access", "access_token_is_jwt",
]
missing = [k for k in required if k not in n]
if missing:
    print("FAIL missing fields:", missing)
    sys.exit(1)
if n["http_status"] != 200 or not n["refresh_issued"]:
    print("FAIL unexpected normalized values", n)
    sys.exit(1)
if "sub" not in n["claim_keys_id"]:
    print("FAIL id token keys missing sub", n["claim_keys_id"])
    sys.exit(1)
if n.get("access_token_is_jwt") is not True:
    print("FAIL expected JWT access token for Keycloak pin", n)
    sys.exit(1)
print("PASS normalize smoke →", p)
print(json.dumps(n, indent=2, sort_keys=True))
PY
