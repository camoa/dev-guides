---
description: Pixelmatch options beyond threshold — includeAA, alpha, aaColor, diffColor, diffColorAlt, and diffMask, with patterns for directional diff visualization.
tldr: Use diffColorAlt to distinguish additions from removals in the diff PNG, and diffMask to get a transparent-background overlay. Avoid includeAA true unless captures are pinned to identical rendering environments, and avoid alpha 1 which hides the diff overlay behind the original image.
---

# Pixelmatch Other Options

## When to Use

> Use this when customizing the diff visualization or changing anti-aliasing behavior beyond the default.

## Decision

| Option | Default | Behavior |
|---|---|---|
| `threshold` | `0.1` | YIQ color-distance bound |
| `includeAA` | `false` | When `true`, anti-aliased pixels are not skipped — every changed pixel counts |
| `alpha` | `0.1` | Opacity of original image behind the diff overlay. `0` = white background; `1` = full original |
| `aaColor` | `[255, 255, 0]` (yellow) | Color marking detected anti-aliased pixels in the diff PNG |
| `diffColor` | `[255, 0, 0]` (red) | Color marking differing pixels |
| `diffColorAlt` | `null` | When set, `diffColor` marks img2-darker pixels and `diffColorAlt` marks img2-lighter pixels |
| `diffMask` | `false` | When `true`, diff is drawn on transparent background — no original-image bleed-through |

## Pattern: directional diff visualization

```js
pixelmatch(img1, img2, output, width, height, {
  threshold: 0.1,
  diffColor: [255, 0, 0],          // img2 darker → red
  diffColorAlt: [0, 255, 0],       // img2 lighter → green
});
```

Visually distinguishes "this region got darker" from "this region got lighter" — useful when reviewing layout shifts that change foreground/background relationships.

## Pattern: clean diff mask

```js
pixelmatch(img1, img2, output, width, height, {
  threshold: 0.1,
  diffMask: true,
});
```

Output is just the diff overlay on transparent background — no faded original. Easier to overlay onto either source image manually.

## Common Mistakes

- **Wrong**: `includeAA: true` without identical cross-OS capture conditions — every text edge counts; baselines must be regenerated in the exact same environment
- **Wrong**: `alpha: 1` — full original image obscures the red diff overlay; defeats the visualization
- **Wrong**: Custom diff colors that conflict with Playwright's mask color — `#FF00FF` is Playwright's mask fill; don't reuse it as `diffColor`

## See Also

- [Algorithm](pixelmatch-algorithm.md) — how AA detection works
- [Threshold](pixelmatch-threshold.md) — tuning the YIQ tolerance
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
