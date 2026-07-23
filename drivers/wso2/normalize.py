#!/usr/bin/env python3
"""WSO2 IS driver entry — delegates to shared normalizer."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
from normalize import main, normalize_token_response  # noqa: E402,F401

if __name__ == "__main__":
    raise SystemExit(main())
