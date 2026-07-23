# Reproduce

## Normalize smoke (current public gate)

```bash
./scripts/quick_test.sh
```

Expect exit 0 and `artifacts/normalize-smoke/keycloak-normalized.json` with the methodology field set.

## Frozen measurements

When a matrix or capture is published as evidence, cite the **Git tag** (not necessarily `main`) and verify any SHA published with that citation.

## Lab environment

Live Keycloak normalize smoke used public alias **stackdiff-lab**, image `quay.io/keycloak/keycloak:26.0.7`, kernel release recorded in the fixture `lab_environment` object.
