---
description: Pixelmatch limitations and when to switch to odiff, looks-same, resemble.js, or dssim.
tldr: Pixelmatch is RGBA-only, single-threaded, and has no SSIM or semantic awareness. Switch to odiff for speed, looks-same for cross-OS font tolerance (CIEDE2000), or dssim for compression-robust structural similarity. Never switch libraries to mask flake — fix the environment first.
---

# Pixelmatch Limitations & Alternatives

## When to Use

> Use this when deciding whether pixelmatch is the right tool, or which alternative fits a specific scenario.

## Decision

| Need | Library |
|---|---|
| Drop-in, mostly compatible | pixelmatch (default) |
| Same algorithm, much faster | odiff |
| Cross-OS font tolerance | looks-same (CIEDE2000) |
| Structural similarity (compression-robust) | dssim (SSIM) |
| Browser-side diffing | resemble.js |

## Alternatives

| Library | Algorithm | When |
|---|---|---|
| **odiff** | Same YIQ + AA, OCaml/native, SIMD | Suites > 500 screenshots; 4K captures; CI throughput |
| **looks-same** | CIEDE2000 (industry-standard perceptual color delta) | Cross-OS font/AA differences |
| **resemble.js** | Browser-friendly; mismatch percentage | Browser-side comparisons without bundling pngjs |
| **dssim** | Rust-based SSIM (structural similarity) | Robust against minor compression/AA noise |

## Limitations

- **RGBA only** — must convert grayscale or RGB sources first
- **Strict same-dimension requirement** — no resize/align logic
- **No SSIM / CIEDE2000 / perceptual-hash modes** — YIQ + AA detection is the entire toolkit
- **No semantic awareness** — moved layouts produce huge diffs even if visually "equivalent"
- **No font-rendering tolerance beyond the AA detector** — sub-pixel font hinting across OSes leaks through unless threshold is raised
- **Single-threaded** — slow on large images or large suites

## Common Mistakes

- **Wrong**: Switching libraries to mask flake — fix the env first; algorithm choice is downstream
- **Wrong**: Picking SSIM for pixel-perfect VR — SSIM is "perceptually similar," not strict; you'll miss small regressions
- **Wrong**: Picking pixelmatch for cross-OS font comparisons — use looks-same or fix the environment

## See Also

- [Performance](pixelmatch-performance.md) — when odiff throughput becomes relevant
- [Overview](pixelmatch-overview.md) — decision table for pixelmatch vs Playwright vs alternatives
- Reference: [odiff](https://github.com/dmtrKovalenko/odiff)
- Reference: [looks-same](https://github.com/gemini-testing/looks-same)
