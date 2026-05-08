---
description: Pixelmatch — decision guides for understanding the algorithm, tuning thresholds, calling the API, reading PNGs, and deciding when to use alternatives.
guide-meta:
  concepts:
    - pixelmatch
    - image diff
    - pixel comparison
    - YIQ color space
    - anti-aliasing detection
    - threshold
    - includeAA
    - diffColor
    - diffColorAlt
    - diffMask
    - alpha
    - pngjs
    - sharp RGBA
    - odiff
    - looks-same
    - SSIM
    - CIEDE2000
    - maxDiffPixels
    - maxDiffPixelRatio
    - PNG RGBA buffer
    - pixelmatch CLI
    - pixelmatch API
    - standalone diff script
    - mapbox pixelmatch
  not:
    - Playwright screenshot capture (see testing/visual-regression/playwright)
    - VR workflow procedure (see testing/visual-regression/workflow)
    - toHaveScreenshot options overview (see playwright guide)
    - Playwright setup and config (see testing/visual-regression/playwright)
  requires: []
  complements:
    - testing/visual-regression/playwright
    - testing/visual-regression/workflow
  specializes: ""
  category: testing
---

# Pixelmatch

`pixelmatch` is the Mapbox image-diff library at the core of most JS visual regression tooling — including Playwright's `toHaveScreenshot()`. These guides cover the algorithm, every option, and when to reach for a faster or different engine.

| I need to... | Guide | Summary |
|---|---|---|
| Understand what pixelmatch is and when to use it directly vs through Playwright | [Overview](pixelmatch-overview.md) | Use pixelmatch directly when diffing arbitrary PNGs outside Playwright (custom scripts, Puppeteer, Selenium). For standard Playwright VR tests, pixelmatch runs under the hood automatically — read this guide to tune its thresholds correctly. |
| Understand the YIQ + anti-aliasing detection algorithm | [Algorithm](pixelmatch-algorithm.md) | Pixelmatch uses YIQ color space (luminance-weighted) to compare pixels perceptually, then skips pixels on anti-aliased edges by default. Setting includeAA true or threshold 0 does not mean raw byte comparison — the algorithm is always perceptual. |
| Tune the threshold option | [Threshold](pixelmatch-threshold.md) | Lower threshold is stricter — it reduces the maximum allowed YIQ delta per pixel before flagging a diff. The pixelmatch library default is 0.1; Playwright overrides it to 0.2. Bump threshold only to absorb genuine env noise, never to silence flake. |
| Use includeAA, diffColor, diffMask, alpha | [Other Options](pixelmatch-other-options.md) | Use diffColorAlt to distinguish additions from removals in the diff PNG, and diffMask to get a transparent-background overlay. Avoid includeAA true unless captures are pinned to identical rendering environments, and avoid alpha 1 which hides the diff overlay behind the original image. |
| Call the API from Node | [API](pixelmatch-api.md) | Call pixelmatch(img1, img2, output, width, height, options) with decoded RGBA Uint8Array buffers — not PNG file bytes. Pass null as output for count-only mode. Returns an integer count of mismatched pixels. |
| Use the CLI for ad-hoc diffs | [CLI](pixelmatch-cli.md) | Run npx pixelmatch img1.png img2.png diff.png threshold in shell scripts. Exit code 0 means match, 66 means diffs detected (not an error), 64/65 are real failures. Colors, diffMask, and alpha are API-only — write a Node script for those. |
| Load PNG files into pixelmatch via pngjs or sharp | [Reading PNGs](pixelmatch-reading-pngs.md) | Use pngjs as the default PNG decoder — PNG.sync.read() returns an object with a .data RGBA Buffer that pixelmatch expects directly. For multi-format support (JPEG, WebP) or faster processing, use sharp with .raw().ensureAlpha() to guarantee the RGBA channel order. |
| Handle the same-size requirement | [Same-Size Constraint](pixelmatch-same-size.md) | Pixelmatch requires both buffers to be identical dimensions — it has no resize, pad, or align logic. The API throws, the CLI exits 65, and Playwright fails the assertion outright. Fix capture conditions so images match natively; resizing introduces interpolation artifacts that produce false diffs. |
| Evaluate performance and when to switch to odiff | [Performance](pixelmatch-performance.md) | Pixelmatch is single-threaded pure JS — adequate for suites under 500 screenshots. For larger suites or 4K captures, odiff is ~6x faster via native SIMD. Never replace pixelmatch inside Playwright's toHaveScreenshot — its auto-retry stability is tied to it. |
| Understand how Playwright defaults differ from pixelmatch defaults | [Inside Playwright](pixelmatch-inside-playwright.md) | Playwright defaults to threshold 0.2 (pixelmatch's own default is 0.1) and adds two extra knobs — maxDiffPixels and maxDiffPixelRatio — on top of the raw pixel count. Without either extra knob configured, any non-zero diff fails the test. |
| Use pixelmatch in custom scripts outside Playwright | [Standalone Use](pixelmatch-standalone.md) | Build standalone diff scripts with pngjs for PNG decoding and pixelmatch for the comparison. Always guard against dimension mismatches explicitly — pixelmatch throws. For Puppeteer or other captures, pin viewport and DPR consistently across baseline and current captures. |
| Know pixelmatch's limitations and when to switch | [Limitations & Alternatives](pixelmatch-limitations.md) | Pixelmatch is RGBA-only, single-threaded, and has no SSIM or semantic awareness. Switch to odiff for speed, looks-same for cross-OS font tolerance (CIEDE2000), or dssim for compression-robust structural similarity. Never switch libraries to mask flake — fix the environment first. |
| Pick a threshold for a specific scenario | [Tuning Recipes](pixelmatch-tuning-recipes.md) | Start with Playwright's default of 0.2 and stabilize the suite, then tighten incrementally toward 0.1. For cross-OS captures use 0.2–0.3; for animations and gradients prefer maxDiffPixelRatio over raising threshold. Document every non-default per-test threshold with a comment. |
