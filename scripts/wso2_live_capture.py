#!/usr/bin/env python3
"""Capture a live WSO2 IS token response (password grant) for Case 1.

Assumes WSO2 IS listening on WSO2_BASE (default https://127.0.0.1:9443),
admin credentials for DCR, and TLS verify disabled for lab self-signed certs.

Example:

  export WSO2_BASE=https://127.0.0.1:9443
  export WSO2_ADMIN_USER=admin
  export WSO2_ADMIN_PASSWORD=admin
  python3 scripts/wso2_live_capture.py
"""

from __future__ import annotations

import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _req(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    method: str = "GET",
) -> tuple[int, bytes]:
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(r, timeout=60, context=_ctx()) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def dcr_register(base: str, admin_user: str, admin_pass: str) -> dict:
    auth = base64.b64encode(f"{admin_user}:{admin_pass}".encode()).decode()
    body = json.dumps(
        {
            "client_name": "itl-lab-client",
            "grant_types": ["password", "refresh_token", "client_credentials"],
            "redirect_uris": ["http://localhost/callback"],
            "ext_param_client_id": "itl_lab_wso2_client",
        }
    ).encode()
    status, raw = _req(
        f"{base.rstrip('/')}/api/identity/oauth2/dcr/v1.1/register",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
    )
    if status not in (200, 201):
        # Maybe already registered — try get by name is awkward; fail loud.
        raise SystemExit(f"DCR failed HTTP {status}: {raw[:500]!r}")
    return json.loads(raw.decode())


def password_grant(
    base: str, client_id: str, client_secret: str, username: str, password: str
) -> tuple[int, dict]:
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    form = urllib.parse.urlencode(
        {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "openid profile email",
        }
    ).encode()
    status, raw = _req(
        f"{base.rstrip('/')}/oauth2/token",
        data=form,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        payload = json.loads(raw.decode())
    except Exception:
        payload = {"_raw": raw.decode(errors="replace")[:2000]}
    return status, payload


def main() -> int:
    base = os.environ.get("WSO2_BASE", "https://127.0.0.1:9443")
    admin_user = os.environ.get("WSO2_ADMIN_USER", "admin")
    admin_pass = os.environ.get("WSO2_ADMIN_PASSWORD", "admin")
    # Default super-admin user for password grant against newly registered app
    user = os.environ.get("WSO2_USERNAME", "admin")
    password = os.environ.get("WSO2_PASSWORD", "admin")

    client_id = os.environ.get("WSO2_CLIENT_ID")
    client_secret = os.environ.get("WSO2_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("DCR register itl-lab-client…", file=sys.stderr)
        reg = dcr_register(base, admin_user, admin_pass)
        client_id = reg.get("client_id")
        client_secret = reg.get("client_secret")
        print(f"DCR client_id={client_id}", file=sys.stderr)
        if not client_id or not client_secret:
            print(f"DCR response missing credentials: {reg}", file=sys.stderr)
            return 1

    status, payload = password_grant(base, client_id, client_secret, user, password)
    raw = {
        "idp": "wso2is",
        "capture_note": "Live capture via wso2_live_capture.py (password grant)",
        "http_status": status,
        "refresh_reuse_accepted": None,
        "lab_environment": {
            "public_alias": "itl-lab",
            "wso2_image": os.environ.get("WSO2_IMAGE", "wso2/wso2is:7.0.0"),
            "base_url": base,
            "client_id": client_id,
            "grant": "password",
            "scope": "openid profile email",
        },
        "body": payload,
    }
    out = ROOT / "fixtures" / "wso2-token-raw.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    print("wrote", out, "http_status=", status)
    if status != 200:
        print(json.dumps(payload, indent=2)[:800], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
