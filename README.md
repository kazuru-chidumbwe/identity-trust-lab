# Identity Trust Lab

Reusable OIDC semantic measurement framework: identical profiles across identity providers > field extraction v0 > deviation matrix.

Not a product shootout. Not a conformance suite. Synthetic / lab IdPs only. Normalization (full semantic mapping) is a future layer.

## Status

| Item | State |
| --- | --- |
| Matrix cell model | [`schemas/matrix.schema.json`](schemas/matrix.schema.json) — closed `verdict` enum |
| Methodology | [`docs/methodology.md`](docs/methodology.md) |
| Related work | [`docs/RELATED-WORK.md`](docs/RELATED-WORK.md) |
| Dual-IdP Case 1 (partial) | [`results/case1-partial/matrix-C1-token-shape-2026-07-23.json`](results/case1-partial/matrix-C1-token-shape-2026-07-23.json) — Keycloak vs WSO2 IS |
| Normalize smoke | Keycloak + WSO2 · `./scripts/quick_test.sh` green |
| Lab pin | itl-lab · KC `26.0.7` · WSO2 IS `7.0.0` · `uname_r` 6.8.0-134-generic |

## Quick start

```bash
git clone https://github.com/kazuru-chidumbwe/identity-trust-lab
cd identity-trust-lab
./scripts/quick_test.sh
# → PASS; Keycloak + WSO2 normalize + Case 1 partial matrix checks
```

## Partial lab evidence (instrument validation)

Under matched grant + scopes on itl-lab (`P-TOKEN-SHAPE-v0`):

| Feature | Verdict |
| --- | --- |
| Password+openid issues tokens (200 / Bearer / refresh / `sub`) | `same` |
| Access token is JWT | `config_drift` — KC default JWT vs WSO2 IS 7.0.0 default opaque |
| `expires_in` token lifetime | `config_drift` — 300s vs 3600s (lifetimes not equated) |
| ID-token `email` after `profile`+`email` scopes | `config_drift` — KC `has_email: true` vs WSO2 `has_email: false` (claim mapping not equated) |

Operational checklist: [`results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json`](results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json) (`passed: false`).  
Protocol: [`docs/config-equivalence-protocol.md`](docs/config-equivalence-protocol.md).  

**Not** a claim about IdPs in general — pinned lab snapshot only. Pipeline term: field extraction v0 (normalization = future layer).

Optional live re-capture:

```bash
docker compose -f docker/compose.keycloak.yaml up -d
# … KC_* env — see scripts/keycloak_live_capture.py

docker compose -f docker/compose.wso2.yaml up -d
# wait for :9443, then:
python3 scripts/wso2_live_capture.py
python3 scripts/redact_wso2_fixture.py
```

## Research question

Given identical OpenID Connect profiles, do independent IdPs expose identical protocol semantics?

Pairwise matrices validate the instrument on pinned versions. They do not license claims about IdPs in general.

## Framework

1. **Profile** — deterministic OIDC scenario JSON  
2. **Drivers** — same profile bytes → each IdP → raw capture  
3. **Field extraction v0** — HTTP + tokens → comparable fields (normalization = future semantic-mapping layer; not implemented on this pin)  
4. **Deviation matrix** — rows with `verdict` ∈ {`same`, `config_drift`, `implementation_drift`, `undefined`, `harness_error`}

## Docs

- [`docs/methodology.md`](docs/methodology.md) — equivalence, validity threats, disclosure  
- [`docs/RELATED-WORK.md`](docs/RELATED-WORK.md)  
- [`docs/repro.md`](docs/repro.md)  
- [`docs/SCOPE.md`](docs/SCOPE.md)

## License

MIT (see [`LICENSE`](LICENSE)).
