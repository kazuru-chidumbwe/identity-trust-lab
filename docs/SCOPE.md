# Scope

## In scope (public tree)

- OIDC profile + matrix schemas with closed `verdict` enum
- Shared token-response **normalizer** (`drivers/common`)
- Keycloak + WSO2 IS drivers (normalize entrypoints)
- Redacted live captures from lab alias **itl-lab**
- Case 1 **partial** matrix (token-endpoint shape): Keycloak 26.0.7 vs WSO2 IS 7.0.0

## Out of scope (this tree)

- Product rankings or marketing comparisons
- Conformance certification claims
- Offensive exploit write-ups
- Unredacted production tokens or realm exports
- Venue / paper submission roadmaps

## Drivers

Drivers are IdP-specific. Public normalize paths are exercised on **Keycloak** and **WSO2 Identity Server**. Additional IdP drivers use the same profile and matrix contracts when present.
