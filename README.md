# Identity Trust Lab

Reusable **OIDC semantic measurement** framework: identical profiles across identity providers → normalized traces → deviation matrix.

Not a product shootout. Not a conformance suite. Synthetic / lab IdPs only.

## Status

| Item | State |
| --- | --- |
| Matrix cell model | [`schemas/matrix.schema.json`](schemas/matrix.schema.json) — closed `verdict` enum |
| Methodology | [`docs/methodology.md`](docs/methodology.md) |
| Related work | [`docs/RELATED-WORK.md`](docs/RELATED-WORK.md) |
| Keycloak normalize | `./scripts/quick_test.sh` green |
| Lab pin (normalize smoke) | itl-lab · Keycloak 26.0.7 · `uname_r` 6.8.0-134-generic · claim keys from live JWTs (signatures/refresh redacted in public fixture) |

## Quick start

```bash
git clone https://github.com/kazuru-chidumbwe/identity-trust-lab
cd identity-trust-lab
./scripts/quick_test.sh
# → PASS; writes artifacts/normalize-smoke/keycloak-normalized.json
```

Optional live re-capture (local Docker):

```bash
docker compose -f docker/compose.keycloak.yaml up -d
# configure realm/client, then set KC_* env vars — see scripts/keycloak_live_capture.py
python3 scripts/keycloak_live_capture.py
./scripts/normalize_smoke.sh
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
