# Config equivalence — human summary for `P-TOKEN-SHAPE-v0` (2026-07-23)

**Machine-checkable record:** [`../results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json`](../results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json)  
**Protocol:** [`config-equivalence-protocol.md`](config-equivalence-protocol.md)

**Lab alias:** itl-lab · Keycloak `26.0.7` · WSO2 IS `7.0.0`  
**`passed`:** **false** → no `implementation_drift` rows on this pin

| Item id | Equated? | Required for drift gate? | Threshold (short) |
| --- | --- | --- | --- |
| `grant_type` | yes | yes | exact `password` |
| `requested_scopes` | yes | yes | set equality `{openid,profile,email}` |
| `access_token_lifetime_expires_in` | **no** (300 vs 3600) | yes | integer equality |
| `refresh_token_presence` | yes | no | both `refresh_issued` |
| `refresh_lifetime_or_rotation` | n/a both | no | out of scope for this profile |
| `pkce` | n/a both | no | password grant |
| `access_token_jwt` | **no** (true vs false) | yes | boolean equality |
| `id_token_claim_key_set_email_profile` | **no** | yes | `email` ∈ claim_keys_id |
| `http_client` | yes | yes | both urllib |
| `lab_host` | yes | yes | same alias + `uname_r` |
| `clock_skew_tolerance` | **not checked** | no | unset on this pin |

**Flow note:** password grant stand-in vs future `P-REFRESH-REUSE-v0` (auth-code+PKCE) — see methodology threats.
