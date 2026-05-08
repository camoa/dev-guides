---
description: How pixelmatch's YIQ perceptual color difference and anti-aliasing detection algorithms work, and what counts as "different."
tldr: Pixelmatch uses YIQ color space (luminance-weighted) to compare pixels perceptually, then skips pixels on anti-aliased edges by default. Setting includeAA true or threshold 0 does not mean raw byte comparison — the algorithm is always perceptual.
---

# Pixelmatch Algorithm

## When to Use

> Read this when tuning thresholds or debugging "why was this pixel flagged?" — understanding the two algorithmic ideas explains every pixelmatch decision.

## Decision

| Pixel pair | Counted as different? |
|---|---|
| Identical RGBA | No |
| Slight chroma shift | Probably no (YIQ weights luma) |
| Slight luminance shift | Yes if past `threshold` |
| Both pixels are anti-aliased edges | No (skipped) — unless `includeAA: true` |
| One pixel changed but it's anti-aliased | No (skipped) |

## Pattern

Per-pixel decision flow:

1. **RGBA equal** → skip (no diff)
2. Compute YIQ delta
3. **Delta within `threshold²`-scaled bound** → equal
4. **Either pixel is anti-aliased AND `includeAA` is false** → mark as AA (yellow), skip
5. **Otherwise** → mark as diff (red), increment counter

## Two Algorithmic Ideas

**YIQ perceptual color difference** — converts each pixel to YIQ (NTSC luma + chroma) and computes a perceptually weighted distance. Y (luminance) dominates because the human eye is more sensitive to brightness than chroma. A hue shift (Q channel) is judged less different than a brightness shift (Y channel).

**Anti-aliasing detection** — before flagging a pixel as different, pixelmatch checks whether either pixel sits on an anti-aliased edge by examining 8 neighbors for the characteristic intensity-slope pattern. AA pixels are skipped by default to suppress false positives from sub-pixel font/edge rendering differences.

## Common Mistakes

- **Wrong**: Expecting pixel-perfect raw-RGB comparison — pixelmatch is perceptual; `threshold: 0` does not mean "every byte equal"
- **Wrong**: Setting `includeAA: true` without understanding consequences — every text rendering tick now counts as a diff
- **Wrong**: Confusing AA detection with masking — AA detection is automatic; masking is the `mask` option in Playwright

## See Also

- [Threshold](pixelmatch-threshold.md) — tuning the YIQ tolerance
- [Other Options](pixelmatch-other-options.md) — `includeAA`, `aaColor`, `diffColor`, `diffMask`
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
