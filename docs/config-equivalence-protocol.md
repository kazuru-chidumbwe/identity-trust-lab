# Config equivalence protocol (operational)

**Schema:** [`schemas/config-equivalence.schema.json`](../schemas/config-equivalence.schema.json)

## Rule (machine-facing)

1. Every checklist item records an **observable**, a **how_checked** procedure, **evidence** pointers, per-IdP **values**, a **compare** operator, a **threshold**, and `equated` boolean.  
2. Items with `required_for_implementation_drift: true` must all have `equated: true` for `passed: true`.  
3. Matrix rows may use verdict `implementation_drift` **only** when the checklist cited by the matrix has `passed: true`.  
4. If `passed: false`, allowed comparative verdicts are `same`, `config_drift`, `undefined`, `harness_error`.

## This pin

Filled checklist: [`results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json`](../results/case1-partial/config-equivalence-CE-TOKEN-SHAPE-v0.json)  
Human summary: [`config-equivalence-case1-partial.md`](config-equivalence-case1-partial.md)

`passed: false` on this pin — lifetimes and JWT access-token defaults were not equated before capture.

## Compare operators

| `compare` | Pass when |
| --- | --- |
| `exact` | Per-IdP values are equal |
| `set_eq` | Sets of tokens/names are equal |
| `numeric_eq` | Numbers equal under `threshold` (this pin: integer equality, no tolerance) |
| `presence_eq` | Boolean presence flags equal |
| `both_n_a` | Both sides intentionally out of scope for this profile |

## Adding a check later

Add an item to a new checklist version (`0.2`, …). Do not silently edit a checklist cited by a frozen matrix tag.
