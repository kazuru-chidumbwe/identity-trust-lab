# Release tags

Annotated tags mark reproducible anchors. **`main` may advance** after a tag — always `git checkout <tag>` when reproducing a cited result.

| Tag | Commit | Purpose |
| --- | --- | --- |
| [`v0.1.0`](https://github.com/kazuru-chidumbwe/identity-trust-lab/releases/tag/v0.1.0) | `77938ec` | First SemVer release |
| [`case1-partial-2026-07`](https://github.com/kazuru-chidumbwe/identity-trust-lab/tree/case1-partial-2026-07) | `77fcb8e` | Dual-IdP Case 1 partial measurement pin |

## Quick checkout

```bash
git checkout v0.1.0
./scripts/quick_test.sh
```

## Tag policy

- **SemVer** → `v0.1.0` (see [`CHANGELOG.md`](../CHANGELOG.md)).
- Case 1 measurement cite → `case1-partial-2026-07`.
- Never cite floating `main` for published results.
- New SemVer tags when the release boundary changes — not on every doc commit.
