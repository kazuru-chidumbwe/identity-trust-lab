!/usr/bin/env bash
# Smoke gate: Keycloak + WSO2 normalize paths + Case 1 partial matrix present.
set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/normalize_smoke.sh

OUT_W="artifacts/normalize-smoke/wso2-normalized.json"
python3 drivers/wso2/normalize.py fixtures/wso2-token-raw.json -o "$OUT_W"
python3 - <<'PY'
import json, sys
from pathlib import Path
n = json.loads(Path("artifacts/normalize-smoke/wso2-normalized.json").read_text())
required = [
    "http_status", "error", "token_type", "expires_in",
    "refresh_issued", "claim_keys_id", "claim_keys_access", "access_token_is_jwt",
]
missing = [k for k in required if k not in n]
if missing:
    print("FAIL wso2 missing fields:", missing)
    sys.exit(1)
if n["http_status"] != 200 or not n["refresh_issued"]:
    print("FAIL unexpected wso2 values", n)
    sys.exit(1)
if "sub" not in n["claim_keys_id"]:
    print("FAIL wso2 id token keys missing sub", n["claim_keys_id"])
    sys.exit(1)
if n["access_token_is_jwt"] is not False:
    print("FAIL expected opaque WSO2 access token in this pin", n)
    sys.exit(1)
print("PASS wso2 normalize →", "artifacts/normalize-smoke/wso2-normalized.json")

m = json.loads(Path("results/case1-partial/matrix-C1-token-shape-2026-07-23.json").read_text())
assert m["rows"][0]["verdict"] == "same"
assert m["rows"][1]["feature"] == "access_token_is_jwt" and m["rows"][1]["verdict"] == "config_drift"
assert m["rows"][2]["feature"] == "token_lifetime_expires_in" and m["rows"][2]["verdict"] == "config_drift"
assert m["rows"][2]["observed"]["keycloak"]["expires_in"] == 300
assert m["rows"][2]["observed"]["wso2is"]["expires_in"] == 3600
assert m["rows"][3]["feature"] == "id_token_claim_key_set_email_profile" and m["rows"][3]["verdict"] == "config_drift"
assert m["rows"][3]["observed"]["keycloak"]["has_email"] is True
assert m["rows"][3]["observed"]["wso2is"]["has_email"] is False
assert len(m["rows"]) == 4
assert m["config_equivalence"]["passed"] is False
assert m["config_equivalence"].get("checklist_id") == "CE-TOKEN-SHAPE-v0"
ce = json.loads(Path("results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json").read_text())
assert ce["passed"] is False
assert ce["checklist_id"] == "CE-TOKEN-SHAPE-v0"
assert any(i["id"] == "access_token_lifetime_expires_in" and i["equated"] is False for i in ce["items"])
assert any(i["id"] == "access_token_jwt" and i["equated"] is False for i in ce["items"])
assert any(i["id"] == "id_token_claim_key_set_email_profile" and i["equated"] is False for i in ce["items"])
print("PASS case1 partial matrix present (", len(m["rows"]), "rows)")
print("PASS config-equivalence CE-TOKEN-SHAPE-v0 present (passed=false)")
PY

echo "PASS: dual-IdP partial lab evidence smoke green."
