#!/usr/bin/env python3
"""Redact secrets from a live WSO2 fixture and write normalized artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "drivers" / "common"))
from normalize import normalize_token_response  # noqa: E402


def _redact_jwt(token: str | None) -> str | None:
    if not isinstance(token, str) or token.count(".") < 2:
        return token
    h, p, _ = token.split(".", 2)
    return f"{h}.{p}.REDACTED_LIVE_SIG"


def main() -> int:
    src = ROOT / "fixtures" / "wso2-token-raw.json"
    raw = json.loads(src.read_text(encoding="utf-8"))
    body = dict(raw.get("body") or {})
    for k in ("access_token", "id_token"):
        if k in body:
            body[k] = _redact_jwt(body.get(k))
    if "refresh_token" in body and isinstance(body["refresh_token"], str):
        body["refresh_token"] = "redacted-live-refresh"
    raw["body"] = body
    note = raw.get("capture_note", "")
    if "redacted" not in note.lower():
        raw["capture_note"] = (
            note.rstrip(".")
            + ". Public alias itl-lab. Token signatures and refresh secret "
            "redacted for public tree; claim keys preserved from live capture."
        )
    src.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    norm = normalize_token_response(
        http_status=int(raw["http_status"]),
        body=dict(raw["body"]),
        refresh_reuse_accepted=raw.get("refresh_reuse_accepted"),
    )
    out = ROOT / "artifacts" / "normalize-smoke" / "wso2-normalized.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(norm, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("public fixture + normalized artifact ready →", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
