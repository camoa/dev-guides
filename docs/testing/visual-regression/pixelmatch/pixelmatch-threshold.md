---
description: How to tune the pixelmatch threshold option — what the values mean, how they differ from Playwright's default, and which value to pick per scenario.
tldr: Lower threshold is stricter — it reduces the maximum allowed YIQ delta per pixel before flagging a diff. The pixelmatch library default is 0.1; Playwright overrides it to 0.2. Bump threshold only to absorb genuine env noise, never to silence flake.
---

# Pixelmatch Threshold

## When to Use

> Use this when tuning how forgiving the comparison is — picking the right threshold for your capture environment.

## Decision

| Goal | Threshold |
|---|---|
| Catch every meaningful change, accept minor noise | `0.1` (library default) |
| Default Playwright posture (slightly forgiving) | `0.2` |
| Cross-OS comparisons (mac vs Linux CI) | `0.2`–`0.3` |
| Components with shadows, blurs, video posters | `0.3` |
| Different font hinting across OSes | Above `0.4` — switch tools or fix the env |

## Pattern

```js
pixelmatch(img1, img2, output, width, height, { threshold: 0.1 });
```

| Aspect | Value |
|---|---|
| Type | `number` in `[0, 1]` |
| **Library default** | **0.1** |
| **Playwright default** | **0.2** |
| Maps to | A perceived YIQ color-distance bound |
| `0` | Effectively requires exact pixel match |
| `1` | Anything counts as the same |

## Why Lower Is Stricter

`threshold` is the **maximum allowed difference per pixel** before a pixel is flagged. Lower = stricter. Higher = laxer. Setting `threshold: 0` means any perceived YIQ delta whatsoever counts as different — effectively pixel-perfect, modulo the AA detector.

## Common Mistakes

- **Wrong**: Assuming "0 = lax, 1 = strict" — it's reversed; 0 is strictest
- **Wrong**: Bumping threshold to silence flake — masks real regressions; fix the env first
- **Wrong**: Setting per-test threshold without a comment — document why the non-default value is needed

## See Also

- [Other Options](pixelmatch-other-options.md) — `maxDiffPixels`, `maxDiffPixelRatio` (Playwright additions)
- [Inside Playwright](pixelmatch-inside-playwright.md) — why Playwright defaults to 0.2 instead of 0.1
- [Tuning Recipes](pixelmatch-tuning-recipes.md) — scenario-by-scenario threshold reference
