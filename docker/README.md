# Docker lab

| Compose | Image | Port |
| --- | --- | --- |
| [`compose.keycloak.yaml`](compose.keycloak.yaml) | `quay.io/keycloak/keycloak:26.0.7` | 8080 |
| [`compose.wso2.yaml`](compose.wso2.yaml) | `wso2/wso2is:7.0.0` | 9443 |

Lab-only credentials. No production realm exports in public trees.

WSO2 startup often takes several minutes. DCR client ids must match `[a-zA-Z0-9_]{15,30}` (see `scripts/wso2_live_capture.py`).
