---
description: Choose JPEG, WebP, AVIF, PNG, SVG, or video — format decision table, quality settings by use case, and animated image strategy
tldr: "Use this when deciding what format to produce and serve. Choosing the wrong format is the single biggest avoidable image performance mistake."
---

# Image Format Strategy

## When to Use

> Choosing the wrong format is the single biggest avoidable image performance mistake. Use this section when deciding what format to produce and serve, including animated content.

## Decision

| Format | Best For | Avoid When | Typical Size vs JPEG |
|---|---|---|---|
| **JPEG** | Fallback for photos; maximum compatibility | You can use WebP/AVIF | Baseline |
| **WebP** | Photos, broad compatibility, fastest decode | IE (dead); use as primary + AVIF as upgrade | 25–34% smaller |
| **AVIF** | Maximum compression, high-fidelity photos, HDR | Encode time is a concern; use as `<picture>` first source | 45–55% smaller |
| **PNG** | Logos, screenshots, illustrations with transparency; lossless | Photos (huge files) | Often 2–5x larger than JPEG |
| **SVG** | Icons, logos, diagrams, illustrations, anything that scales | Photography; complex raster art | N/A (vector) |
| **GIF** | Legacy animated content only | All new animated content — use `<video>` instead | Always replace with video |

**Format delivery strategy** (2025 baseline):
```
AVIF (preferred, 93%+ browser support) → WebP (95%+ support) → JPEG fallback
```

Use `<picture>` with `type` sources to implement the fallback chain — browser picks first supported format:
```html
<picture>
  <source srcset="photo.avif" type="image/avif">
  <source srcset="photo.webp" type="image/webp">
  <img src="photo.jpg" alt="..." width="800" height="600">
</picture>
```

## Quality Settings by Use Case

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

**AVIF encode time**: AVIF encoding is 5–10x slower than WebP at equivalent quality. For build-time pipelines, use parallel encoding with Sharp or libvips. For CMS/on-demand, consider CDN-side conversion (Cloudinary, imgix, Cloudflare Images auto-format).

## Animated Images

| If you need... | Use... | Why |
|---|---|---|
| Looping background animation | `<video autoplay muted loop playsinline>` | 5–20x smaller than GIF; hardware decoded |
| User-controlled animated content | `<video controls>` with poster | Respects reduced motion, accessibility |
| Animated illustration served from `<img>` | WebP animated | 64%+ browser support; 70% smaller than GIF |
| Maximum compatibility animated | GIF | Last resort; massive files, no audio |

**Never** use GIF for new content. A 3-second animation that is 3MB as GIF is typically 150–300KB as WebP or `<video>`.

## Content Negotiation (CDN Auto-Format)

Cloudinary, imgix, and Cloudflare Images support automatic format selection via `Accept` header: the CDN detects what the browser supports and serves the best format without `<picture>` elements. Trade-off: simpler markup, but you lose fine-grained control and are locked to the CDN.

## Common Mistakes

- Serving PNG for photographs — JPEG/WebP at quality 80 produces smaller files with negligible visible difference
- Skipping AVIF because "it's slow to encode" — pre-encode at build time or use CDN auto-format; decoding is fast
- Using WebP at quality 90+ — at high quality settings WebP files can exceed equivalent JPEG; quality 75–85 is the sweet spot
- Serving `image/jpeg` to `<picture>` fallback chains without the `src` on `<img>` — always include `<img src>` as the ultimate fallback
- Animated GIF in new projects — always use `<video>` or animated WebP

## See Also

- [Build Pipeline Optimization](build-pipeline-optimization.md) — how to produce these formats at build time
- [Drupal Media Pipeline](drupal-media-pipeline.md) — Drupal's ImageAPI Optimize for format conversion
- Reference: [MDN Image Types Guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types)
- Reference: [SpeedVitals WebP vs AVIF 2025](https://speedvitals.com/blog/webp-vs-avif/)
