---
description: Scenario-by-scenario pixelmatch threshold reference — which value to pick and when to combine with maxDiffPixels.
tldr: Start with Playwright's default of 0.2 and stabilize the suite, then tighten incrementally toward 0.1. For cross-OS captures use 0.2–0.3; for animations and gradients prefer maxDiffPixels (an absolute cap, sized from a measured residual) over raising threshold. Document every non-default per-test threshold with a comment.
---

# Pixelmatch Tuning Recipes

## When to Use

> Use this as the scenario-by-scenario reference for picking a `threshold` value.

## Decision

| Scenario | `threshold` | Notes |
|---|---|---|
| Pixel-perfect, same OS, same browser version | `0.1` (library default) | Catches real regressions; rare false positives |
| Same OS, anti-aliasing variability (Canvas/WebGL) | `0.1` with `includeAA: false` (default) | AA detector handles most of it |
| Cross-OS (mac vs Linux CI) | `0.2`–`0.3` | Combine with `maxDiffPixelRatio: 0.01` to absorb noise |
| Different font hinting / sub-pixel rendering across OSes | `0.3+`, or switch to looks-same / dssim | Pixelmatch's YIQ saturates here; perceptual SSIM is more stable |
| Animations, gradients, video frames | Use `maxDiffPixels` / `maxDiffPixelRatio` rather than raising threshold | Keeps regression sensitivity high while tolerating bounded noise |

## Pattern: incremental tightening

Start with Playwright's defaults (`threshold: 0.2`, no `maxDiffPixels`). When tests are stable, tighten:

1. Lower `threshold` to `0.15`, then `0.1`
2. If — and only if — repeat runs against an unchanged site show a residual, add a `maxDiffPixels` ceiling sized from that residual (absolute, not a ratio, so it does not scale with page height)
3. For sub-pixel-precise components, override per-test with `threshold: 0.05` and a comment

If tightening produces flakes, the env or stability controls (animations, fonts) are the real problem. Don't bandaid with looser thresholds.

## Common Mistakes

- **Wrong**: Setting `threshold: 0.5+` as the default — effectively not testing
- **Wrong**: Per-test thresholds without a `// why` comment — six months later the comment is the only justification
- **Wrong**: Tightening on day one — start lax, stabilize, then tighten

## See Also

- [Inside Playwright](pixelmatch-inside-playwright.md) — `maxDiffPixels` and `maxDiffPixelRatio` explained
- [Threshold](pixelmatch-threshold.md) — what the threshold value means mechanically
- [Limitations & Alternatives](pixelmatch-limitations.md) — when to switch algorithms entirely
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
- Reference: [odiff (faster alternative)](https://github.com/dmtrKovalenko/odiff)
