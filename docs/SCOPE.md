# Scope

## In this tree

- Profile schema + example refresh-spine profile  
- Deviation-matrix schema with closed `verdict` enum  
- Keycloak token-response **normalizer**  
- Normalize smoke gate (`./scripts/quick_test.sh`)  
- Redacted live Keycloak capture from lab alias **stackdiff-lab**  

## Measurement discipline

- Synthetic / lab IdPs only  
- Programme-neutral public artifacts (claim **keys**, not PII values)  
- Cite **Git tags** for frozen measurements — not necessarily `main`  
- Config equivalence before `implementation_drift`  
- Security-relevant rows: disclosure before public exploit-flavoured language  

## Platforms

Drivers are IdP-specific. This repository’s public normalize path is exercised on **Keycloak**. Additional IdP drivers use the same profile and matrix contracts when present.
