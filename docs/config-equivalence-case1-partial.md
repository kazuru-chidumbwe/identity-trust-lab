# Config equivalence — Case 1 partial (2026-07-23)

**Lab alias:** itl-lab  
**IdPs:** Keycloak `26.0.7` · WSO2 IS `7.0.0`  
**Profile:** `P-PASSWORD-OPENID-v0` (lab password grant + `openid profile email`)

| Checklist item | Keycloak | WSO2 IS | Equated? |
| --- | --- | --- | --- |
| Grant type | password | password | **yes** |
| Requested scopes | openid profile email | openid profile email | **yes** |
| Access token lifetime | 300s (realm default in capture) | 3600s (product default) | **no** |
| Refresh issued | yes | yes | **yes** (presence) |
| Refresh lifetime / rotation | not measured this row | not measured this row | **n/a** |
| PKCE | n/a (password) | n/a | **n/a** |
| JWT access token | default **JWT** | default **opaque** | **no** |
| ID claim attribute mapping | email/profile claims present | email/profile claims **absent** on id_token | **no** |
| HTTP client | Python urllib | Python urllib | **yes** |
| Host | itl-lab (`uname_r` 6.8.0-134-generic) | same | **yes** |

**Sign-off:** `config_equivalence.passed = false` for rows that depend on lifetimes, JWT access tokens, or claim mappings.

**Allowed verdicts under this checklist:** `same` (basic token success), `config_drift` (JWT vs opaque), not `implementation_drift`.
