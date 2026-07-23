# Reproduce

## Dual-IdP normalize + Case 1 partial (current public gate)

```bash
./scripts/quick_test.sh
```

Expect exit 0, Keycloak + WSO2 normalized artifacts under `artifacts/normalize-smoke/`, and Case 1 partial matrix checks.

## Frozen measurements

| Path | Meaning |
| --- | --- |
| [`results/case1-partial/matrix-C1-token-shape-2026-07-23.json`](../results/case1-partial/matrix-C1-token-shape-2026-07-23.json) | First dual-IdP rows on itl-lab |
| Tag `case1-partial-2026-07` | Measurement tag for the above (when published) |

When a matrix or capture is published as evidence, cite the **Git tag** (not necessarily `main`) and verify any SHA published with that citation.

## Lab environment

Public alias **itl-lab** (`uname_r` 6.8.0-134-generic):

- Keycloak `quay.io/keycloak/keycloak:26.0.7`
- WSO2 Identity Server `wso2/wso2is:7.0.0`

Kernel and image pins are recorded in each fixture `lab_environment` object. Config checklist: [`config-equivalence-case1-partial.md`](config-equivalence-case1-partial.md).
