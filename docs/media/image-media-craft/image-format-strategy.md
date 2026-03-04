---
description: Choose JPEG, WebP, AVIF, PNG, SVG, or video — format decision table, quality settings by use case, and animated image strategy
---

# Image Format Strategy

## When to Use

> Use this when deciding what format to produce and serve. Choosing the wrong format is the single biggest avoidable image performance mistake. For 2025 projects: AVIF first, WebP fallback, JPEG as ultimate fallback.

## Decision

| Format | Best For | Avoid When | Typical Size vs JPEG |
|---|---|---|---|
| **JPEG** | Fallback for photos; maximum compatibility | You can use WebP/AVIF | Baseline |
| **WebP** | Photos, broad compatibility, fastest decode | IE (dead); use as primary + AVIF as upgrade | 25–34% smaller |
| **AVIF** | Maximum compression, high-fidelity photos, HDR | Encode time is a concern; use as `<picture>` first source | 45–55% smaller |
| **PNG** | Logos, screenshots, illustrations with transparency; lossless | Photos (huge files) | Often 2–5x larger than JPEG |
| **SVG** | Icons, logos, diagrams, anything that scales | Photography; complex raster art | N/A (vector) |
| **GIF** | Legacy animated content only | All new animated content — use `<video>` instead | Always replace with video |

**2025 delivery strategy**: AVIF (93%+ browser support) → WebP (95%+ support) → JPEG fallback

## Pattern

```html
<picture>
  <source srcset="photo.avif" type="image/avif">
  <source srcset="photo.webp" type="image/webp">
  <img src="photo.jpg" alt="..." width="800" height="600">
</picture>
```

**Quality settings by use case**:

| Context | Format | Quality | Target File Size |
|---|---|---|---|
| Hero / full-bleed | AVIF | 65–75 | < 200KB |
| Hero / full-bleed | WebP | 80–85 | < 250KB |
| Card image (medium) | AVIF | 60–70 | < 60KB |
| Card image (medium) | WebP | 75–80 | < 80KB |
| Thumbnail | WebP | 60–70 | < 20KB |
| Photo / article | WebP | 80 | < 120KB |
| Illustration / UI | PNG (lossless) | — | < 50KB |
| SVG icon | SVG (SVGO-optimized) | — | < 5KB |

**Animated images**:

| If you need... | Use... | Why |
|---|---|---|
| Looping background animation | `<video autoplay muted loop playsinline>` | 5–20x smaller than GIF; hardware decoded |
| User-controlled animated content | `<video controls>` with poster | Accessibility-compliant |
| Animated illustration from `<img>` | WebP animated | 64%+ browser support; 70% smaller than GIF |

## Common Mistakes

- **Wrong**: serving PNG for photographs → **Right**: JPEG/WebP at quality 80 produces smaller files with negligible visible difference
- **Wrong**: skipping AVIF because encoding is slow → **Right**: pre-encode at build time or use CDN auto-format; decoding is fast
- **Wrong**: WebP at quality 90+ → **Right**: quality 75–85 is the sweet spot; above 90, WebP files can exceed equivalent JPEG
- **Wrong**: no `<img src>` in `<picture>` fallback chains → **Right**: always include `<img src>` as the ultimate fallback
- **Wrong**: animated GIF in new projects → **Right**: always use `<video>` or animated WebP

## See Also

- [Build Pipeline Optimization](build-pipeline-optimization.md) — how to produce these formats at build time
- [Drupal Media Pipeline](drupal-media-pipeline.md) — Drupal's ImageAPI Optimize for format conversion
- Reference: [MDN Image Types Guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)
- Reference: [SpeedVitals WebP vs AVIF 2025](https://speedvitals.com/blog/webp-vs-avif/)
