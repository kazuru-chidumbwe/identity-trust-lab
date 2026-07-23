#!/usr/bin/env python3
"""Redact live Keycloak capture for public commit; keep claim keys."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "drivers" / "common"))
from normalize import normalize_token_response  # noqa: E402


def b64url_decode(seg: str) -> dict:
    pad = "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg + pad))


def b64url_encode(obj: dict) -> str:
    raw = json.dumps(obj, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def resign(tok: str) -> str:
    h, p, _ = tok.split(".")
    return f"{b64url_encode(b64url_decode(h))}.{b64url_encode(b64url_decode(p))}.REDACTED_LIVE_SIG"


def main() -> int:
    live_path = ROOT / "fixtures" / "keycloak-token-raw.live.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    body = live["body"]
    pub = {
        "idp": live["idp"],
        "capture_note": live["capture_note"]
        + " Token signatures and refresh secret redacted for public tree; claim keys preserved from live capture.",
        "http_status": live["http_status"],
        "refresh_reuse_accepted": None,
        "lab_environment": live["lab_environment"],
        "body": {
            "access_token": resign(body["access_token"]),
            "expires_in": body["expires_in"],
            "refresh_expires_in": body.get("refresh_expires_in"),
            "refresh_token": "redacted-live-refresh",
            "token_type": body["token_type"],
            "id_token": resign(body["id_token"]),
            "scope": body.get("scope"),
        },
    }
    (ROOT / "fixtures" / "keycloak-token-raw.json").write_text(
        json.dumps(pub, indent=2) + "\n", encoding="utf-8"
    )
    norm = normalize_token_response(
        http_status=pub["http_status"],
        body=pub["body"],
        refresh_reuse_accepted=None,
    )
    out = ROOT / "artifacts" / "normalize-smoke" / "keycloak-normalized.json"
    out.write_text(json.dumps(norm, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    live_path.unlink(missing_ok=True)
    print("public fixture + normalized artifact ready")
    print("lab_environment:", json.dumps(pub["lab_environment"]))
    print("claim_keys_id count:", len(norm["claim_keys_id"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
