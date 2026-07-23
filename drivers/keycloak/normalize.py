#!/usr/bin/env python3
"""Normalize raw OIDC token-endpoint material into comparable fields."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path
from typing import Any


def _b64url_json(segment: str) -> dict[str, Any] | None:
    try:
        pad = "=" * (-len(segment) % 4)
        raw = base64.urlsafe_b64decode(segment + pad)
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return None


def _jwt_claim_keys(token: str | None) -> list[str]:
    if not token or token.count(".") < 2:
        return []
    payload = _b64url_json(token.split(".")[1])
    if not isinstance(payload, dict):
        return []
    return sorted(payload.keys())


def normalize_token_response(
    *,
    http_status: int,
    body: dict[str, Any],
    refresh_reuse_accepted: bool | None = None,
) -> dict[str, Any]:
    """Map a token-endpoint response to the methodology field set."""
    err = body.get("error")
    return {
        "http_status": http_status,
        "error": err if isinstance(err, str) else None,
        "error_description": body.get("error_description")
        if isinstance(body.get("error_description"), str)
        else None,
        "token_type": body.get("token_type")
        if isinstance(body.get("token_type"), str)
        else None,
        "expires_in": body.get("expires_in")
        if isinstance(body.get("expires_in"), int)
        else None,
        "refresh_issued": isinstance(body.get("refresh_token"), str)
        and len(body.get("refresh_token", "")) > 0,
        "refresh_reuse_accepted": refresh_reuse_accepted,
        "claim_keys_id": _jwt_claim_keys(
            body.get("id_token") if isinstance(body.get("id_token"), str) else None
        ),
        "claim_keys_access": _jwt_claim_keys(
            body.get("access_token")
            if isinstance(body.get("access_token"), str)
            else None
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "raw_json",
        type=Path,
        help="Raw capture: {http_status, body, refresh_reuse_accepted?}",
    )
    p.add_argument("-o", "--out", type=Path, help="Write normalized JSON here")
    args = p.parse_args()
    raw = json.loads(args.raw_json.read_text(encoding="utf-8"))
    norm = normalize_token_response(
        http_status=int(raw["http_status"]),
        body=dict(raw["body"]),
        refresh_reuse_accepted=raw.get("refresh_reuse_accepted"),
    )
    text = json.dumps(norm, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
