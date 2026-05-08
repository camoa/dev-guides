---
description: What pixelmatch is, where it sits in the JS test ecosystem, and when to use it directly vs through Playwright.
tldr: Use pixelmatch directly when diffing arbitrary PNGs outside Playwright (custom scripts, Puppeteer, Selenium). For standard Playwright VR tests, pixelmatch runs under the hood automatically — read this guide to tune its thresholds correctly.
---

# Pixelmatch Overview

## When to Use

> Use pixelmatch directly when comparing arbitrary PNGs in custom scripts or non-Playwright captures. Use it through Playwright when running standard VR test loops — Playwright handles capture, retry, and the pixelmatch call automatically.

## Decision

| Use Case | Pixelmatch directly | Through Playwright |
|---|---|---|
| Standard VR test loop in Playwright | — | Yes — Playwright handles capture, retry, and pixelmatch under the hood |
| Custom script comparing two arbitrary PNGs | Yes | — |
| Diffing screenshots from Puppeteer/Selenium/Cypress | Yes | — |
| CI script that diffs URL X against reference Y | Yes | — |
| Tuning Playwright `threshold` correctly | Read this guide | — |
| Cross-OS comparisons with font rendering issues | Switch to looks-same / SSIM | Switch to looks-same / SSIM |
| Suite > 500 screenshots, runs are slow | Switch to odiff | Switch to odiff (post-process) |

## Pattern

```js
import pixelmatch from 'pixelmatch';

// Inputs: two decoded RGBA Uint8Array buffers of identical dimensions
// Returns: integer count of differing pixels
const diffCount = pixelmatch(img1.data, img2.data, diff.data, width, height, { threshold: 0.1 });
```

- Repo: github.com/mapbox/pixelmatch
- License: ISC
- Inputs: two RGBA `Uint8Array` buffers of identical dimensions
- Output: integer count of differing pixels + optional diff visualization PNG

## Common Mistakes

- **Wrong**: Treating pixelmatch as the test runner — it's an image-diff library; you need a test framework around it
- **Wrong**: Comparing pixelmatch defaults to Playwright defaults — they differ (Playwright uses `threshold: 0.2`, pixelmatch default is `0.1`)
- **Wrong**: Reaching for pixelmatch when SSIM is right — sub-pixel font hinting differences across OSes need a different algorithm

## See Also

- [Algorithm](pixelmatch-algorithm.md) — how YIQ + AA detection work
- [Inside Playwright](pixelmatch-inside-playwright.md) — how Playwright wraps pixelmatch and where defaults differ
- [Limitations & Alternatives](pixelmatch-limitations.md) — when to switch to odiff or looks-same
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
