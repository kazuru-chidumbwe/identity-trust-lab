#!/usr/bin/env python3
"""Capture a live Keycloak token response for normalize smoke.

Requires Docker Keycloak (docker/compose.keycloak.yaml) and a realm/client
configured for password or client-credentials grant. Writes fixtures/ and
re-runs normalize.

Example (resource-owner password — lab only):

  export KC_TOKEN_URL=http://localhost:8080/realms/itl/protocol/openid-connect/token
  export KC_CLIENT_ID=itl-lab-client
  export KC_CLIENT_SECRET=...
  export KC_USERNAME=labuser
  export KC_PASSWORD=...
  python3 scripts/keycloak_live_capture.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    token_url = os.environ.get("KC_TOKEN_URL")
    if not token_url:
        print(
            "KC_TOKEN_URL not set. Start docker/compose.keycloak.yaml, "
            "configure realm/client, then export KC_* vars. See script docstring.",
            file=sys.stderr,
        )
        return 2

    data = {
        "grant_type": "password",
        "client_id": os.environ["KC_CLIENT_ID"],
        "username": os.environ["KC_USERNAME"],
        "password": os.environ["KC_PASSWORD"],
        "scope": "openid profile email",
    }
    if secret := os.environ.get("KC_CLIENT_SECRET"):
        data["client_secret"] = secret

    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        token_url, data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            payload = json.loads(resp.read().decode())
    except Exception as e:
        print(f"live capture failed: {e}", file=sys.stderr)
        return 1

    raw = {
        "idp": "keycloak",
        "capture_note": "Live capture via keycloak_live_capture.py",
        "http_status": status,
        "refresh_reuse_accepted": None,
        "body": payload,
    }
    out = ROOT / "fixtures" / "keycloak-token-raw.json"
    out.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
