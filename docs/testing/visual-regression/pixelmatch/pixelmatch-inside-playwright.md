---
description: How Playwright wraps pixelmatch in toHaveScreenshot — default differences, and the two extra thresholds Playwright adds on top of the pixel count.
tldr: Playwright defaults to threshold 0.2 (pixelmatch's own default is 0.1) and adds two extra knobs — maxDiffPixels and maxDiffPixelRatio — on top of the raw pixel count. Without either extra knob configured, any non-zero diff fails the test.
---

# Inside Playwright: How Playwright Uses Pixelmatch

## When to Use

> Use this when tuning Playwright VR thresholds — critical for understanding why explicitly setting `threshold: 0.1` in Playwright is stricter than the Playwright default.

## Decision

| Goal | Tune |
|---|---|
| Pixel-level forgiveness (anti-aliasing tolerance) | `threshold` |
| Tolerate small noise pockets in an otherwise stable test | `maxDiffPixels` (small components) or `maxDiffPixelRatio` (full-page) |
| Both | All three; they compose |

## Pattern: layered thresholds

```ts
expect: {
  toHaveScreenshot: {
    threshold: 0.15,              // per-pixel YIQ tolerance
    maxDiffPixelRatio: 0.005,     // 0.5% of total pixels can differ
    // No maxDiffPixels → ratio applies to all sizes
  },
}
```

This says: individual pixels can shift up to YIQ delta 0.15; up to 0.5% of pixels can be flagged before failing.

## The Defaults Differ

| Default | Pixelmatch library | Playwright |
|---|---|---|
| `threshold` | **0.1** | **0.2** |

Playwright's choice is more forgiving — designed to absorb typical variation in real browser captures.

## Two Extra Knobs Playwright Adds

| Option | Default | Job |
|---|---|---|
| `maxDiffPixels` | unset | Absolute integer cap on differing pixels |
| `maxDiffPixelRatio` | unset | Cap as a fraction of total pixels (0–1) |

A test passes when:
- `diffCount <= maxDiffPixels` (if configured), AND
- `diffCount / totalPixels <= maxDiffPixelRatio` (if configured)

If neither is configured, any non-zero diff fails the test.

## Common Mistakes

- **Wrong**: Reading pixelmatch's `0.1` default and writing it into Playwright — explicitly setting `threshold: 0.1` is *stricter* than Playwright's default of `0.2`
- **Wrong**: Setting `maxDiffPixels: 0` — redundant; that's the default behavior
- **Wrong**: Setting both `maxDiffPixels` and `maxDiffPixelRatio` without thought — the strictest of the two wins

## See Also

- [Threshold](pixelmatch-threshold.md) — what threshold values mean
- [Tuning Recipes](pixelmatch-tuning-recipes.md) — scenario-by-scenario threshold reference
- Playwright docs: [toHaveScreenshot options](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
