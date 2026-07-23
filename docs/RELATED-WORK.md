# Related work

Niche: **reproducible benign semantic comparison** under identical OIDC profiles — complementary to attack testing and conformance.

## Security analysis / offensive evaluation

1. Christian Mainka, Vladislav Mladenov, Jörg Schwenk, Tobias Wich. **SoK: Single Sign-On Security — An Evaluation of OpenID Connect.** IEEE EuroS&P 2017. Introduces **PrOfESSOS** (Practical Offensive Evaluation of Single Sign-On Services).  
   https://doi.org/10.1109/EuroSP.2017.32 · tool: https://github.com/RUB-NDS/PrOfESSOS

2. Daniel Fett, Ralf Küsters, Guido Schmitz. **The Web SSO Standard OpenID Connect: In-Depth Formal Security Analysis and Security Guidelines.** IEEE CSF 2017.  
   https://doi.org/10.1109/CSF.2017.20

## Compliance / ecosystem measurement

3. Pieter Philippaerts, Davy Preuveneers, Wouter Joosen. **OAuch: Exploring Security Compliance in the OAuth 2.0 Ecosystem.** RAID 2022.  
   https://doi.org/10.1145/3545948.3545955 · https://oauch.io/

4. OpenID Foundation. **OpenID Connect Conformance Test Suite** (certification tooling).  
   https://openid.net/certification/

## JWT implementation differential testing

5. **Token Time Bomb: Evaluating JWT Implementations for Vulnerability Discovery** (JWTeemo). NDSS 2026.  
   https://www.ndss-symposium.org/ndss-paper/token-time-bomb-evaluating-jwt-implementations-for-vulnerability-discovery/  
   https://github.com/JWTeemo/JWTeemo

## How this lab differs

| Line of work | Typical question | This lab |
| --- | --- | --- |
| PrOfESSOS / formal OIDC analysis | Can the protocol/implementation be attacked or proven secure? | Do pinned IdPs **agree semantically** under one profile? |
| OAuch / Conformance Suite | Does the AS implement required security/conformance checks? | Where do **normalized** outputs diverge for migrators? |
| JWTeemo | Do JWT **libraries** disagree dangerously on parsing? | Do **IdP token endpoints** disagree on refresh semantics? |
