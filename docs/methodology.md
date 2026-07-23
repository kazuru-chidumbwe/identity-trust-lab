# Methodology — OIDC semantic measurement

**Repo:** https://github.com/kazuru-chidumbwe/identity-trust-lab

---

## 1. Goal

Under **identical** OIDC profiles, execute the same client inputs against independent IdP implementations, **normalize** responses to a fixed field set, and emit a **deviation matrix** whose cells use a closed verdict vocabulary.

We measure **benign protocol semantics** (migration-relevant behaviour), not conformance pass/fail and not attack success rates.

### 1.1 Research question

> Given identical OpenID Connect profiles, do independent identity providers expose identical protocol semantics?

### 1.2 What a pairwise pin supports

A two-IdP matrix on pinned versions is an **existence proof that the instrument works**. It does not support claims of the form “OIDC IdPs typically …”.

---

## 2. Apparatus

| Component | Role |
| --- | --- |
| Profile | Versioned JSON scenario (`schemas/profile.schema.json`) |
| Driver | IdP-specific executor; same profile bytes in |
| Normalizer | Maps raw HTTP/token material → comparable fields |
| Matrix | Rows per feature; cells per `schemas/matrix.schema.json` |

### 2.1 Baseline flow and spine

- Flow: Authorization Code + PKCE  
- Spine: refresh-token handling (rotation, reuse, offline vs online)  

---

## 3. Calibration — configuration equivalence

Before any row may carry verdict `implementation_drift`, compared IdPs must pass a documented **config-equivalence** checklist for the lab realm/client:

- Access / refresh / ID token lifetimes  
- Refresh rotation enabled/disabled (matched)  
- Session vs offline access mode  
- PKCE required  
- Claim mappings for the test client  
- Clock skew tolerance  

Failures → row verdict `config_drift` (or exclude the row). Config drift must not be narrated as product inferiority.

---

## 4. Normalization

Raw responses are not compared with unstructured diffs. The normalizer emits at least:

| Field | Meaning |
| --- | --- |
| `http_status` | Token endpoint status |
| `error` / `error_description` | Present if OAuth error |
| `token_type` | Normalized string or null |
| `expires_in` | Integer seconds or null |
| `refresh_issued` | boolean |
| `refresh_reuse_accepted` | boolean or null if not exercised |
| `claim_keys_id` | Sorted list of ID-token claim names (no PII values in public artifacts) |
| `claim_keys_access` | Sorted list of access-token claim names when JWT |
| `access_token_is_jwt` | Whether the access token parses as a JWT |

Public artifacts remain programme-neutral.

---

## 5. Matrix data model (formal object)

A matrix cell is **not** a bare boolean and **not** free text alone.

`verdict` ∈ {

| Value | Meaning |
| --- | --- |
| `same` | Normalized observations match under the profile assertion |
| `config_drift` | Difference explained by failed/unequal config equivalence |
| `implementation_drift` | Config-equivalent setups still disagree on normalized fields |
| `undefined` | Spec/profile does not determine expected behaviour tightly enough |
| `harness_error` | Measurement failure (timeout, driver bug, parse error) — not an IdP finding |

}

`impact` is required when `verdict` ∈ {`config_drift`, `implementation_drift`, `undefined`}.

Schema: [`schemas/matrix.schema.json`](../schemas/matrix.schema.json).

---

## 6. Threats to validity

Even after config equivalence, results may be confounded by:

| Threat | Mitigation |
| --- | --- |
| Host clock drift between containers | Shared chrony/NTP; record `time_sync` in lab manifest; avoid wall-clock assertions where possible |
| Resource contention affecting timing-sensitive fields (`expires_in` boundaries) | Pin CPU/memory in compose; repeat runs; treat borderline expiry as `undefined` if unstable |
| Patch-level drift within a major version | Pin exact image digests on the measurement tag |
| Asymmetric request stacks (SDK vs curl vs raw socket) | Drivers must document HTTP client; prefer one shared HTTP library across drivers |
| Network path asymmetry | Same Docker network; no host-vs-container split for one IdP only |
| Non-deterministic claim sets (session ids) | Compare claim **keys** and selected semantic fields, not raw identifiers |
| Operator error in realm export | Checklist sign-off in matrix `config_equivalence` object |

---

## 7. Responsible disclosure boundary

This programme targets **benign semantic drift**. If a normalized trace nevertheless shows **security-relevant** behaviour (example: reuse of a rotated refresh token silently accepted), we:

1. Label the row privately as security-relevant  
2. **Disclose to the vendor(s)** before any public matrix language that implies exploitability  
3. Publish only after coordination or an agreed timeout  
4. Never present `harness_error` as an IdP vulnerability  

Benign, documented drift may appear on public pins without vulnerability framing.

---

## 8. Reproducibility

- Frozen measurements cite **Git tags** (and optional archival DOI when minted)  
- Lab environment fields travel with the capture (`lab_environment` on fixtures / manifests)  
- `docs/methodology.md` on the cited tag is the methodological record for that measurement  
