# Identity Trust Lab

Reusable **OIDC semantic measurement** framework: identical profiles across identity providers → normalized traces → deviation matrix.

Not a product shootout. Not a conformance suite. Synthetic / lab IdPs only.

## Status

| Item | State |
| --- | --- |
| Matrix cell model | [`schemas/matrix.schema.json`](schemas/matrix.schema.json) — closed `verdict` enum |
| Methodology | [`docs/methodology.md`](docs/methodology.md) |
| Related work | [`docs/RELATED-WORK.md`](docs/RELATED-WORK.md) |
| Dual-IdP Case 1 (partial) | [`results/case1-partial/matrix-C1-token-shape-2026-07-23.json`](results/case1-partial/matrix-C1-token-shape-2026-07-23.json) — Keycloak vs WSO2 IS |
| Normalize smoke | Keycloak + WSO2 · `./scripts/quick_test.sh` green |
| Lab pin | **itl-lab** · KC `26.0.7` · WSO2 IS `7.0.0` · `uname_r` 6.8.0-134-generic |

## Quick start

```bash
git clone https://github.com/kazuru-chidumbwe/identity-trust-lab
cd identity-trust-lab
./scripts/quick_test.sh
# → PASS; Keycloak + WSO2 normalize + Case 1 partial matrix checks
```

## Case 1 partial finding (instrument validation)

Under matched grant + scopes on itl-lab (`P-PASSWORD-OPENID-v0`):

| Feature | Verdict |
| --- | --- |
| Password+openid issues tokens (200 / Bearer / refresh / `sub`) | `same` |
| Access token is JWT | `config_drift` — KC default JWT vs WSO2 IS 7.0.0 default **opaque** |

Config checklist: [`docs/config-equivalence-case1-partial.md`](docs/config-equivalence-case1-partial.md).  
This does **not** support “OIDC IdPs typically…” claims.

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

Pairwise matrices validate the **instrument** on pinned versions. They do not license claims about IdPs in general.

## Framework

1. **Profile** — deterministic OIDC scenario JSON  
2. **Drivers** — same profile bytes → each IdP → raw capture  
3. **Normalization** — HTTP + tokens → comparable fields  
4. **Deviation matrix** — rows with `verdict` ∈ {`same`, `config_drift`, `implementation_drift`, `undefined`, `harness_error`}

## Docs

- [`docs/methodology.md`](docs/methodology.md) — equivalence, validity threats, disclosure  
- [`docs/RELATED-WORK.md`](docs/RELATED-WORK.md)  
- [`docs/repro.md`](docs/repro.md)  
- [`docs/SCOPE.md`](docs/SCOPE.md)

## License

MIT (see [`LICENSE`](LICENSE)).
