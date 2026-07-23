# Fixtures

| File | Meaning |
| --- | --- |
| `keycloak-token-raw.json` | Redacted **live** token-endpoint capture from itl-lab (Keycloak 26.0.7). Signatures/refresh redacted; JWT **payload claim keys** preserved. |
| `wso2-token-raw.json` | Redacted **live** token-endpoint capture from itl-lab (WSO2 IS 7.0.0). Signatures/refresh redacted; claim keys preserved. Access token is **opaque** in this pin. |

Do not commit unredacted live tokens (`.live.json`).
